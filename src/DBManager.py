import psycopg2


class DBManager:
    """
    Класс для работы с базой данных
    """
    def __init__(self, database_name: str, params: dict):
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self) -> None:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                '''
                SELECT employer_name, COUNT(*)
                FROM vacancies
                GROUP BY employer_name
                ORDER BY COUNT(*) DESC
                '''
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)
            print('\n')
        conn.close()

    def get_all_vacancies(self) -> None:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                '''
                SELECT * FROM vacancies
                '''
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)
            print('\n')
        conn.close()

    def get_avg_salary(self) -> None:
        """
        Получает среднюю зарплату по вакансиям.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                '''
                SELECT AVG(salary) FROM vacancies
                '''
            )
            row = str(cur.fetchall()[0])[10:-4]
            print(f'Средняя зарплата по всем вакансиям: {round(float(row))}\n')
        conn.close()

    def get_vacancies_with_higher_salary(self) -> None:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                '''
                SELECT * FROM vacancies
                WHERE salary > (SELECT AVG(salary) FROM vacancies)
                '''
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)
            print('\n')
        conn.close()

    def get_vacancies_with_keyword(self) -> None:
        """
        Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                '''
                SELECT * FROM vacancies
                '''
            )
            rows = cur.fetchall()
            user_input = input('Введите значение, по которому вы '
                               'хотите произвести поиск по вакансиям:\n')
            for row in rows:
                if user_input.lower() in row[1].lower():
                    print(row)
            print('\n')
        conn.close()


