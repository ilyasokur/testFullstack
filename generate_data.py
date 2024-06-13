'''

CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    birth_date DATE NOT NULL,
    inn VARCHAR(12) NOT NULL,
    responsible_full_name VARCHAR(150) NOT NULL,
    status VARCHAR(20) DEFAULT 'Не в работе'
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(150) NOT NULL,
    login VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL
);
'''


import sqlite3
from faker import Faker
import random

fake = Faker('ru_RU')

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Генерация пользователей
user_data = []
for _ in range(10):
    full_name = fake.name()
    login = fake.user_name()
    password = fake.password()
    user_data.append((full_name, login, password))
cursor.executemany("INSERT INTO users (full_name, login, password) VALUES (?, ?, ?)", user_data)

# Получаем все сгенерированные имена пользователей
cursor.execute("SELECT full_name FROM users")
user_full_names = cursor.fetchall()

# Генерация клиентов
client_data = []
for _ in range(50):
    account_number = fake.iban()
    last_name = fake.last_name()
    first_name = fake.first_name()
    middle_name = fake.middle_name()
    birth_date = fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=90)
    inn = fake.ssn()
    responsible_full_name = random.choice(user_full_names)[0]
    status = 'Не в работе'
    client_data.append((account_number, last_name, first_name, middle_name, birth_date, inn, responsible_full_name, status))
cursor.executemany("INSERT INTO clients (account_number, last_name, first_name, middle_name, birth_date, inn, responsible_full_name, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", client_data)

conn.commit()
conn.close()



