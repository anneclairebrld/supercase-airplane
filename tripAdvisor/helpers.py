from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def get_number_of_pages(driver):
    return int(driver.find_elements_by_css_selector("a.pageNum")[-1].text)
    
def get_companies_elements(driver):
    return driver.find_elements_by_class_name('prw_airlines_airline_lander_card')


def get_company_name(company_element):
    return company_element.find_element_by_class_name('airlineName').text


def get_company_ratings_url(company_element):
    return company_element.find_element_by_class_name('review_button'). get_attribute("href")


def bubble_to_number(bubble):
    return int(bubble.split('_')[1])


def get_company_rating(company_element):
    return bubble_to_number(company_element.find_element_by_class_name('ui_bubble_rating').get_attribute("class").split(' ')[1])


def get_company_count(company_element):
    return int(company_element.find_element_by_class_name('airlineReviews').text.split(' ')[0])


def get_rating_url(rating_element):
    try:
        return rating_element.find_element_by_class_name('article-item').get_attribute("href")
    except NoSuchElementException:
        return None


def is_company_valid(name, companies_list, excluded_companies_list):
    is_valid = (not companies_list or name in companies_list) and (
        not excluded_companies_list or not name in excluded_companies_list)
    if not is_valid:
        print('Excluding {}'.format(', '.join(excluded_companies_list)))
    return is_valid


def get_number_of_companies(driver):
    return len(get_companies_elements(driver))


def get_ratings_elements(driver):
    return driver.find_elements_by_class_name("location-review-card-Card__ui_card--2Mri0")


def get_more_from_rating(driver, element):
    el = element.find_element_by_class_name(
        'location-review-review-list-parts-ExpandableReview__reviewText--gOmRC')
    driver.execute_script("arguments[0].click();", el)


def get_global_rating_from_element(element):
    return bubble_to_number(element.find_element_by_class_name('location-review-review-list-parts-RatingLine__bubbles--GcJvM').find_element_by_class_name('ui_bubble_rating').get_attribute("class").split(' ')[1])


def get_title_from_element(element):
    return element.find_element_by_class_name('location-review-review-list-parts-ReviewTitle__reviewTitleText--2tFRT').text


def get_comment_from_element(element):
    return element.find_element_by_class_name('location-review-review-list-parts-ExpandableReview__reviewText--gOmRC').text


def get_date_from_element(element):
    try:
        return ' '.join(element.find_element_by_class_name('location-review-review-list-parts-EventDate__event_date--1epHa').text.split(' ')[-2:])
    except NoSuchElementException:
        return 'Non communiquée'


def get_travel_from_element(element):
    return element.find_element_by_class_name('location-review-review-list-parts-RatingLine__labelBtn--e58BL').text


def get_sub_ratings_from_element(element):
    sub_ratings = []
    try:
        sub_ratings_frame = element.find_element_by_class_name(
            'location-review-review-list-parts-AdditionalRatings__ratings--hIt-r')
        if sub_ratings_frame:
            sub_ratings_elements = sub_ratings_frame.find_elements_by_class_name(
                'location-review-review-list-parts-AdditionalRatings__rating--1_G5W')
            for sr in sub_ratings_elements:
                rating = bubble_to_number(
                    sr.find_element_by_class_name('ui_bubble_rating').get_attribute("class").split(' ')[1])
                name = sr.text
                sub_ratings.append({'name': name, 'rating': rating})
            return sub_ratings
    except NoSuchElementException:
        return []


def get_price_from_str(price_str):
    try:
        price = int(price_str.strip('€').strip().replace('.', ''))
    except ValueError:
        price = None
    return price


def get_price_from_element(element):
    return get_price_from_str(element.find_element_by_class_name('article-price').text)


def get_reference_from_element(element):
    return element.find_elements_by_class_name('row-direct')[4].text.split('\n')[1]


def get_model_from_rating_name(rating_name, brand_name):
    return rating_name.replace(brand_name + ' ', '')


def get_features_from_element(element):
    description = element.find_elements_by_class_name('row-direct')
    date = description[2].text.split('\n')[1]
    return {'movement': description[0].text.split('\n')[1],
            'box': description[1].text.split('\n')[1],
            'year': None if date == '-' else datetime.strptime(date, '%Y'),
            'state': description[3].text.split('\n')[1],
            'reference': description[4].text.split('\n')[1],
            'boxAndPapers': description[5].text.split('\n')[1],
            'place': description[6].text.split('\n')[1],
            'size': description[7].text.split('\n')[1]}


def get_brand_name_from_rating_name(rating_name):
    for brand in LONG_BRANDS:
        if brand in rating_name:
            return brand
    return rating_name.split(' ')[0]
