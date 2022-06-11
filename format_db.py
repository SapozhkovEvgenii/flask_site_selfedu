from psycopg2.extras import DictCursor
from datetime import date


class FormatDataBase():
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor(cursor_factory=DictCursor)

    def get_menu(self):
        sql = """select * from mainmenu;"""
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
            sql = f"""insert into posts (title, text, date)
                      values ('{title}', '{text}', '{date_post}');"""
            self.__cursor.execute(sql)
            self.__db.commit()
        except Exception as _ex:
            print("[INFO] Error adding data in database", _ex)
            return False

        return True
