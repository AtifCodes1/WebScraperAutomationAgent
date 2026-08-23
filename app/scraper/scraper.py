import requests
from bs4 import BeautifulSoup
def scrape_page(url):
    page_books = []
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Re  uest failed {url}")
        print(e)
        return []    
    html = response.text
    soup = BeautifulSoup(html,"html.parser")
    books = soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
    for book in books:
        title_tag = book.find("h3")
        if title_tag is None:
            print("skiping book,Title not found")
            continue
        title = title_tag.a["title"]
        price_tag = book.find("p",class_="price_color")
        if price_tag is None:
            print("skiping book,Price not found")
            continue
        price = price_tag.get_text(strip=True)
        price = price.replace("Â£","")
        price = float(price)
        rating_tag = book.find("p",class_= "star-rating")
        if rating_tag is None:
            print("Skipping book : Rating tag not found")
            continue
        rating = rating_tag["class"]
        rating = rating[1]
        data ={
            "title":title,
            "price":price,
            "rating":rating }
        page_books.append(data)
    return page_books    
def main():
    books_data = []
    url_1 = "https://books.toscrape.com/"
    books = scrape_page(url_1)
    books_data.extend(books)
    for page_no in range(2,51):
        url_2 = f"https://books.toscrape.com/catalogue/page-{page_no}.html"
        books = scrape_page(url_2)
        books_data.extend(books)
    print(len(books_data))
main()        

            

