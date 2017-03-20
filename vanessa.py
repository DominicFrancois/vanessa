from bs4 import BeautifulSoup
from parse import parse_page, headers, requests

food_link = 'https://www.bbcgoodfood.com/search/recipes?query=&page=0#path=course/dinner/course/main-course'

html_doc = requests.get(food_link, headers=headers)
soup = BeautifulSoup(html_doc.text, 'html.parser')
pages = soup.select('.teaser-item__title a')

for a in pages:

	url = f"https://www.bbcgoodfood.com{(a['href'])}"
	print(url)
	print(parse_page(url))