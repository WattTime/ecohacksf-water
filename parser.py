import json
import requests

def hit_api():
	"""Hits the WattTime API and returns json information for CAISO."""

	response = requests.get('http://api.watttime.org/api/v1/datapoints/', 
		headers={'Authorization': 'Token 07ec538dda25b11a5414a32bf250319f78a68dfc'}, 
		params={'ba': 'CAISO', 'page_size': 1})
	
	json_data = response.json()

	return json_data["results"][0]["carbon"]


# TODO: Decide if want to split this into two functions
def parse(json_data):
	"""Returns the average carbon intensity."""

	print json_data["results"][0]["carbon"]


if __name__ == "__main__":
	hit_api()
	#parsed = parse(data)