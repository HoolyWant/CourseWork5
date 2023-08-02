import re
from requests import get
from json import loads


class HHEmployers:
    """
    Класс для работы с API hh.ru
    Хранящий в своих атрибутах информацию
    о работадателях и их вакансиях
    """
    employers_info = []
    vacancies_info = []

    def __init__(self, employer_ids_list):
        self.employer_ids_list = employer_ids_list

    def get_hh_employers(self) -> None:
        """
        Парсит данные о работадателях
        и сохраняет в список employers_info
        """
        for employer_id in self.employer_ids_list:
            json_response = get(f'https://api.hh.ru/employers/{employer_id}').text
            response = loads(json_response)
            name = self.cleanhtml(response['name']).replace(u'\xa0', ' ')
            description = self.cleanhtml(response['description']).replace(u'\xa0', ' ')
            site_url = response['site_url']
            url = response['alternate_url']
            vacancies_url = response['vacancies_url']
            employer_info = {
                             'name': name,
                             'description': description,
                             'url': url,
                             'site_url': site_url,
                             'vacancies_url': vacancies_url
            }
            self.employers_info.append(employer_info)

    @staticmethod
    def cleanhtml(string: str) -> str:
        """
        Статический метод для очистки описаний
        работадателей и не только от html-тегов
        :param string:
        :return cleantext:
        """
        CLEANR = re.compile('<.*?>')
        cleantext = re.sub(CLEANR, '', string)
        return cleantext

    def get_vacancies(self):
        """
        Парсит данные о вакансиях работадателей
        и сохраняет в список vacancies_info
        """
        for item in self.employers_info:
            json_response = get(item['vacancies_url']).text
            vacancies = loads(json_response)['items']
            item_list = []
            for vacancy in vacancies:
                clear_dict = {
                              'name': vacancy['name'],
                              'url': vacancy['alternate_url'],
                }
                try:
                    pay_from = str(vacancy['salary']['from'])
                    pay_to = str(vacancy['salary']['to'])
                    if pay_to == 'None':
                        salary = pay_from
                    elif pay_from == 'None':
                        salary = pay_to
                    else:
                        salary = pay_to
                except TypeError:
                    salary = None
                clear_dict['salary'] = salary
                item_list.append(clear_dict)
            vacancy_dict = {item['name']: item_list}
            self.vacancies_info.append(vacancy_dict)



