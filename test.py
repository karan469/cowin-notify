import requests
import argparse
import json
import logging
# from datetime import date
import datetime
import time
import os

logging.basicConfig(level=logging.INFO, 
					filename='dump.log', 
					filemode='a', 
					format='%(name)s - %(levelname)s - %(message)s')

def by_district(district_id, date):
	url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=%s&date=%s' % (district_id,date)
	res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
							'accept': 'application/json'})
	res = (res.json())
	with open('dump_district.json', 'w') as f:
		f.write(json.dumps(res, indent=2))

def by_pin(pin, date):
	url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=%s&date=%s' % (pin,date)
	res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
							'accept': 'application/json'})
	res = (res.json())
	with open('dump_pin.json', 'w') as f:
		f.write(json.dumps(res, indent=2))


def interpret_json(filename, channel_hook, minimum_age):
	with open(filename, 'r') as fd:
		s = fd.read()
		s = s.replace("\'", "\"")
		data = json.loads(s)
	
	centers_n_sessions = {}
	centers = (data['centers'])
	
	for center in centers:
		sessions = center['sessions']
		
		for session in sessions:
			if(session['min_age_limit']==minimum_age and session['available_capacity']>0):
				try:
					centers_n_sessions[center['name'].append(session)]
				except:
					centers_n_sessions[center['name']] = [session]
	
	for i in centers_n_sessions:
		centers_n_sessions[i] = sum([j['available_capacity'] for j in centers_n_sessions[i]])
	
	print(centers_n_sessions)
	if(centers_n_sessions):
		logging.info(centers_n_sessions)
		message = str(centers_n_sessions)
		message = message.replace("'", "")
		# self DM
		print('here')
		os.system("curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"%s\"}' https://hooks.slack.com/services/%s" % (message, channel_hook))
		time.sleep(60)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Cowin slots checker by @_tanwar_karan')
	parser.add_argument('--district_id', type=int, action='store')
	parser.add_argument('--pincode', type=int, action='store')
	parser.add_argument('--channel_hook', type=str, action='store')
	parser.add_argument('--method', type=str, choices=['pincode', 'district_id'], action='store')
	parser.add_argument('--minimum_age', type=int, default=18, choices=[18, 45], action='store')

	args = parser.parse_args()

	print(args)

	while(True):
		try:
			os.system('rm dump_pin.json')
			os.system('rm dump_district.json')
		except:
			pass
		date = datetime.date.today().strftime("%d-%m-%Y")
		if(args.method=='district_id' or args.district_id):
			by_district(args.district_id, date)
			interpret_json('dump_district.json', args.channel_hook, args.minimum_age)
		elif (args.method=='pincode' or args.pincode):
			by_pin(args.pincode, date)
			interpret_json('dump_pin.json', args.channel_hook, args.minimum_age)

		time.sleep(3)

