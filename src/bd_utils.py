import psycopg2


def create_database(database_name: str, params: dict) -> None:
    """
    Создает базу данных с нуля и создает
    в ней таблицы для работадателей и их вакансий
    :param database_name: имя базы данных
    :param params: параметры для подключения к базе
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(f"DROP DATABASE {database_name}")
    except psycopg2.errors.InvalidCatalogName:
        pass
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute('''
                CREATE TABLE employers (
                        employer_name varchar(50) PRIMARY KEY NOT NULL,
                        employer_url varchar(100) NOT NULL,
                        site_url varchar(100),
                        vacancies_url varchar(100),
                        description varchar
                )
            ''')

    with conn.cursor() as cur:
        cur.execute('''
                CREATE TABLE vacancies (
                        vacancy_id serial PRIMARY KEY,
                        vacancy_name varchar(100) NOT NULL,
                        salary INT,
                        vacancy_url varchar(100) NOT NULL,
                        employer_name varchar(100) REFERENCES employers(employer_name)
                )
        ''')
    conn.commit()
    conn.close()


def fill_employer_table(database_name: str, params: dict, data: list[dict[str, any]]) -> None:
    """
    Заполняет таблицу с работадателями
    по заданному списку словарей data
    """
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for item in data:
            cur.execute(
                    '''
                    INSERT INTO employers (employer_name, description, employer_url, site_url, vacancies_url)
                    VALUES (%s, %s, %s, %s, %s)
                    ''',
                    (item['name'], item['description'], item['url'], item['site_url'], item['vacancies_url'])
            )
    conn.commit()
    conn.close()


def fill_vacancy_table(database_name: str, params: dict, data: list[dict[str, any]]) -> None:
    """
    Заполняет таблицу с вакансиями
    по заданному списку словарей data
    """
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for item in data:
            for key, value in item.items():
                for vacancy in value:
                    cur.execute(
                            '''
                            INSERT INTO vacancies (vacancy_name, vacancy_url, salary, employer_name)
                            VALUES (%s, %s, %s, %s)
                            ''',
                            (vacancy['name'], vacancy['url'], vacancy['salary'], key)
                    )
    conn.commit()
    conn.close()

