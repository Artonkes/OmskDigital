import requests
from bs4 import BeautifulSoup

r = requests.get("https://omsk.postupi.online/professiya/it-specialist/ssuzy/")

r.raise_for_status()
# with open("College.lxml", "w", encoding="utf-8") as college:
#     college.write(r.text)

soup = BeautifulSoup(r.content, "lxml")
# print(soup.prettify())
# print(soup.find("ul", class_="list-unstyled list-wrap").find("div", class_="flex-nd list__info-inner"))

#name
name = soup.find("ul", class_="list-unstyled list-wrap").find_all("a")

