import requests
from bs4 import BeautifulSoup
from app.config.config_loader import load_config
from app.exporters.csv_exporter import save_to_csv
from app.exporters.json_exporter import save_to_json
from app.exporters.excel_exporter import save_to_excel
from urllib.parse import urljoin
Rating = {
    "One":1,
    "Two":2,
    "Three":3,
    "Four":4,
    "Five":5
}
def _fetch_soup(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed {url}")
        print(e)
        return None
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup    
def scrape_page(url):
    page_books = []
    soup = _fetch_soup(url)
    if soup is None:
        return []
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
def scrape_website(url):
    books_data =[]
    current_url = url
    while current_url:
        books = scrape_page(current_url)
        books_data.extend(books)  
        soup = _fetch_soup(current_url)
        next_page = soup.find("li", class_="next")  
        if next_page is None:
            current_url = None 
        else:
            next_link = next_page.find("a")
            next_href = next_link["href"]
            current_url = urljoin(current_url, next_href)
    return books_data                    
def main():
    config = load_config("config.json")
    url = config["url"]
    books_data = scrape_website(url)
    print(len(books_data))
    save_to_csv(books_data,config["output"]["csv"])
    save_to_json(books_data,config["output"]["json"])
    save_to_excel(books_data,config["output"]["excel"])
if __name__ == "__main__":
    main()        

            

