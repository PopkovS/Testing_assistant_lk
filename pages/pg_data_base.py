from pages.locators import Links, TestData
import pages.requests
import psycopg2


def db_connect(dbname='assistant_test_corp_linux', user='postgres',
               password='1q2w3e', host='192.168.70.220'):
    conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host=host)
    cursor = conn.cursor()
    return conn, cursor


def db_disconnect():
    conn, cursor = db_connect()
    conn.close()
    cursor.close()


def check_user_exist():
    conn, cursor = db_connect()
    cursor.execute('SELECT email '
                   'FROM public.astusers'
                   f' WHERE email=\'{TestData.TEST_USER}\'')
    records = cursor.fetchall()
    if not records:
        return False
    else:
        return True


def get_id_user():
    conn, cursor = db_connect()
    assert check_user_exist(), f"Невозможно получить id, Пользователя {TestData.TEST_USER} нет в базе"
    cursor.execute('SELECT id '
                   'FROM public.astusers'
                   f' WHERE email=\'{TestData.TEST_USER}\'')
    id_user = cursor.fetchall()[0][0]
    return id_user


def edit_stausid(stat=0):
    conn, cursor = db_connect()

    assert check_user_exist(), f"Невозможно получить id, Пользователя {TestData.TEST_USER} нет в базе"
    cursor.execute('UPDATE public.astusers '
                   f'SET status = \'{stat}\''
                   f' WHERE email=\'{TestData.TEST_USER}\'')

    cursor.execute('UPDATE public."AspNetUsers"'
                   f'SET "Status" = {stat}'
                   f' WHERE "Email"=\'{TestData.TEST_USER}\'')
    conn.commit()
    db_disconnect()


edit_stausid(2)
# print(edit_stausid())
