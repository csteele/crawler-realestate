import csv
import pickle

IN_PATH='../../data/SA2_2016_AUST.csv'
OUT_PATH='../../data/locations.p'

def parse_location(location):
	replace=['- East', '- West', '- North' ,'- South',
	         'East', 'West', 'North', 'South'
	         ,'(East)', '(West)','(North)','(South)'
	         ,'Region','(Qld)']
	for r in replace:
		location=location.replace(r,'')
	locations=location.split(' - ')
	return locations

def process_locations(IN_PATH):
	with open(IN_PATH) as f:
		reader = csv.reader(f)
		header=next(reader)

		location_index=header.index("SA2_NAME_2016")
		state_index=header.index("STATE_NAME_2016")
		results=[]
		for row in reader:
			if row[state_index]=="Queensland":
				SA2_NAME_STRING=row[location_index]
				locations=parse_location(SA2_NAME_STRING)
				results.extend(locations)
		return set(results)


with open(OUT_PATH,'wb') as f:
	locations=process_locations(IN_PATH)
	print(locations)
	print(len(locations))
	pickle.dump(locations,f)