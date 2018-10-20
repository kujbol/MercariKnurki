import csv
import os

import requests
from bs4 import BeautifulSoup


great = 'https://www.mercari.com/u/{user_id}/reviews/great/'
good = 'https://www.mercari.com/u/{user_id}/reviews/good/'
bad = 'https://www.mercari.com/u/{user_id}/reviews/poor/'

reviews_urls = {2: great, 1: good, 0: bad}

visited = []
to_visit = ['795606679']


def gather_user(user_id, dict_writer):
    for rate, url in reviews_urls.items():
        url = url.format(user_id=user_id)
        get_data(rate, url=url, user_id=user_id, dict_writer=dict_writer)


def scrap_data(data, user_id, rate_value, dict_writer):
    soup = BeautifulSoup(data, 'html.parser')
    reviews = soup.find_all("div", {"class": 'review-item'})

    if len(reviews) == 0:
        raise StopIteration

    for review in reviews:
        reviewer_id = review.a.get('href', '').replace('/', '').replace('u', '')
        is_buyer = 'Buyer' in review.div.a.div.string
        is_seller = 'Seller' in review.div.a.div.string
        date = review.div.time.string.strip()

        if reviewer_id not in visited and reviewer_id not in to_visit:
            to_visit.append(reviewer_id)

        if is_buyer is False and is_seller is False or (is_buyer and is_seller):
            print('invalid review')
            continue

        if is_buyer:
            dict_writer.writerow({
                'buyer': reviewer_id,
                'seller': user_id,
                'rate': rate_value,
                'date': date,
            })

        if is_seller:
            dict_writer.writerow({
                'buyer': user_id,
                'seller': reviewer_id,
                'date': date,
                'rate': rate_value
            })

    next_url = 'https://www.mercari.com' + soup.find('li', {'class': 'pager-next pager-cell'}).a.get('href')
    return next_url


def get_data(rate, user_id, url, dict_writer):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    try:
        content = requests.get(url, headers=headers).content
        next_url = scrap_data(content, user_id=user_id, rate_value=rate, dict_writer=dict_writer)
        if next_url:
            get_data(rate, user_id=user_id, url=next_url, dict_writer=dict_writer)
    except StopIteration:
        return


if os.path.exists('visited.txt'):
    with open('visited.txt') as visited_file:
        visited = visited_file.read().split(',')


if os.path.exists('to_visit.txt'):
    with open('to_visit.txt') as to_visit_file:
        to_visit = to_visit_file.read().split(',')


with open('scrapped.csv', 'a+') as scrape_file:
    dict_writer = csv.DictWriter(scrape_file, ['buyer', 'seller', 'rate', 'date'])
    while to_visit:
        user_id = to_visit.pop()
        visited.append(user_id)
        print(f'getting user{user_id}')
        gather_user(user_id, dict_writer)

        scrape_file.flush()

        with open('visited.txt', 'w+') as visited_file:
            visited_file.write(','.join(visited))

        with open('to_visit.txt', 'w+') as to_visit_file:
            to_visit_file.write(','.join(to_visit))
