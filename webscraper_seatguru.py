import pandas as pd 
import numpy as np 
import sys
import requests 
import re 
from bs4 import BeautifulSoup 

def get_data(r, airline_company, airplane):
	rows = list() 
	soup = BeautifulSoup(r.text, 'html.parser')

	user_comments = soup.find('div', class_ = 'aside-box-alt aircraftPage user-comments')

	if user_comments:
		info_comments = user_comments.find_all('div', class_ = 'submitted')
		comments  = user_comments.find_all('div', class_ = 'comment')

		# check length matches
		for (info, comment) in zip(info_comments, comments):
			raw_text_info = info.find('span', class_ = 'date').text
			date_posted = re.search(r'(\d+/\d+/\d+)', raw_text_info).group(1)
			## do something about the seat in info?
			comment_text = comment.text.strip()
			rows.append([date_posted, comment_text, airline_company, airplane]) # append the data 
	#print(rows)
	return rows 

def get_airplane_names(r):
	airplanes = list() 
	soup = BeautifulSoup(r.text, 'html.parser')
	tables = soup.find_all('table', class_ = 'seats')

	for table in tables:
		links = table.find_all('a')

		for link in links:
			airplanes.append(link.get('href'))

	print(airplanes)
	return airplanes 

def get_airline_names(r):
	airlines = list() 
	soup = BeautifulSoup(r.text, 'html.parser')
	uls = soup.find('div', class_ = 'browseAirlines').find_all('ul')

	for ul in uls:
		links  = ul.find_all('a')
		for link in links:
			airlines.append(link.get('href'))

	return airlines

def request_website(website):
	try:
		r = requests.get(website)
	except requests.exceptions.RequestException as e:
		print(e)

	if r.status_code == 200:
		return r

	return 'error'


if __name__ == '__main__':
	data = list() 
	r = request_website('https://www.seatguru.com/browseairlines/browseairlines.php')
	airlines  = get_airline_names(r)
	r.close()
	

	for count, airline in enumerate(airlines):
		print('Webscraping airline %d/%d' % (count, (len(airlines) - 1) ))
		url_base = 'https://www.seatguru.com/' + airline
		r = request_website(url_base)

		# do this for a certain amount of companies 

		if r != 'error':
			airplanes = get_airplane_names(r)
			r.close()

			for i, airplane in enumerate(airplanes):
				print('Airplane %d/%d' % (i, (len(airplanes) - 1) ))
				website = 'https://www.seatguru.com/' + airplane
				r2 = request_website(website)

				if r2 != 'error':
					airline_comp = airplane.split('/')[2]
					airplane_name = airplane.split('/')[3].split('.ph')[0]
					airline_data = get_data(r2, airline_comp, airplane_name)
					r2.close()

					data = data + airline_data
	
	df = pd.DataFrame(data, columns = ['date', 'comment', 'flight_company', 'airplane_model'])
	df.to_csv('./data/seatguru_data.csv', index=False)
	print('file written')