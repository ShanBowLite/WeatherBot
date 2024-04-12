import pyodbc
import logging
from bd.user import User

#logging.basicConfig(level=logging.ERROR, filename="Errors.log",filemode="w",
#                    format="%(asctime)s %(levelname)s %(message)s")


# Адрес до БД
path_bd = "bd/bd.accdb"
# Подключение к БД
config_connection = "Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:%s;" % (path_bd)
# Добавление пользователя в БД
def add_user(user:User):
    try:
       connect = pyodbc.connect(config_connection)
       cursor = connect.cursor() 

       cursor.execute("insert into Пользователи (FirstName, LastName, ID, City, Status) values (?,?,?,?,?)", user.name, user.lastname, user.id, user.city, user.status)
       connect.commit()

       cursor.close()
       connect.close()
    except pyodbc.Error as err:
        logging.error("Can't connection to DB while try add user", exc_info=True)
        print("Error in connection while try add user")
# Удаление пользователя из БД
def delete_user(id):
    try:
       connect = pyodbc.connect(config_connection)
       cursor = connect.cursor() 

       cursor.execute("delete from Пользователи where id = ?", id)
       connect.commit()

       cursor.close()
       connect.close()
    except pyodbc.Error as err:
        logging.error("Can't connection to DB while try delete user", exc_info=True)
        print("Error in connection while try delete user")


#Поиск пользователя в БД и сбор данных о нём
def search_user(id:int):
    try:
       connect = pyodbc.connect(config_connection)
       cursor = connect.cursor() 

       cursor.execute("select FirstName, LastName, ID, City, Status from Пользователи where ID = ? ", str(id))
       row = cursor.fetchone()
       if row == None:
           cursor.close()
           connect.close()
           return None
       else:
        user = User(row.FirstName, row.LastName, row.ID, row.City, row.Status)

        cursor.close()
        connect.close()

        return user
    except pyodbc.Error as err:
        logging.error("Can't connection to DB while try search user", exc_info=True)
        print("Error in connection while try search user")
#Проверка наличия пользователя в БД
def check_user(id:int):
    try:
       connect = pyodbc.connect(config_connection)
       cursor = connect.cursor() 

       cursor.execute("select ID from Пользователи where ID = ? ", str(id))
       row = cursor.fetchone()
       if row == None:
           cursor.close()
           connect.close()
           return False
       else:

        cursor.close()
        connect.close()

        return True
    except pyodbc.Error as err:
        logging.error("Can't connection to DB while try search user", exc_info=True)
        print("Error in connection while try search user")

#Смена города пользователя в БД
def change_city(user:User):
    try:
       connect = pyodbc.connect(config_connection)
       cursor = connect.cursor() 

       cursor.execute("update Пользователи set City = ? where ID = ? ", str(user.city),  user.id)
       connect.commit()

       cursor.close()
       connect.close()

    except pyodbc.Error as err:
        logging.error("Can't connection to DB while try change city", exc_info=True)
        print("Error in connection while try change city")
#Получение ссылки на сайт gismeteo.ru с городом пользователя
def get_city_link(id:int):
    try:
       connect = pyodbc.connect(config_connection)
       cursor = connect.cursor() 

       cursor.execute("select City from Пользователи where ID = ? ", str(id))
       row = cursor.fetchone()
       if row == None:
           cursor.close()
           connect.close()
           return None
       else:
        cursor.execute("select Link from Города where City = ? ", row.City)
        row = cursor.fetchone()
        if row == None:
            cursor.close()
            connect.close()
            return None
        else:
            cursor.close()
            connect.close()
            return str(row.Link)


    except pyodbc.Error as err:
        logging.error("Can't connection to DB while try get city link", exc_info=True)
        print("Error in connection while try get city link")


