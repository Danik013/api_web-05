import os
import requests
from terminaltables import AsciiTable
from dotenv import load_dotenv


def predict_salary(salary_from, salary_to):
    if (salary_from == 0 or salary_from is None) and (salary_to == 0 or salary_to is None):
        return None
    if salary_from == 0 or salary_from is None:
        return salary_to * 0.8
    if salary_to == 0 or salary_to is None:
        return salary_from * 1.2

    return (salary_from + salary_to) / 2


def predict_rub_salary_hh(vacancy):
    if vacancy["salary"]["currency"] == 'RUR':
        salary_from = vacancy["salary"]["from"]
        salary_to = vacancy["salary"]["to"]
        average_salary = predict_salary(salary_from, salary_to)
        return average_salary

    return None


def get_hh_salary_statistics(programming_language):
    page_number = 0
    total_salary = 0
    count_salary = 0

    while True:
        url = "https://api.hh.ru/vacancies"
        params = {
            "area": "1",
            "text": programming_language,
            "professional_role": "96",
            "period": "30",
            "page": f"{page_number}",
            "per_page": "20",
            "only_with_salary": "true",
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        for vacancy in response.json()["items"]:
            expected_salary = predict_rub_salary_hh(vacancy)
            if expected_salary is None:
                continue
            total_salary += expected_salary
            count_salary += 1

        vacancy_statistics = {
            "vacancies_found": response.json()["found"],
            "vacancies_processed": count_salary,
            "average_salary": int(total_salary / count_salary),
        }
        if page_number >= response.json()["pages"]:
            break

        page_number +=1

    return vacancy_statistics


def predict_rub_salary_sj(vacancy):
    if vacancy["currency"] == 'rub':
        salary_from = vacancy["payment_from"]
        salary_to = vacancy["payment_to"]
        average_salary = predict_salary(salary_from, salary_to)
        return average_salary

    return None


def get_sj_salary_statistics(programing_language, superjob_api_token):
    page_number = 0
    total_salary = 0
    count_salary = 0

    while True:
        url = "https://api.superjob.ru/2.0/vacancies/"
        params = {
            "period": 0,
            "keywords": programing_language,
            "catalogues": 48,
            "town": 4,
            "count": 20,
            "page": page_number,
        }
        headers = {"X-Api-App-Id": superjob_api_token}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        for vacancy in response.json()["objects"]:
            if vacancy["currency"] == 'rub':
                expected_salary = predict_rub_salary_sj(vacancy)
                if expected_salary is None:
                    continue
                total_salary += expected_salary
                count_salary += 1

        if total_salary == 0 or count_salary == 0:
            return None
        vacancy_statistics_sj = {
            "vacancies_found": response.json()["total"],
            "vacancies_processed": count_salary,
            "average_salary": int(total_salary / count_salary),
        }
        if not response.json()["more"]:
            break

        page_number += 1

    return vacancy_statistics_sj


def get_table(salary_analysis, title):
    column_names = [
        "Язык программирования",
        "Вакансий найдено",
        "Вакансий обработано",
        "Средняя зарплата",
    ]
    columns_table = [column_names]
    for language, stats in salary_analysis.items():
        line = [
            language,
            stats["vacancies_found"],
            stats["vacancies_processed"],
            stats["average_salary"],
        ]
        columns_table.append(line)

    table = AsciiTable(columns_table, title)

    return table.table


def main():
    load_dotenv()
    superjob_api_token = os.getenv("SUPERJOB_API_TOKEN")

    programming_languages = [
        "Python", 
        "Java", 
        "Javascript",
        "Ruby",
        "C",
        "Go",
        "C++",
    ]

    salary_analysis_hh = {}
    salary_analysis_sj = {}

    for programming_language in programming_languages:
        title_hh = "HeadHunter Moscow"
        salary_analysis_hh[programming_language] = get_hh_salary_statistics(programming_language)

        title_sj = "SuperJob Moscow"
        if get_sj_salary_statistics(programming_language, superjob_api_token):
            salary_analysis_sj[programming_language] = get_sj_salary_statistics(programming_language, superjob_api_token)
        else:
            continue

    print(get_table(salary_analysis_hh, title_hh))
    print()
    print(get_table(salary_analysis_sj, title_sj))


if __name__ == "__main__":
    main()
