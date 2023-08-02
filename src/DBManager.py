import psycopg2


class DBManager:
    def __init__(self, database_name: str, params: dict):
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
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
        conn.close()

    def get_all_vacancies(self):
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
        conn.close()

    def get_avg_salary(self):
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                '''
                SELECT AVG(salary) FROM vacancies
                '''
            )
            row = str(cur.fetchall()[0])[10:-4]
            print(f'\nСредняя зарплата по всем вакансиям: {round(float(row))}\n')
        conn.close()

    def get_vacancies_with_higher_salary(self):
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
        conn.close()

    def get_vacancies_with_keyword(self):
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                '''
                SELECT * FROM vacancies
                WHERE vacancy_name LIKE '%python%' 
                OR vacancy_name LIKE 'Python%' 
                OR vacancy_name LIKE '%python'
                OR vacancy_name LIKE '%Python%'
                OR vacancy_name LIKE '%Python'
                '''
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)
        conn.close()


