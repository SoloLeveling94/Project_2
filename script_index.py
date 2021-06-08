from bs4 import BeautifulSoup
import requests


url = "http://books.toscrape.com/index.html"

response = requests.get(url)

data = response.content

soup = BeautifulSoup(data, 'html.parser')

list_category = []
links_category_books = []
links_books = []
dict_links_category_books = {}
clean_list_category = []

category_books = soup.find('ul', {'class': 'nav nav-list'}).text
list_category = category_books.splitlines()
list_category = list(filter(str.strip, list_category))

for i in list_category:
    j = i.replace('  ', '')
    clean_list_category.append(j)

for cat in clean_list_category:
    if cat == 'Books':
        clean_list_category.remove(cat)

find_links_href = soup.find_all('a', {'href': True})
for link in find_links_href:
    for list in clean_list_category:
        if list == link.text.strip():
            #links_category_books.append(link['href'])
            dict_links_category_books[list] = 'http://books.toscrape.com/' + link['href']
            
for key in dict_links_category_books:
    print(key, dict_links_category_books[key])

find_links_books = soup.find_all('div', {'class': 'image_container'})
for link in find_links_books:
    links_books.append(link.find('a').attrs['href'])

next_page_link = soup.find('li', {'class': 'next'})
next_page_link = next_page_link.find('a').attrs['href']
# print(next_page_link)


def Scrape_book(url):

    dict_info_book = {}

    product_page_url = url
    universal_product_code = results.find(
        'th', text='UPC').find_next_sibling('td').text
    title = results.find('h1').text
    price_including_tax = results.find(
        'th', text='Price (incl. tax)').find_next_sibling('td').text
    price_excluding_tax = results.find(
        'th', text='Price (excl. tax)').find_next_sibling('td').text
    number_search = results.find(
        'th', text='Availability').find_next_sibling('td').text
    number_treatment = number_search.rsplit("(")
    number_treatment = number_treatment[1].split()
    for number in number_treatment:
        if number.isdigit():
            number_available = number

    product_description = (results.find(
        'div', id='product_description').find_next_sibling('p').text)
    category = results.find('ul', class_='breadcrumb')
    category_split = list(category.stripped_strings)
    category_book = category_split[2]
    # print(category_split)

	# Recupere la valeur classe star-rating sans les childs
    review_rating = results.find('p', class_='star-rating')['class']
    review_rating = review_rating[1]
    # print(review_rating)

    img_url = results.find('div', {'class': 'item active'}).find_next("img")
    img_url = img_url.get('src')

    dict_info_book = {
        'product_page_url': product_page_url,
        'universal_product_code': universal_product_code,
        'title': title,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'number_available': number_available,
        'product_description': product_description,
        'category': category_book,
        'review_rating': review_rating,
        'image_url': 'http://books.toscrape.com/' + img_url[6:]
    }
    
    for key in dict_info_book:
        print(key, '--->', dict_info_book[key])

