-- Получает список всех компаний и количество вакансий у каждой компании.
SELECT employer_name, COUNT(*)
FROM vacancies
GROUP BY employer_name
ORDER BY COUNT(*) DESC;

-- Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
SELECT * FROM vacancies;

-- Получает среднюю зарплату по вакансиям.
SELECT AVG(salary) FROM vacancies;

-- Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
SELECT * FROM vacancies
WHERE salary > (SELECT AVG(salary) FROM vacancies);

-- Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
SELECT * FROM vacancies
WHERE vacancy_name LIKE '%Python%'
OR vacancy_name LIKE 'Python%'
OR vacancy_name LIKE '%Python'
