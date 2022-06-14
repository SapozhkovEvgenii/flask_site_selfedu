from datetime import date
from psycopg2.extras import DictCursor


class FormatDataBase():
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor(cursor_factory=DictCursor)

    def get_menu(self):
        sql = """select * from mainmenu order by id;"""
        try:
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
            if result:
                return result
        except Exception as _ex:
            print("[INFO] Error reading from database", _ex)
        return []

    def add_post(self, title, text):
        try:
            date_post = date.today()
            sql = """insert into posts (title, text, date)
                      values (%s, %s, %s);"""
            self.__cursor.execute(sql, (title, text, date_post))
            self.__db.commit()
        except Exception as _ex:
            print("[INFO] Error adding data in database", _ex)
            return False

        return True

    def get_post(self, id_post):
        try:
            sql = "select title, text from posts where id = %s;"
            self.__cursor.execute(sql, (id_post,))
            result = self.__cursor.fetchone()
            if result:
                return result
        except Exception as _ex:
            print("[INFO] Error reading from database", _ex)

        return (False, False)

    def get_all_posts(self):
        try:
            sql = "select id, title, text from posts order by date desc;"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
            if result:
                return result
        except Exception as _ex:
            print("[INFO] Error reading from database", _ex)

        return []
