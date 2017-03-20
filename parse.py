from bs4 import BeautifulSoup
import requests, pprint, shutil

headers = {
'user-agent':'my-app/0.0.1'
}

classes = {
'title': 'h1.recipe-header__title',
'description' : '.recipe-header__description ',    
'duration' : {
    'full': '.recipe-details__cooking-time-full',
    'prep' : '.recipe-details__cooking-time-prep .mins',
    'cook' : '.recipe-details__cooking-time-cook .mins'
},
'skill' : 'span.recipe-details__text',
'ingredients': '#recipe-ingredients .ingredients-list__content',
'method': 'ol.method__list',
'image': '.recipe-header__media img'
}
# duration as a dictionary with two keys of prep bake null 

def parse_page(food_link):

    info = {
    'title': '',
    'description': '',
    'duration' : {
        'full': '',
        'prep' : '',
        'cook' : ''
    },
    'skill':'',
    'ingredients': [],
    'method': [],
    'image' : '',
    }


    html_doc = requests.get(food_link, headers=headers)
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    info['title'] = soup.select(classes['title'])[0].string
    info['description'] = soup.select(classes['description'])[0].string
    info['skill'] = soup.select(classes['skill'])[0].string
    info['image'] = soup.select(classes['image'])[0].get('src')

    full = soup.select(classes['duration']['full'])
    prep = soup.select(classes['duration']['prep'])
    cook = soup.select(classes['duration']['cook'])

    if len(full):
        info['duration']['full'] = full[0].string  
    if len(prep):
        info['duration']['prep'] = prep[0].string  
    if len(cook):
        info['duration']['cook'] = cook[0].string  

    response = requests.get(f"https:{info['image']}", stream=True, headers=headers)

    with open(f'images/{info["title"]}.jpg', 'wb') as out_file:
        for chunk in response:
            out_file.write(chunk)

    ingredient_sections = soup.select(classes['ingredients'])[0] 

    it = ingredient_sections.children

    next(it)

    for element in it:
        heading = element.string
        steps = None

        try:
            steps = next(it)
        except StopIteration:
            break

        list_of_steps = []    

        for li in steps:
            string = ' '.join([x.string for x in filter(lambda i: i.string is not None, li.children)])
            list_of_steps.append(string)

            info['ingredients'].append({'heading': heading, 'steps': list_of_steps })

    method_section = soup.select(classes['method'])[0] 

    for li in method_section.children:
        p = next(li.children)
        instructions = ' '.join([x.string for x in filter(lambda i: i.string is not None, p.children)])
        info['method'].append(instructions)

    return info
