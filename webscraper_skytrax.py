import pandas as pd 
import numpy as np 
import sys
import requests 
import binascii
from bs4 import BeautifulSoup 


def get_data(r, airline_name):
	rows = list()	# this is where the rows of data will be stored
	soup = BeautifulSoup(r.text, 'html.parser')

	# grab all review pages
	for article in soup.find_all('article', class_ = 'comp', itemprop = 'review'):
		# declare variables for data structure
		airplane_model = None
		review_title = None
		date_of_comment = None
		verified = False 
		review_title = None 
		type_of_traveler = None 
		start_point = None 
		end_point = None 
		date_of_flight = None 
		overall_rating = None 
		recommended = None 
		seat_comfort = None
		cabin_staff_service = None
		food_beverages = None 
		ground_service = None 
		value_for_money = None  
		airplane_model = None

		# check to see if something was posted (if no time then data we are not interested in)
		if  article.find('time'):
			if article.find('h2', class_ = 'text_header'):
				review_title = article.find('h2', class_ = 'text_header').text

			date_of_comment = article.find('time')['datetime'] 
			review_comment = article.find('div', class_ = 'tc_mobile' ).find('div', class_ = 'text_content')
			
			if article.find('div', class_ = 'rating-10').find('span'):
				overall_rating = article.find('div', class_ = 'rating-10').find('span').text

			if review_comment:
				review_comment = review_comment.text

				# check if the comment was verified by someone 
				if review_comment.split()[0].encode('utf-8') == b'\xe2\x9c\x85':
					verified = True 
					review_comment = review_comment.split('|')[1]  # get review comments interesting part

			
			# grab the stats/basic information of a review
			for review_stats in article.find_all('table', class_ = 'review-ratings'): #  
				for tr in review_stats.find_all('tr'):
					rating_header = tr.find('td', class_ = 'review-rating-header').text.strip().lower() 
					rating_stars = tr.find('td', class_ = 'review-rating-stars')
					rating_text = tr.find('td', class_ = 'review-value')

					stat = None

					if rating_stars :
						stat = len(rating_stars.find_all('span', class_ = 'star fill'))
					elif rating_text:
						stat = rating_text.text

					if rating_header == 'type of traveller' :
						type_of_traveler = stat
					elif rating_header == 'route':
						start_point = stat.strip().split(' to ')[0]
						end_point = stat.strip().split(' to ')[-1]
					elif rating_header == 'date flown':
						date_flown = stat
					elif rating_header == 'recommended':
						recommended = stat
					elif rating_header == 'seat comfort':
						seat_comfort = stat
					elif rating_header == 'cabin staff service':
						cabin_staff_service = stat
					elif rating_header == 'food & beverages':
						food_beverages = stat
					elif rating_header == 'ground service':
						ground_service = stat
					elif rating_header == 'value for money':
						value_for_money = stat
					elif rating_header == 'aircraft':
						airplane_model = stat

			# create new row of data
			review_data = [date_of_comment, verified, review_title, review_comment, type_of_traveler, 
				start_point, end_point, date_flown, overall_rating, 
				recommended, seat_comfort, cabin_staff_service, food_beverages, 
				ground_service, value_for_money, airline_name, airplane_model]

			# add data row to data 
			rows.append(review_data)
	
	return rows



# define colunmns of data
columns = ['date', 'verified', 'review_title', 'review_comment', 'type_of_traveler', 
			'start_point', 'end_point', 'date_of_flight', 'overall_rating', 
			'recommended', 'seat_comfort', 'cabin_staff_service', 'food_beverages', 
			'ground_service', 'value_for_money', 'flight_company', 'airplane_model']


## define the airline companies 
airline_companies = ['american-airlines', 'british-airways', 'emirates', 'ryanair', 'virgin-atlantic']

# unique id counter 


if __name__ == '__main__':
	data = list()

	# grab data for each airline
	for i, airline in enumerate(airline_companies):
		print('Getting data: %d / %d' % (i, (len(airline_companies)-1 )))
		# define url_base  
		url_base = 'https://www.airlinequality.com/airline-reviews/' + airline + '/?sortby=post_date%3ADesc&pagesize=10000'

		try:
			r = requests.get(url_base)
		except requests.exceptions.RequestException as e:
			print('Airline %s ERROR ' % airline)
			print(e)

		# if no error get the data 
		if r.status_code == 200:
			airline_data = get_data(r, airline)
			r.close()

		data = data + airline_data
		print('Data for %s loaded' % airline)

	df = pd.DataFrame(data, columns = columns)

	df.to_csv('data.csv', index=False)
	print('File written')
