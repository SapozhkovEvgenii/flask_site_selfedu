create table if not exists mainmenu (
    id serial primary key,
    title varchar(100) not null,
    url varchar(50) not null);

insert into mainmenu (title, url)
values
    ('Add post', 'add_post'),
    ('Home', 'index'),
    ('Login', 'login'),
    ('Registration', 'register');

create table if not exists posts (
    id serial primary key,
    title varchar(100) not null,
    text text not null,
    url varchar(100) not null,
    date date not null);

insert into posts (title, text, url, date)
values
    ('About Flask', 'Flask  is a framework for creating web applications in the Python programming language using the Werkzeug toolkit and the Jinja2 templating engine . Belongs to the category of so-called microframeworks [en]  - minimalistic web application frameworks that deliberately provide only the most basic features.

Installation via the PyPI package manager is supported , version 1.0 is compatible with Python 2.7, Python 3.3 and above.

The creator and main author is the Austrian programmer Armin Ronacher , who began work on the project in 2010.', 'about-flask', '2022-09-15'),
    ('About Python', 'Python is a high-level general-purpose programming language with dynamic strong typing and automatic memory management [25] [26] , focused on increasing developer productivity, code readability and quality, as well as ensuring the portability of programs written on it [27] . The language is completely object-oriented  in the sense that everything is an object [25]. An unusual feature of the language is whitespace indentation of blocks of code [28] . The syntax of the core language is minimalistic, due to which in practice there is rarely a need to refer to the documentation [27] . The language itself is known as interpreted and is used, among other things, for writing scripts [25] . The disadvantages of the language are often lower speed and higher memory consumption of programs written in it compared to similar code written in compiled languages such as C or C++', 'about-python', '2022-09-15');

create table if not exists users (
    id serial primary key,
    name varchar(100) not null,
    email text not null,
    password text not null,
    date_register date not null,
    avatar text);
