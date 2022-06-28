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

    def add_post(self, title, url, text):
        try:
            query_exist_url = """select count(url) as count from posts
                                 where url like %s;"""
            self.__cursor.execute(query_exist_url, (url,))
            res = self.__cursor.fetchone()
            if res['count'] > 0:
                print("An article with this url exists")
                return False
            date_post = date.today()
            sql = """insert into posts (title, url, text, date)
                      values (%s, %s, %s, %s);"""
            self.__cursor.execute(sql, (title, url, text, date_post))
            self.__db.commit()
        except Exception as _ex:
            print("[INFO] Error adding data in database", _ex)
            return False

        return True

    def get_post(self, alias):
        try:
            sql = "select title, text from posts where url like %s;"
            self.__cursor.execute(sql, (alias,))
            result = self.__cursor.fetchone()
            if result:
                return result
        except Exception as _ex:
            print("[INFO] Error reading from database", _ex)

        return (False, False)

    def get_all_posts(self):
        try:
            sql = "select title, url, text from posts order by date desc;"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
            if result:
                return result
        except Exception as _ex:
            print("[INFO] Error reading from database", _ex)

        return []
