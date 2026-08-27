import csv
def save_to_csv(books,filename):
    with open(filename,"w",newline = "",encoding="utf-8")  as file:
        writer = csv.DictWriter(file,fieldnames=["title","price","rating"])
        writer.writeheader()
        writer.writerows(books)