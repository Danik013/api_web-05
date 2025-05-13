import os
import time
import requests
from terminaltables import AsciiTable
from dotenv import load_dotenv


HH_AREA_MOSCOW = "1"
HH_PROFESSION_PROGRAMMER = "96"

SJ_AREA_MOSCOW = 4
SJ_PROFESSION_PROGRAMMER = 48
SJ_ALLTIME_SEARCH = 0


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from:
        return salary_from * 1.2
    if salary_to:
        return salary_to * 0.8


def get_hh_salary_statistics(programming_language):
    page_number = 0
    total_salary = 0
    salary_count = 0

    while True:
        url = "https://api.hh.ru/vacancies"
        params = {
            "area": HH_AREA_MOSCOW,
            "text": programming_language,
            "professional_role": HH_PROFESSION_PROGRAMMER,
            "period": "30",
            "page": f"{page_number}",
            "per_page": "20",
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        time.sleep(0.5)
        api_hh_response = response.json()

        for vacancy in api_hh_response["items"]:
            if not vacancy["salary"] or vacancy["salary"]["currency"] != "RUR":
                continue
            expected_salary = predict_salary(vacancy["salary"]["from"], vacancy["salary"]["to"])
            total_salary += expected_salary
            salary_count += 1

        if page_number >= api_hh_response["pages"]:
            break
        page_number +=1

    try:
        average_salary = int(total_salary / salary_count)
    except ZeroDivisionError:
        average_salary = 0

    return {
        "vacancies_found": api_hh_response["found"],
        "vacancies_processed": salary_count,
        "average_salary": average_salary,
    }


def get_sj_salary_statistics(programing_language, superjob_api_token):
    page_number = 0
    total_salary = 0
    salary_count = 0

    while True:
        url = "https://api.superjob.ru/2.0/vacancies/"
        params = {
            "period": SJ_ALLTIME_SEARCH,
            "keywords": programing_language,
            "catalogues": SJ_PROFESSION_PROGRAMMER,
            "town": SJ_AREA_MOSCOW,
            "count": 20,
            "page": page_number,
        }
        headers = {"X-Api-App-Id": superjob_api_token}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        api_sj_response = response.json()

        for vacancy in api_sj_response["objects"]:
            if vacancy["currency"] != 'rub':
                continue
            expected_salary = predict_salary(vacancy["payment_from"], vacancy["payment_to"])
            if not expected_salary:
                continue
            total_salary += expected_salary
            salary_count += 1

        if not api_sj_response["more"]:
            break

        page_number += 1

    try:
        average_salary = int(total_salary / salary_count)
    except ZeroDivisionError:
        average_salary = 0

    return {
        "vacancies_found": api_sj_response["total"],
        "vacancies_processed": salary_count,
        "average_salary": average_salary,
    }

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
    title_hh = "HeadHunter Moscow"
    title_sj = "SuperJob Moscow"

    for programming_language in programming_languages:
        salary_analysis_hh[programming_language] = get_hh_salary_statistics(programming_language)

        salary_analysis_sj[programming_language] = get_sj_salary_statistics(programming_language, superjob_api_token)

    print(get_table(salary_analysis_hh, title_hh))
    print()
    print(get_table(salary_analysis_sj, title_sj))


if __name__ == "__main__":
    main()
