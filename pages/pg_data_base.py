import psycopg2

from pages.locators import LoginLocators, Links, TestData


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


def change_cells(table, column, new_val, where_col="email", where_val=TestData.TEST_USER):
    conn, cursor = db_connect()
    cursor.execute(f'UPDATE public.{table}'
                   f' SET {column} = \'{new_val}\''
                   f' WHERE {where_col} =\'{where_val}\'')
    conn.commit()
    db_disconnect()


def change_stausid(stat=0):
    stat = int(stat)
    assert check_user_exist(), f"Невозможно изменить данные, Пользователя {TestData.TEST_USER} нет в базе"
    change_cells(table="astusers", column="status", new_val=stat)
    change_cells(table="\"AspNetUsers\"", column="\"Status\"", new_val=stat, where_col="\"Email\"")


def change_direct_control(val="True"):
    change_cells(table="systemparameters", column="value", new_val=val, where_col="type", where_val=118)


def change_twofactor(val="true"):
    assert check_user_exist(), f"Невозможно изменить данные, Пользователя {TestData.TEST_USER} нет в базе"
    change_cells(table="astusers", column="twofactorsignneeded", new_val=val)
    change_cells(table='"AspNetUsers"', column='"TwoFactorEnabled"', new_val=val, where_col='"Email"',
                 where_val=TestData.TEST_USER)


change_stausid(0)
change_twofactor("false")
