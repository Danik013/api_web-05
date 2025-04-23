import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36", 
    "X-Amzn-Trace-Id": "Root=1-67cdd7a5-7dbb0568305856bc19b4e836"}

url = "https://api.hh.ru/vacancies"
params = {
	"area": "1",
	"text": {"Python"},
	"professional_role": "96",
	"search_period": "0"
}

response = requests.get(url, params=params)
response_elements = response.json()

print(response.url)