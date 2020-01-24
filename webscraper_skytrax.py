import pandas as pd 
import numpy as np 
import sys
import requests 
import binascii
from bs4 import BeautifulSoup 

url_base = 'https://www.airlinequality.com/airline-reviews/air-caraibes/page/1/'

r = requests.get(url_base)

id = 0 
rows = list()

if r.status_code == 200:
	soup = BeautifulSoup(r.text, 'html.parser')

	for article in soup.find_all('article', class_ = 'comp'):
		airplane_model = None
		review_title = None
		date_of_comment = None
		verified = None 
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
		flight_company = None 
		airplane_model = None

		if  article.find('time'):
			if article.find('h2', class_ = 'text_header'):
				review_title = article.find('h2', class_ = 'text_header').text

			date_of_comment = article.find('time')['datetime'] 
			overall_rating = article.find('div', class_ = 'rating-10').find('span').text
			print(review_title)
			print(date_of_comment)
			print(overall_rating)
			review_comment = article.find('div', class_ = 'tc_mobile' ).find('div', class_ = 'text_content')
			

			if review_comment:
				verified = False
				if review_comment.text.split()[0].encode('utf-8') == b'\xe2\x9c\x85':
					verified = True 

				review_comment = review_comment.text.split('|')[1]

			for review_stats in article.find_all('table', class_ = 'review-ratings'): #  
				print('Review_stat found') 
				


				# get all review stats 
				for tr in review_stats.find_all('tr'):
					rating_header = tr.find('td', class_ = 'review-rating-header').text.strip().lower() 
					rating_stars = tr.find('td', class_ = 'review-rating-stars')
					rating_text = tr.find('td', class_ = 'review-value')

					stat = None

					if rating_stars :
						stat = rating_stars.find_all('span', class_ = 'star fill')[-1].text
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

					print('%s, %s' % (rating_header, stat )) 

				print('\n')

			
			review_data = [id, date_of_comment, verified, review_title, review_comment, type_of_traveler, 
				start_point, end_point, date_flown, overall_rating, 
				recommended, seat_comfort, cabin_staff_service, food_beverages, 
				ground_service, value_for_money, flight_company, airplane_model]

			rows.append(review_data)
			id += 1 

columns = ['id', 'date', 'verified', 'review_title', 'review_comment', 'type_of_traveler', 
			'start_point', 'end_point', 'date_of_flight', 'overall_rating', 
			'recommended', 'seat_comfort', 'cabin_staff_service', 'food_beverages', 
			'ground_service', 'value_for_money', 'flight_company', 'airplane_model']

df = pd.DataFrame(rows, columns = columns)
print(df.head())
print(df.tail())

print(df.review_title)
print(id)