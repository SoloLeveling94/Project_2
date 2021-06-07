import requests
from bs4 import BeautifulSoup

#URL = 'http://books.toscrape.com/'
url = 'http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html'
response = requests.get(url)
data = response.content
soup = BeautifulSoup(data, 'html.parser')
results = soup.find(id='default')

info_book = []

# Affichage lisible html
#print(results.prettify())

product_page_url = url
info_book.append(product_page_url)

universal_product_code = results.find('th', text = 'UPC').find_next_sibling('td').text
info_book.append(universal_product_code)

title = results.find('h1').text
info_book.append(title)

price_including_tax = results.find('th', text = 'Price (incl. tax)').find_next_sibling('td').text
info_book.append(price_including_tax)

price_excluding_tax = results.find('th', text = 'Price (excl. tax)').find_next_sibling('td').text
info_book.append(price_excluding_tax)

number_search = results.find('th', text = 'Availability').find_next_sibling('td').text
number_treatment = number_search.rsplit("(")
#print("1 " , number_treatment)
number_treatment = number_treatment[1].split()
#print("2 " ,  number_treatment)
for number in number_treatment:
	if number.isdigit():
		info_book.append(number)

product_description = (results.find('div', id = 'product_description').find_next_sibling('p').text)
info_book.append(product_description)

category = results.find('ul', class_ = 'breadcrumb')
category_split = list(category.stripped_strings)
#print(category_split)
info_book.append(category_split[2])

#Recupere la valeur classe star-rating sans les childs
review_rating = results.find('p', class_ = 'star-rating')['class']
review_rating = review_rating[1]
#print(review_rating)
info_book.append(review_rating)

img_url = results.find('div', {'class':'item active'}).find_next("img")
img_url = img_url.get('src')
info_book.append(img_url)


for info in info_book:
	print(info)







