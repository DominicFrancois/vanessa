from bs4 import BeautifulSoup
import requests, pprint

food_link = "https://www.bbcgoodfood.com/recipes/1997/classic-victoria-sandwich"

headers = {
	'user-agent':'my-app/0.0.1'
}

classes = {
	'title': 'h1.recipe-header__title',
	'description' : '.recipe-header__description p',	
	'duration' : '.recipe-details__cooking-time-full',
	'skill' : 'span.recipe-details__text',
	'ingredients': 'li.ingredients-list__item'
}

info = {
	'title': '',
	'description': '',
	'duration':'',
	'skill':'',
	'ingredients': '',
}

html_doc = requests.get(food_link, headers=headers)
soup = BeautifulSoup(html_doc.text, 'html.parser')

info['title'] = soup.select(classes['title'])[0].string
info['description'] = soup.select(classes['description'])[0].string
info['duration'] = soup.select(classes['duration'])[0].string
info['skill'] = soup.select(classes['skill'])[0].string
#info['ingredients'] = soup.select(classes['ingredients'])[0].string

section = soup.find('div', classes='ingredients-list__content')
info['ingredients'] = section.find_all('li').find_all('li')


#buyers = soup.select('.ingredients-list__item')

#for ul in ingredients:
#	for li in ul.findAll('li'):
#   	 print(li)

#ingredients-list__item
pprint.pprint(info)