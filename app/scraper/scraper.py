import requests
from bs4 import BeautifulSoup
books_data = []
def scrap_page(url):
    response = requests.get(url,timeout=10)
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html,"html.parser")
    books = soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
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
            "rating":rating }
        books_data.append(data)
def main():
    url_1 = "https://books.toscrape.com/"
    scrap_page(url_1)
    for page_no in range(2,51):
        url_2 = f"https://books.toscrape.com/catalogue/page-{page_no}.html"
        scrap_page(url_2)
    print(len(books_data))
main()        

            

