import plistlib
import datetime
import uuid
import os
import shutil
import json

gpath = "."


def create_record(record_date, text, placename, city, country, lat, lng, picname):
	uid = uuid.uuid1().hex.upper()
	locdict = {"Place Name" : placename}
	if city is not None: locdict["Locality"] = city
	if country is not None: locdict["Country"] = country
	if lat is not None: locdict["Latitude"] = lat
	if lng is not None: locdict["Longitude"] = lng
	default_dic = {
		"Activity":"Stationary",
		"Creation Date": record_date,
		"Creator": {"Generation Date": record_date, "OS Agent": "Linux", "Software Agent": "4s2d1 Converter"},
		"Entry Text": text,
		"Ignore Step Count": True,
		"Location": locdict,
		"Starred": False,
		"Tags": ("Imported", "4square"),
		"UUID": uid
	}
	filename = os.path.join(gpath, "entries", uid+".doentry")
	plistlib.writePlist(default_dic, filename)

	if picname is not None:
		srcfile = os.path.join(gpath, picname)
		destfile = os.path.join(gpath, "photos", uid+".jpg")
		shutil.copyfile(srcfile, destfile)
	return uid


def convert_file(filename):
	f = file(filename,'r')
	lines = f.readlines()
	f.close()
	for l in lines:
		d = json.loads(l)
		t = datetime.datetime.fromtimestamp(d['createdAt'])
		text_str='4square check-in'
		if 'shout' in d:
			text_str=d['shout']
		venue = d['venue']
		city = None
		country = None
		lat = None
		lng = None
		pic = None
		if 'location' in venue:
			loc = venue['location']
			if 'city' in loc:
				city = loc['city']
			if 'country' in loc:
				country = loc['country']
			if 'lat' in loc and 'lng' in loc:
				lat = loc['lat']
				lng = loc['lng']
		photos = d['photos']
		if photos['count'] != 0:
			pi = photos['items']
			pic = pi[0]['suffix'][1:]
		create_record(t, text_str, venue['name'], city, country, lat, lng, pic)

convert_file('myplaces2.txt')