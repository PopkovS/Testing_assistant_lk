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


def check_user_exist(user=TestData.USER_NORMAL_EMAIL):
    conn, cursor = db_connect()
    cursor.execute('SELECT email '
                   'FROM public.astusers'
                   f' WHERE email=\'{user}\'')
    # print(cursor.fetchall())
    astusers = bool(cursor.fetchall())
    cursor.execute(f'SELECT "Email" '
                   f'FROM public."AspNetUsers" '
                   f'WHERE "Email" = \'{user}\'')
    # print(cursor.fetchall())
    aspNetUsers = bool(cursor.fetchall())
    assert astusers == aspNetUsers, f"Ответ от таблиц отличается. " \
                                    f"astusers = '{astusers}', AspNetUsers = '{aspNetUsers}'"
    return astusers and aspNetUsers


def get_id_user(user=TestData.USER_NORMAL_EMAIL):
    conn, cursor = db_connect()
    assert check_user_exist(user), f"Невозможно получить id, Пользователя {user} нет в базе"
    cursor.execute('SELECT id '
                   'FROM public.astusers'
                   f' WHERE email=\'{user}\'')
    result = cursor.fetchall()
    # print(result)
    if result:
        return result[0][0]


def change_cells(table, column, new_val, where_col="email", where_val=TestData.USER_NORMAL_EMAIL):
    conn, cursor = db_connect()
    cursor.execute(f'UPDATE public.{table}'
                   f' SET {column} = \'{new_val}\''
                   f' WHERE {where_col} =\'{where_val}\'')
    conn.commit()
    db_disconnect()


def get_cell(search_row="id", table="astusers", where_col="email", val=TestData.USER_NORMAL_EMAIL):
    conn, cursor = db_connect()
    cursor.execute(f'SELECT {search_row} '
                   f'FROM public.{table}'
                   f' WHERE {where_col}=\'{val}\'')
    cell = cursor.fetchall()[0][0]
    return cell


def delete_row(table="astclientdevices", column="title", val="'Наименование'"):
    conn, cursor = db_connect()
    cursor.execute(f"DELETE FROM public.{table} WHERE {column} ={val}")
    conn.commit()
    db_disconnect()


def change_stausid(stat=0, user=TestData.USER_NORMAL_EMAIL):
    stat = int(stat)
    assert check_user_exist(user), f"Невозможно изменить данные, Пользователя {user} нет в базе"
    change_cells(table="astusers", column="status", new_val=stat, where_val=user)
    change_cells(table="\"AspNetUsers\"", column="\"Status\"", new_val=stat, where_col="\"Email\"", where_val=user )


def change_direct_control(val="True"):
    change_cells(table="systemparameters", column="value", new_val=val, where_col="type", where_val=118)


def change_auth_ad(val="True"):
    change_cells(table="systemparameters", column="value", new_val=val, where_col="type", where_val=135)
    if val == "True":
        change_cells(table="systemparameters", column="value", new_val="test.local;safib.ru;test2.test1.local",
                     where_col="type", where_val=136)
    else:
        change_cells(table="systemparameters", column="value", new_val="", where_col="type", where_val=136)


def change_twofactor(val="true", user=TestData.USER_NORMAL_EMAIL):
    assert check_user_exist(), f"Невозможно изменить данные, Пользователя {user} нет в базе"
    change_cells(table="astusers", column="twofactorsignneeded", new_val=val)
    change_cells(table='"AspNetUsers"', column='"TwoFactorEnabled"', new_val=val, where_col='"Email"',
                 where_val=user)


def del_new_user(user=TestData.NEW_USER_EMAIL):
    assert check_user_exist(user), f"Пользователя '{user}' нет в бд, удаление не возможно"
    id = get_id_user(user=f'{user}')
    delete_row(table='astclientdevicegroups', column='userid',
               val=(f"'{id}'"))
    delete_row(table='"AspNetUsers"', column='"Email"', val=(f"'{user}'"))
    delete_row(table='astusers', column='email', val=(f"'{user}'"))


# print(check_user_exist("testassistantNewUser@mailforspam.com"))
# change_direct_control(val="False")
# del_new_user("testassistnewuser2@mailforspam.com")
# del_new_user("testassistNewUser@test.local")
# del_new_user(user=TestData.NEW_USER.replace("ser","ser2").lower())
# print(check_user_exist(user="testassistknewuser2@mailforspam.com"))
# change_stausid(stat=2, user="testassistnewuser2@mailforspam.com")
