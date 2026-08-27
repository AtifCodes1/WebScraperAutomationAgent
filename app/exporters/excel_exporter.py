import pandas as pd
def save_to_excel(books,filename):
    df = pd.DataFrame(books)
    df.to_excel(filename,index=False) 