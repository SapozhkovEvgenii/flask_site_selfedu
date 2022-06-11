import psycopg2
from config import DB_PASSWORD, DB_USERNAME


try:
    connection = psycopg2.connect(
        host='localhost',
        database='flask_selfedu',
        user=DB_USERNAME,
        password=DB_PASSWORD
    )

    with connection.cursor() as cursor:
        cursor.execute(
            """create table if not exists mainmenu (
                id serial primary key,
                title varchar(100) not null,
                url varchar(50) not null);"""
        )

    with connection.cursor() as cursor:
        cursor.execute(
            """create table if not exists posts (
                id serial primary key,
                title varchar(100) not null,
                text text not null,
                date date not null);"""
        )

        connection.commit()
        print("[INFO] create table")

except Exception as _ex:
    print("[INFO] Error while working with PosgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")
