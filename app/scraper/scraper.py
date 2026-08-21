import requests
from bs4 import BeautifulSoup
url = "https://books.toscrape.com/"
response = requests.get(url,timeout=10)
response.raise_for_status()
html = response.text
soup = BeautifulSoup(html,"html.parser")
books = soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
books_data = []
for book in books:
    tag = book.find("h3")
    title = tag.a["title"]
    price_tag = book.find("p",class_="price_color")
    price = price_tag.get_text(strip=True)
    price = price.replace("Â£","")
    price = float(price)
    rating_tag = book.find("p",class_= "star-rating")
    rating = rating_tag["class"]
    rating = rating[1]
    data ={
        "title":title,
        "price":price,
        "rating":rating
        }
    books_data.append(data)
for data in books_data:
    print(data)