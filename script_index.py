from bs4 import BeautifulSoup
from pathlib import Path
import requests
import csv
import time
import os
import timeit

def get_info_book(url):
    try:
        info_book = {}
        response = requests.get(url)
        data = response.content
        soup = BeautifulSoup(data, 'html.parser')
        results = soup.find(id='default')
        table_td = results.select("td")
        product_page_url = value
        #universal_product_code = results.find(
        #    'th', text='UPC').find_next_sibling('td').text
        universal_product_code = str(table_td[0])[5:-6]
        #title = results.find('h1').text
        title = str(results.select("h1"))[5:-6]
        #price_including_tax = results.find(
        #    'th', text='Price (incl. tax)').find_next_sibling('td').text
        price_including_tax = str(table_td[3])[4:-5]
        #price_excluding_tax = results.find(
        #    'th', text='Price (excl. tax)').find_next_sibling('td').text
        price_excluding_tax = str(table_td[2])[4:-5]
        #number_search = results.find(
        #    'th', text='Availability').find_next_sibling('td').text
        number_search = str(table_td[5])[4:-5]
        number_treatment = number_search.rsplit('(')
        number_treatment = number_treatment[1].split()

        for number in number_treatment:
            if number.isdigit():
                number_available = number

        search_p = results.select("p")
        #product_description = results.find('div', id='product_description')
        product_description = str(search_p[3])[3:-4]
        #if product_description is None:
        #    product_description = " "
        #else:
        #    product_description = results.find(
        #        'div', id='product_description').find_next('p').text

        category_book = key

        # Recupere la valeur classe star-rating sans les childs
        #review_rating = results.find('p', class_='star-rating')['class']
        #review_rating = review_rating[1]
        search_rating = str(results.select_one("[class~=star-rating]"))
        star = ['One', 'Two', 'Three', 'Four', 'Five']
        for s in star:
            if s in search_rating:
                review_rating = s
       
        img_url = str(results.select_one("img"))
        x = img_url.find('../') + 6
        y = img_url.find('"/>')
        img_url = 'http://books.toscrape.com/' + img_url[x:y]

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
        print(f"Infos du livre récupérées : {title}")
        lst_info_books.append(info_book)
        save_image(img_url)
        print(f"-> Image du livre enregistée")
        return lst_info_books

    except Exception as e:
        print(e)


def save_image(url):

    parent_dir = Path().absolute()
    directory = "images_books"
    path = os.path.join(parent_dir, directory)
    image_url = url
    filename = image_url.split('/')[-1]
    img_data = requests.get(image_url).content
    completename = os.path.join(path, filename)

    try:
        os.makedirs(path, exist_ok=True)
        with open(completename, 'wb') as handler:
            handler.write(img_data)

    except Exception as e:
        print(e)

    finally:
        handler.close()


def save_csv(my_csv_file):
    
    try:
        with open(my_csv_file, 'w', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(
                csvfile, dialect='excel', fieldnames=csv_columns)
            writer.writeheader()
            for info in lst_info_books:
                writer.writerow(info)

    except Exception as e:
        print(e)

    finally:
        csvfile.close()


list_category = []
links_books = []
dict_links_category_name = {}
clean_list_category = []
dict_links_pages = {}
dict_links_books = {}


url = "http://books.toscrape.com/index.html"

try:
    response = requests.get(url)
    data = response.content
    soup = BeautifulSoup(data, 'html.parser')
    results = soup.find(id='default')
    next_page_link = soup.find('li', {'class': 'next'})
    category_books = soup.find('ul', {'class': 'nav nav-list'}).text
    list_category = category_books.splitlines()
    list_category = list(filter(str.strip, list_category))

    for i in list_category:
        j = i.replace('  ', '')
        clean_list_category.append(j)

    for cat in clean_list_category:
        if cat == 'Books':
            clean_list_category.remove(cat)

    # On crée le dictionnaire de catégorie 'dict_links_category_name' avec nom(clean_list) 
    # comme key & lien comme value 
    start_of_f1 = time.time()
    find_links_href = soup.find_all('a', {'href': True})
    for link in find_links_href:
        for lst in clean_list_category:
            if lst == link.text.strip():
                dict_links_category_name[lst] = 'http://books.toscrape.com/' + link['href']
    end_of_f1 = time.time()
    print(f"Temps pour récupèrer le lien des catégories index :{end_of_f1-start_of_f1}")

    # On crée le dictionnaire de liens des pages de chaque catégorie 'dict_link_pages'
    start_of_f2 = time.time()  
    for lk in dict_links_category_name:
        x = []
        url_lk = dict_links_category_name[lk]
        dict_links_pages[lk] = []
        x.append(url_lk)
        print(f"Récupération du lien des pages de chaque catégorie : {url_lk}")
        # On récupère les pages suivantes de chaque catégorie si elles existent 
        for i in range(2, 10):
            # time.sleep(1)
            test = url_lk[:-10] + 'page-' + str(i) + '.html'
            response = requests.get(test)
            if response.ok:
                x.append(test)
                print(f"-----------------------------------------> {test}")
            else:
                break

        dict_links_pages[lk] = x
    end_of_f2 = time.time()
    print(f"Temps pour récupèrer les liens de chaque catégorie :{end_of_f2-start_of_f2}")
    # On crée 'dict_links_books' et récupère tous les liens book de chaque page
    start_of_f3 = time.time()
    for key, values in dict_links_pages.items():
        links_books = []
        dict_links_books[key] = []
        for value in values:
            response = requests.get(value)
            # time.sleep(1)
            data = response.content
            soup = BeautifulSoup(data, 'html.parser')

            find_links_books = soup.find_all(
                'div', {'class': 'image_container'})
            for link in find_links_books:
                links_books.append(
                    'http://books.toscrape.com/catalogue/' + link.find('a').attrs['href'][9:])
        dict_links_books[key] = links_books
    end_of_f3 = time.time()
    print(f"Temps pour récupèrer les liens de chaque livre :{end_of_f3-start_of_f3}")
    # On récupère tous les info de chaque book, enregistre l'image puis crée un csv par catégorie
    start_of_f4 = time.time()
    for key, values in dict_links_books.items():
        lst_info_books = []
        csv_columns = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax',
                       'price_excluding_tax','number_available', 'product_description', 'category',
                       'review_rating', 'image_url']
        csv_file = key.replace(" ", "_") + '.csv'
        for value in values:
            get_info_book(value)
            print(f"---> {len(values)} livre(s) traité(s) pour la catégorie {csv_file[:-4]}")
        save_csv(csv_file)
        print(f"---> Enregistrement du fichier {csv_file}")
    end_of_f4 = time.time()
    print(f"Temps total pour récupèrer les infos, enregistrer image et csv :{end_of_f4-start_of_f4}")
except Exception as e:
    print(e)
