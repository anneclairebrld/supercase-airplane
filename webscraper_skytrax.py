import pandas as pd 
import numpy as np 
import sys
import requests 
from bs4 import BeautifulSoup 

url_base = 'https://www.airlinequality.com/airline-reviews/air-caraibes/page/1/'

r = requests.get(url_base)
if r.status_code == 200:
	soup = BeautifulSoup(r.text, 'html.parser')
	#print(soup.prettify())

	# for article in soup.find_all('article'): #   
		# print(article.find_all('div'))

