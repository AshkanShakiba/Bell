import time
import random
import requests
from environs import Env
from threading import Thread
from datetime import datetime
from django.test import TestCase

env = Env()
env.read_env()

url = env.str("DEPLOYED_URL")
username = env.str("DEPLOYED_USERNAME")
password = env.str("DEPLOYED_PASSWORD")


def login():
    login_response = requests.post(
        url=url + "api/v1/auth/login/",
        json={"username": username, "password": password}
    )
    authorization_token = login_response.json()["key"]
    return authorization_token


def get_credit(authorization_token):
    credit_response = requests.get(
        url=url + "api/v1/credit/",
        headers={"Authorization": "Token " + authorization_token}
    )
    credit = credit_response.json()["credit"]
    return credit


def post_increase(authorization_token, amount):
    increase_response = requests.post(
        url=url + "api/v1/increase/",
        headers={"Authorization": "Token " + authorization_token},
        json={"amount": amount},
    )
    if increase_response.status_code != 200:
        raise Exception("increase failed")


def post_sale(authorization_token, amount, phone_number, response_times=None):
    t1 = datetime.now()
    increase_response = requests.post(
        url=url + "api/v1/sale/",
        headers={"Authorization": "Token " + authorization_token},
        json={"amount": amount, "phone_number": phone_number},
    )
    t2 = datetime.now()
    if increase_response.status_code != 200:
        raise Exception("sale failed")
    if response_times is not None:
        response_times.append((t2 - t1).total_seconds())


class AcidTest(TestCase):
    def test_acid_transactions(self):
        authorization_token = login()

        initial_credit = get_credit(authorization_token)

        increase_amounts = []
        increase_threads = []
        for i in range(0, 10):
            increase_amount = random.randrange(1000, 10000, 1)
            increase_threads.append(Thread(target=post_increase, args=(authorization_token, increase_amount)))
            increase_amounts.append(increase_amount)

        for thread in increase_threads:
            thread.start()

        for thread in increase_threads:
            thread.join()

        self.assertEqual(get_credit(authorization_token), initial_credit + sum(increase_amounts))

        sale_amounts = []
        sale_threads = []
        for i in range(0, 1000):
            sale_amount = random.randrange(1, 100, 1)
            sale_threads.append(Thread(target=post_sale, args=(authorization_token, sale_amount, "09123456789")))
            sale_amounts.append(sale_amount)

        for thread in sale_threads:
            thread.start()

        for thread in sale_threads:
            thread.join()

        self.assertEqual(get_credit(authorization_token), initial_credit + sum(increase_amounts) - sum(sale_amounts))

    def test_response_time(self):
        authorization_token = login()

        post_increase(authorization_token, 1000)
        time.sleep(1)

        t1 = datetime.now()
        post_sale(authorization_token, 1, "09123456789")
        t2 = datetime.now()

        print("low traffic sale response time:", (t2 - t1).total_seconds(), "s")

        sale_threads = []
        response_times = []
        for i in range(0, 20):
            sale_threads.append(Thread(target=post_sale, args=(authorization_token, 1, "09123456789", response_times)))

        for thread in sale_threads:
            thread.start()

        for thread in sale_threads:
            thread.join()

        print("high traffic average sale response time:", sum(response_times) / len(response_times), "s")
