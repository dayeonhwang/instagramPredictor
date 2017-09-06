import json
import re

def loadJSON(filename):
	with open(filename) as json_data:
		data = json.load(json_data)
		res= ""
		for element in data: # element: each user
			for e in element.values():
				for i in e:
					i=i.replace('<p class="grid-media-caption">', "caption: ")
					i=i.replace('<i class="fa fa-map-marker"></i>', "location: ")
					i=i.replace('<li class="text-color-3">', "lc: ")
					i=i.replace('<ul class="list-inline grid-media-info "> <li>',"date: ")
					i=i.replace('<ul class="list-inline grid-media-info  grid-media-info-vertical "> <li>',"")
					i=i.replace('</li>',"")
					i=i.replace('</ul>',"")
					i=i.replace('</p>',"")
					i=i.replace('</a>',"")
					i=i.replace('</span>',"")
					i=re.sub("<a href=[^>]*\">","",i)
					i=re.sub('<p class="grid-media-location"> <a class="btn btn-xs btn-orange" href=[^>]*\">',"",i)
					i=i.replace('caption: ADVERTISEMENT',"")
					i=i.replace('<span class="p-stat-number">'," stat: ")
					i=i.replace('&amp;',"and")
					res+=i
		return res

def convert_to_num(input_str):
	input_str = input_str.replace(",", "")
	try:
		thousand=input_str.index("K")
		input_str=input_str.replace("K","")
		num=int(input_str)*1000
	except ValueError:
		try:
			mil=input_str.index("M")
			input_str=input_str.replace("M","")
			num=int(input_str)*1000000
		except ValueError:
			num=int(input_str)
	return num

def postsplit(input):
	post={}
	date=input.index("date: ")
	try:
		location=input.index("location: ")
		post["location"]=input[location+11:date]
	except ValueError:
		post["location"]=""
	
	
	likes=input.index("lc: ")
	comments=input.index("lc: ", likes+2)
	caption=input.index("caption: ")
	post["date"]=input[date+6:likes]
	post["likes"]=input[likes+4:comments]
	post["comments"]=input[comments+4:caption]
	post["caption"]=input[caption+9:]
	num_tags=input.count("#")
	post["num_tags"]=num_tags
	num_insta_tags=input.count("@")
	post["num_insta_tags"]=num_insta_tags
	return post

def add_newline(str, indices):
	start=0
	output=""
	for i in range(len(indices)-5):
		if i%5==0:
			output+=str[indices[i]:indices[i+5]]+"\n"
			start=indices[i]+1

def convert_to_dict(filename):
	# load JSON file
	data = loadJSON(filename)

	# initialize variables
	user_stat = {}
	#user_stats_attr = ["num_posts", "num_followers", "num_followings", "total_likes", "total_comments"]
	final_dict = {}
	post_dict = {}
	date_indices=[]
	stat_indices=[]
	first_date=[]
	loc_indices=[]
	for m in re.finditer('date: ', data):
		date_indices.append(m.start())
	for m in re.finditer('stat: ', data):
		stat_indices.append(m.start())
	for m in re.finditer('location: ', data):
		loc_indices.append(m.start())

	start=0
	stats=[]
	data=add_newline(data, stat_indices)
	user_count=0
	for line in iter(data.splitlines()):
		stat_line=[]
		user={}
		user_stat={}
		for m in re.finditer('stat: ', line):
			stat_line.append(m.start())
		start_info_loc=1000000
		try:
			
			start_info_loc=line.index("location: ")
		except ValueError:
			start_info_loc=100000000
		
		start_info_date=line.index("date: ")
		start_info_index=min(start_info_date, start_info_loc)
		user_stat["num_posts"]=line[stat_line[0]+6:stat_line[1]]
		user_stat["num_followers"]=line[stat_line[1]+6:stat_line[2]]
		user_stat["num_followings"]=line[stat_line[2]+6:stat_line[3]]
		user_stat["total_likes"]=line[stat_line[3]+6:stat_line[4]]
		user_stat["total_comments"]=line[stat_line[4]+6:start_info_index]
		for key,value in user_stat.iteritems():
			user_stat[key]=convert_to_num(value)
		user["stats"]=user_stat
		date_line=[]
		lc_line=[]
		caption_line=[]
		location_line=[]
		posts={}
		post={}
		post_count=0
		#(optional)location - date - likes - comments - caption
		for m in re.finditer('location: ', line):
			location_line.append(m.start())
		for m in re.finditer('date: ', line):
			date_line.append(m.start())

		for i in range(len(date_line)-1):
			one_post=line[date_line[i]:date_line[i+1]]
			try:
				loc=one_post.index("location: ")
				one_post=one_post[0:loc]
			except ValueError:
				one_post=one_post
			if len(location_line)!=0 and location_line[0]<date_line[i]:
				one_post=line[location_line[0]:date_line[i]]+one_post

				location_line.pop(0)
			posts[post_count]=postsplit(one_post)
			post_count+=1
		user["posts"]=posts
		final_dict[user_count]=user
		user_count+=1
		post_count=0
	return final_dict

final_dict = convert_to_dict('quotes.json')
final_json = json.dumps(final_dict, ensure_ascii=False, sort_keys=True, indent=4)

with open('result.json', 'w') as file:
    json.dump(final_dict, file)
