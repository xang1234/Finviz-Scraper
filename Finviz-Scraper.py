import requests
from bs4 import BeautifulSoup
import pandas as pd
import progressbar


def scrape_finviz(symbols):
    # Get Column Headers
    req = requests.get("https://finviz.com/quote.ashx?t=FB")
    soup = BeautifulSoup(req.content, 'html.parser')
    table = soup.find_all(lambda tag: tag.name=='table')
    rows = table[8].findAll(lambda tag: tag.name=='tr')
    out=[]
    for i in range(len(rows)):
        td=rows[i].find_all('td')
        out=out+[x.text for x in td]

    ls=['Ticker']+out[::2]
    dict_ls={k:ls[k] for k in range(len(ls))}

    #  Scrape required Data from symbols
    df=pd.DataFrame()
    p = progressbar.ProgressBar()
    p.start()
    for j in range(len(symbols)):
        p.update(j/len(symbols) * 100)
        req = requests.get("https://finviz.com/quote.ashx?t="+symbols[j])
        if req.status_code !=200:
            continue
        soup = BeautifulSoup(req.content, 'html.parser')
        table = soup.find_all(lambda tag: tag.name=='table')
        rows = table[8].findAll(lambda tag: tag.name=='tr')
        out=[]
        for i in range(len(rows)):
            td=rows[i].find_all('td')
            out=out+[x.text for x in td]
        out=[symbols[j]]+out[1::2]
        out_df=pd.DataFrame(out).transpose()
        df=df.append(out_df,ignore_index=True)

    p.finish()
    df=df.rename(columns=dict_ls)

    return(df)

### Example usage
data=scrape_finviz(['FB','INGN'])
