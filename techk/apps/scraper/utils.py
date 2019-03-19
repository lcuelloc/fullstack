import requests
import re

from bs4 import BeautifulSoup

base_url = 'http://books.toscrape.com/'


# get all categories
def get_categories():
    req = requests.get(base_url)
    soup = BeautifulSoup(req.text, "lxml")
    categories = soup.find("div", {"class": "side_categories"})
    cat_list = categories.findAll('li')
    data = []
    for val in cat_list:
        if (val.a.text):
            text = val.a.text.strip()
            data.append(text)

    # remove books
    data.pop(0)
    return data


# get all book pages
def get_pages():
    count = 1
    req = requests.get(base_url)
    soup = BeautifulSoup(req.text, "lxml")
    current = soup.find("li", {'class': 'current'}).text
    total = int((re.findall('\d+', current ))[1])
    data = []
    while count <= total:
        data.append(base_url + f"catalogue/page-{count}.html")
        count +=1
    
    return data


# get books from one page
def get_page_books(page):
    # get page data
    req = requests.get(page)
    soup = BeautifulSoup(req.text, "lxml")

    # get all books
    articles = soup.findAll("article", {"class": "product_pod"})
    data = []
    for art in articles:
        link = art.a['href']
        link_format = base_url + 'catalogue/' + link
        thumbnail = art.img['src']
        thumb_format = base_url + thumbnail.replace('../', '')
        data.append({
            'url': link_format,
            'thumbnail': thumb_format
        })
    return data


# format book body
def get_book_info(book):
    print(book['url'])
    req = requests.get(book['url'])
    soup = BeautifulSoup(req.text, 'lxml')
    # get categories breadcrumb
    breadcrumb = soup.find('ul',{'class': 'breadcrumb'})
    # get category
    category = breadcrumb.findAll('li')[2].a.text

    article = soup.find('article', {'class': 'product_page'})
    # get title
    title =  article.find('h1').text
    price_string = article.find('p', {'class': 'price_color'}).text
    # get price
    price = price_string[2:]
    stock_string = article.find('p', {'class': 'instock availability'}).text
    # get stock
    stock =  int((re.findall('\d+', stock_string ))[0])
    # get description
    desc_body = article.find('p', {'class': None})
    description = desc_body.text if desc_body else None
    # get table
    table = article.find('table', {'class': 'table table-striped'})
    # get upc
    upc = table.find('td').text
    # format body
    if None in [category,title,price,stock,upc]:
        return {}

    body = {
        'category': category,
        'title': title,
        'thumbnail_url': book['thumbnail'],
        'price': price,
        'stock': stock,
        'product_description': description,
        'upc': upc
    }

    return body
