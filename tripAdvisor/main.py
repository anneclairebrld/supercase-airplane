from static import FEED_URL
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from helpers import *
import time

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('window-size=1200,800')


class Scraper:
    def __init__(self):
        self.companies = []
        self.ratings = []
        self.url = FEED_URL

    @staticmethod
    def start_driver():
        return webdriver.Chrome(executable_path='/Users/macbookair/Desktop/supercase/chromedriver', chrome_options=chrome_options)

    def open_page(self, driver):
        driver.get(self.url)

    def scrap_company(self, driver, company_element, companies_list, excluded_companies_list, verbose):
        name = get_company_name(company_element)
        if is_company_valid(name, companies_list, excluded_companies_list):
            url = get_company_ratings_url(company_element)
            rating = get_company_rating(company_element)
            count = get_company_count(company_element)

            print('----- {} -----'.format(name))

            company = Company(name, url, rating, count)
            if not company in self.companies:
                print('Adding company {}'.format(name))
                self.companies.append(company)
                self.ratings = self.ratings + company.scrap(driver, verbose)
            return

    def scrap_companies(self, driver, companies_list, excluded_companies_list, verbose):
        companies_elements = get_companies_elements(driver)
        for i in range(len(companies_elements)):
            companies_elements = get_companies_elements(driver)
            self.scrap_company(driver,
                               companies_elements[i],
                               companies_list,
                               excluded_companies_list,
                               verbose)
            self.open_page(driver)

    def scrap(self, companies_list=None, excluded_companies_list=None, verbose=False):
        print('Starting driver ...')
        driver = Scraper.start_driver()

        self.open_page(driver)

        self.scrap_companies(driver,
                             companies_list,
                             excluded_companies_list,
                             verbose)

        print('Closing driver ...')
        driver.close()


class Company:
    def __init__(self, name, url, rating, count):
        self.name = name
        self.url = url
        self.rating = rating
        self.count = count

    def go_to(self, driver):
        driver.get(self.url)

    def go_to_next_page(self, driver):
        element = driver.find_element_by_class_name('next')
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.execute_script(
            "window.scrollTo(10, document.body.scrollHeight-950);")
        element.click()

    def scrap_rating(self, driver, element, verbose):
        try:
            get_more_from_rating(driver, element)

            global_rating = get_global_rating_from_element(element)
            title = get_title_from_element(element)
            comment = get_comment_from_element(element)
            date = get_date_from_element(element)
            travel = get_travel_from_element(element)
            sub_ratings = get_sub_ratings_from_element(element)

            return Rating(company=self.name, global_rating=global_rating, title=title, comment=comment, date=date, sub_ratings=sub_ratings, travel=travel)
        except NoSuchElementException:
            return None

    def scrap_page_ratings(self, driver, verbose):
        page_ratings = []
        ratings_elements = get_ratings_elements(driver)
        for i in range(min(5, len(ratings_elements))):
            rating = self.scrap_rating(driver,
                                       ratings_elements[i],
                                       verbose)
            if rating:
                page_ratings.append(rating)
        return page_ratings

    def scrap_ratings(self, driver, verbose):
        scroll_to_bottom(driver)
        if self.count < 6:
            return self.scrap_page_ratings(driver, verbose)
        time.sleep(2)
        ratings = self.scrap_page_ratings(driver, verbose)
        for i in range(get_number_of_pages(driver)-1):
            self.go_to_next_page(driver)
            time.sleep(2)
            ratings = ratings + self.scrap_page_ratings(driver, verbose)
        return ratings

    def scrap(self, driver, verbose=False):
        self.go_to(driver)

        if verbose:
            print('{} ratings available'.format(self.count))

        return self.scrap_ratings(driver, verbose)


class Rating:
    def __init__(self, company, global_rating, title, comment, date, sub_ratings, travel):
        self.company = company
        self.global_rating = global_rating
        self.title = title
        self.comment = comment
        self.date = date
        self.sub_ratings = sub_ratings
        self.travel = travel


scraper = Scraper().scrap()
