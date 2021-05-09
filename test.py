import requests
import argparse
import json
import logging
from datetime import date
import time
import os

logging.basicConfig(level=logging.INFO, 
					filename='dump.log', 
					filemode='a', 
					format='%(name)s - %(levelname)s - %(message)s')

def main(pin, date):
	url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=%s&date=%s' % (pin,date)
	res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
							'accept': 'application/json'})
	res = (res.json())
	with open('dump.json', 'w') as f:
		f.write(json.dumps(res, indent=2))

def interpret_json(filename):
	with open(filename, 'r') as fd:
		s = fd.read()
		s = s.replace("\'", "\"")
		data = json.loads(s)
	centers_n_sessions = {}
	centers = (data['centers'])
	for center in centers:
		sessions = center['sessions']
		
		is_covishield = False
		is_covaxin = False
		
		for session in sessions:
			if(session['min_age_limit']<45 and session['available_capacity']>0):
				is_covishield = (session['vaccine']=="COVISHIELD")
				is_covaxin = (session['vaccine']=="COVAXIN")
				try:
					centers_n_sessions[center['name'].append(session)]
				except:
					centers_n_sessions[center['name']] = [session]
	for i in centers_n_sessions:
		centers_n_sessions[i] = sum([j['available_capacity'] for j in centers_n_sessions[i]])
	
	if(centers_n_sessions):
		logging.info(centers_n_sessions)
		message = str(centers_n_sessions)
		# message = message.replace('{', '|')
		# message = message.replace('}', '|')
		message = message.replace("'", "")
		message += " > " + "COVAXIN: " + str(is_covaxin) + " - COVISHIELD: " + str(is_covishield)
		os.system("curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"%s\"}' https://hooks.slack.com/services/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" % message)

if __name__ == '__main__':
	pin = '110085'
	date = '10-05-2021'
	# main(pin, date)
	# interpret_json('dump.json')

	while(True):
		try:
			os.system('rm dump.json')
		except:
			pass
		# date = date.today().strftime("%d-%m-%Y")
		main(pin, date)
		interpret_json('dump.json')
		time.sleep(3)

