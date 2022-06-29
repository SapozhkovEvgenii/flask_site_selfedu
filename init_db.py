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
                url varchar(100) not null,
                date date not null);"""
        )

        connection.commit()

    with connection.cursor() as cursor:
        cursor.execute(
            """create table if not exists users (
                id serial primary key,
                name varchar(100) not null,
                email text not null,
                password text not null,
                date_register date not null);"""
        )

        connection.commit()

except Exception as _ex:
    print("[INFO] Error while working with PosgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")
