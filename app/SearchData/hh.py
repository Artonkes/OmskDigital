import requests

def vacancies(keyword, salary):
    try:
        params = {
            "User-Agent": "Mozilla / 5.0(Macintosh; Intel MacOS X 10.15 ;rv: 140.0) Gecko/20100101 Firefox/140.0",
            "text": keyword,
            # "area": ,
            "salary": salary,
            "experience": None
        }

        url = requests.get("https://api.hh.ru/vacancies", params=params)

        data = url.json()

        # for vacancies_i in data["items"]:
        #     print(f"name: {vacancies_i['name']}")
        #     print(f"url: {vacancies_i['alternate_url']}")
        #     print(f"зп: {vacancies_i['salary']}")
        #     print(f"город: {vacancies_i['area']["name"]}")
        #     print(f"опыт: {vacancies_i['experience']["name"]}")
        #     print(f"employer: {vacancies_i['employer']["name"]}")
        #     print("\n")


        for i in data["items"]:

            salary_i = f"от {i["salary"]["from"]}, до {i["salary"]["to"]}"
            if salary_i == None:
                salary_i = None
            print(f"зп: {salary_i}")

    except requests.RequestException as e:
        return e

vacancies("frontend", 2000)