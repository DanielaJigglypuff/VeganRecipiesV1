from bs4 import BeautifulSoup
import requests
import time
from csv import writer

url = "https://www.pickuplimes.com/recipe/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

def obtain_names(url):
    names = []
    lists = soup.find_all(attrs={'class': 'flex-item'})
    for item in lists:
        names.append(item.find("h3").text.strip(None))
    return names

def obtain_link(url):
    links=[]
    lists = soup.find_all('li')
    for item in lists:
        if item.find('a').has_attr('href'):
            elm = item.find('a')['href']
            if elm !="/recipe/" and elm.find("/recipe/") != -1:
                links.append("https://www.pickuplimes.com"+item.find('a')['href'])
        else:
            links.append("no links avaliable")
    return links

def obtain_list_ingredients(url):
    page = requests.get(url)
    time.sleep(1)
    soup = BeautifulSoup(page.content, 'html.parser')
    ingredients=[]
    lists = soup.find_all(attrs={'class': 'ingredient-name-text'})
    for item in lists:
        ingredients.append(item.text)
    return ingredients


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def listmagick(source):
    fin =[]
    ltemp=[]
    for lst in source:
        interval = len(lst)
    for j in range(interval):
        for k in range(len(source)):
           fin.append(source[k][j])
    final = list(chunker(fin,3))
    return(final)
with open('food.csv','w',encoding='utf8',newline='') as f:
    thewriter = writer(f)
    header=['Nume','Link','Ingrediente']
    thewriter.writerow(header)
    i = 0
    info=[]
    while i<29:
        i += 1
        urli=url+"?page="+str(i)
        page = requests.get(urli)
        time.sleep(1)
        soup = BeautifulSoup(page.content, 'html.parser')
        names = obtain_names(urli)
        links = obtain_link(urli)
        ingredients = []
        for j in links:
            ingredients.append(obtain_list_ingredients(j))
        temp = [names, links, ingredients]
        for m in range(12):
            thewriter.writerow(listmagick(temp)[m])