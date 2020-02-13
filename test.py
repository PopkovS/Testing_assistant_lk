from time import sleep

import pytest
from selenium.webdriver import DesiredCapabilities

from pages import requests
from pages.locators import Links, TestData
import pages.requests
import psycopg2

# requests.send_pack("login")


def db_connect():
    global cursor
    global conn
    conn = psycopg2.connect(dbname='assistant_test_corp_linux', user='postgres',
                            password='1q2w3e', host='192.168.70.220')
    cursor = conn.cursor()


def check_user_exist():
    db_connect()
    cursor.execute('SELECT email '
                   'FROM public.astusers'
                   f' WHERE email=\'{TestData.TEST_USER}\'')
    records = cursor.fetchall()
    if not records:
        return False
    else:
        return True


def get_id_user():
    db_connect()
    assert check_user_exist(), f"Невозможно получить id, Пользователя {TestData.TEST_USER} нет в базе"
    cursor.execute('SELECT id '
                   'FROM public.astusers'
                   f' WHERE email=\'{TestData.TEST_USER}\'')
    id_user = cursor.fetchall()[0][0]
    return id_user


def edit_stausid(stat):
    db_connect()
    assert check_user_exist(), f"Невозможно получить id, Пользователя {TestData.TEST_USER} нет в базе"
    # cursor.execute('UPDATE public.astusers '
    #                f'SET status = \'{stat}\''
    #                f' WHERE email=\'{TestData.TEST_USER}\'')
    # conn.commit()

    cursor.execute('UPDATE public."AspNetUsers"'
                   f'SET \"Status\" = {stat}'
                   f' WHERE \"Email\"=\'{TestData.TEST_USER}\'')
    conn.commit()
    # id_user = cursor.fetchall()[0][0]
    # return id_user


edit_stausid(0)
# print(edit_stausid())
