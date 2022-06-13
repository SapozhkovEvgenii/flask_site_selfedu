from datetime import date


class FormatDataBase():
    def __init__(self, db, type_data=None):
        self.__db = db
        self.type_data = type_data
        self.__cursor = db.cursor(cursor_factory=self.type_data)

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

    def get_post(self, id_post):
        try:
            sql = f"select title, text from posts where id = {id_post};"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchone()
            return result
        except Exception as _ex:
            print("[INFO] Error reading from database", _ex)

        return (False, False)
