from datetime import date
from psycopg2.extras import DictCursor
from flask import url_for, flash
import re


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
            base = url_for('static', filename='images_html')
            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<path>.+?)(?P=quote)>",
                          "\\g<tag>" + base + r"/\g<path>>", text)
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

    def add_user(self, name, email, hash_psw):
        try:
            query_exist_email = """select count(email) as count from users
                                 where email like %s;"""
            self.__cursor.execute(query_exist_email, (email,))
            res = self.__cursor.fetchone()
            if res['count'] > 0:
                flash("User with this email exist", category='error')
                print('[INFO] Error adding data in database')
                return False

            date_user = date.today()
            sql = """insert into users (name, email, password, date_register)
                      values (%s, %s, %s, %s);"""
            self.__cursor.execute(sql, (name, email, hash_psw, date_user))
            self.__db.commit()
        except Exception as _ex:
            print("[INFO] Error adding data in database", _ex)
            return False

        return True

    def get_user(self, user_id):
        try:
            query_get_user = "select * from users where id = %s limit 1"
            self.__cursor.execute(query_get_user, (user_id,))
            res = self.__cursor.fetchone()
            if not res:
                print("User is not found")
                return False

            return res
        except Exception as _ex:
            print("[INFO] Error reading from database", _ex)

        return False

    def get_user_by_email(self, email):
        try:
            query_user_email = "select * from users where email = %s limit 1"
            self.__cursor.execute(query_user_email, (email,))
            res = self.__cursor.fetchone()
            if not res:
                print("User is not found")
                return False

            return res
        except Exception as _ex:
            print("[INFO] Error reading from database", _ex)

        return False
