# Здесь логика операций с БД
from dotenv import load_dotenv
import os
import psycopg2


class DataBase:
    """Класс для работы с базой данных."""

    def __init__(self):
        """Подключается к БД и создает таблицу, если ее нет."""
        try:
            load_dotenv()
            self.connection = psycopg2.connect(
                host=os.getenv('HOST'),
                user=os.getenv('USER'),
                password=os.getenv('PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            self.connection.autocommit = True
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT version();"
                )
                print(f'Server version: {cursor.fetchone()}')
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users(
                        name TEXT,
                        surname TEXT,
                        age INTEGER,
                        tg_id INTEGER
                    );"""
                )
        except Exception as ex:
            print("[INFO] Error", ex)

    def add_new_user(self, name, surname, age, tg_id):
        """Добавляет нового пользователя в БД."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users(
                        name,
                        surname,
                        age,
                        tg_id
                    ) values (%s, %s, %s, %s);
                    """, (name, surname, age, tg_id)
                )
            self.connection.commit()
        except Exception as ex:
            print("[INFO] Error", ex)

    def check_if_user_exists(self, tg_id):
        """Проверяет, есть ли такой пользователь в БД."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT tg_id FROM users WHERE tg_id = %s;
                    """, (tg_id,)
                )
                result = cursor.fetchone()
                return result is not None
        except Exception as ex:
            print("[INFO] Error", ex)

    def close_connection(self):
        """Закрывает связь с БД."""
        if self.connection:
            self.connection.close()
