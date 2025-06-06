# Сравниваем вакансии программистов

Программа позвояет сравнить зарплаты программистов, производя поиск по определенным языкам программирования.
В данно примере анализируются текущие вакансии с сайтов [*HeadHunter*](https://hh.ru/) и [SuperJob](https://www.superjob.ru/) г. Москвы с указанной заработной платой.

## Как установить 

+ Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
  ```
  pip install -r requirements.txt
  ```

## Как пользоваться

Для обработки вакансий *HeadHunter* используем [*HH API*](https://dev.hh.ru/) - регистраци не требуется  

Для обработки вакансий *SuperJob* используем [*SuperJob API*](https://api.superjob.ru/) - необходимой пройти простую регистрацию и получить API-ключ
  >Ключ помещаем в **.env** файл  
  >используем:
  ```python
  import os
  from dotenv import load_dotenv
  load_dotenv()
  superjob_api_token = os.getenv("SUPERJOB_API_TOKEN")
  ```

### Пример использования 
1. Запускаем программу в командной строке:
   ```
   python main.py
   ```
2. Пример результата:
```
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 256              | 236                 | 216974           |
| Java                  | 136              | 128                 | 224552           |
| Javascript            | 485              | 433                 | 180617           |
| Ruby                  | 15               | 15                  | 245624           |
| C                     | 396              | 386                 | 226793           |
| Go                    | 81               | 72                  | 264215           |
| C++                   | 208              | 201                 | 228678           |
+-----------------------+------------------+---------------------+------------------+

+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 6                | 3                   | 158000           |
| Javascript            | 4                | 1                   | 180000           |
| C                     | 6                | 3                   | 248000           |
| C++                   | 9                | 4                   | 223500           |
+-----------------------+------------------+---------------------+------------------+
```
## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.
