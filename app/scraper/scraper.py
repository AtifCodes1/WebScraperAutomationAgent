import requests
from bs4 import BeautifulSoup
from app.config.config_loader import load_config
from app.exporters.csv_exporter import save_to_csv
from app.exporters.json_exporter import save_to_json
from app.exporters.excel_exporter import save_to_excel
Rating = {
    "One":1,
    "Two":2,
    "Three":3,
    "Four":4,
    "Five":5
}
def scrape_page(url):
    page_books = []
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed {url}")
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
        title = title_tag.a["title"].strip()
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
        rating = Rating.get(rating)
        if rating is None:
            print(f"Skiping book {title} invalid rating ")
            continue
        data ={
            "title":title,
            "price":price,
            "rating":rating }
        page_books.append(data)
    return page_books                    
def main():
    books_data = []
    config = load_config("config.json")
    url_1 = config["url"]
    books = scrape_page(url_1)
    books_data.extend(books)
    pages = config["pages"]
    page_url = config["page_url"]
    for page_no in range(2,pages + 1):
        url_2 = page_url.format(page=page_no)
        books = scrape_page(url_2)
        books_data.extend(books)
    print(len(books_data))
    save_to_csv(books_data,config["output"]["csv"])
    save_to_json(books_data,config["output"]["json"])
    save_to_excel(books_data,config["output"]["excel"])
main()        

            

