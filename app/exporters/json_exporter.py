import json
def save_to_json(books,filename):
    with open(filename,"w",encoding="utf-8") as file:
        json.dump(books,file,indent=4)