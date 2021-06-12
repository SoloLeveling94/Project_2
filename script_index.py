from bs4 import BeautifulSoup
import requests
import csv
import time

def get_info_book(url):
    info_book = {}
    #cle = key + '_' + str(i)
    response = requests.get(url)
    data = response.content
    soup = BeautifulSoup(data, 'html.parser')
    results = soup.find(id='default')
    product_page_url = value
    universal_product_code = results.find('th', text='UPC').find_next_sibling('td').text
    title = results.find('h1').text
    price_including_tax = results.find('th', text='Price (incl. tax)').find_next_sibling('td').text
    price_excluding_tax = results.find('th', text='Price (excl. tax)').find_next_sibling('td').text
    number_search = results.find('th', text='Availability').find_next_sibling('td').text
    number_treatment = number_search.rsplit('(')
    number_treatment = number_treatment[1].split()

    for number in number_treatment:
        if number.isdigit():
            number_available = number

    product_description = results.find('div', id='product_description')
    if product_description is None:
        product_description = " "
    else:
        product_description = results.find('div', id='product_description').find_next('p').text
        
    category_book = key
      
    # Recupere la valeur classe star-rating sans les childs
    review_rating = results.find('p', class_='star-rating')['class']
    review_rating = review_rating[1]

    img_url = results.find('div', {'class': 'item active'}).find_next("img")
    img_url = img_url.get('src')
    img_url = 'http://books.toscrape.com/' + img_url[6:]

    info_book = {
        'product_page_url': product_page_url,
        'universal_product_code': universal_product_code,
        'title': title,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'number_available': number_available,
        'product_description': product_description,
        'category': category_book,
        'review_rating': review_rating,
        'image_url': img_url
    }
    lst_info_books.append(info_book)
    Save_image(img_url)
    return lst_info_books

def Save_image(url):
    image_url = url
    filename = image_url.split('/')[-1]
    img_data = requests.get(image_url).content
    with open(filename, 'wb') as handler:
        handler.write(img_data)
    handler.close()


list_category = []
links_category_books = []
links_books = []
dict_links_category_name = {}
clean_list_category = []
page_category = []
dict_books = {}
dict_links_pages = {}
dict_links_books = {}
dict_info_books = {}

url = "http://books.toscrape.com/index.html"

response = requests.get(url)
data = response.content
soup = BeautifulSoup(data, 'html.parser')
results = soup.find(id='default')
next_page_link = soup.find('li', {'class': 'next'})
if (next_page_link) != None:
    next_page_link = next_page_link.find('a').attrs['href']
    next_page_link = url[:-10] + next_page_link

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
             dict_links_category_name[list] = 'http://books.toscrape.com/' + link['href']

for lk in dict_links_category_name:
    x = [] 
    url_lk = dict_links_category_name[lk]
    dict_links_pages[lk] = []
    x.append(url_lk)

    for i in range(2, 10):
        #time.sleep(1)
        test = url_lk[:-10] + 'page-' + str(i) + '.html'
        response = requests.get(test)
        if response.ok:
            x.append(test)

    dict_links_pages[lk] = x
            
#for key, value in dict_links_pages.items():
#    print(key, '--->', value)

for key, values in dict_links_pages.items():
    #print('Key :: ', key)
    links_books = []
    dict_links_books[key] = []
    for value in values:
        response = requests.get(value)
        #time.sleep(1)
        data = response.content
        soup = BeautifulSoup(data, 'html.parser')

        find_links_books = soup.find_all('div', {'class': 'image_container'})
        for link in find_links_books:
            links_books.append('http://books.toscrape.com/catalogue/' + link.find('a').attrs['href'][9:])
    dict_links_books[key] = links_books

for key, values in dict_links_books.items():
    #print(key, '--->', value)
    #dict_info_books[key] = {}
    lst_info_books = []
    csv_columns = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax',
             'number_available', 'product_description', 'category', 'review_rating', 'image_url']
    csv_file = key + '.csv'
    for value in values:
        get_info_book(value)
    try:
        with open(csv_file, 'w', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, dialect='excel', fieldnames=csv_columns)
            writer.writeheader()
            for info in lst_info_books:
                #print(info)                
                writer.writerow(info)
    except IOError:
        print("I/O error")
   
