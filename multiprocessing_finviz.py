import requests
import sys
from bs4 import BeautifulSoup
import pandas as pd
import time
from multiprocessing import Process
from multiprocessing import Queue


def scrape_finviz(symbols, output):
    # Get Column Header
    req = requests.get("https://finviz.com/quote.ashx?t=FB")
    soup = BeautifulSoup(req.content, 'html.parser')
    table = soup.find_all(lambda tag: tag.name=='table') 
    rows = table[8].findAll(lambda tag: tag.name=='tr')
    out=[]
    for i in range(len(rows)): 
        td=rows[i].find_all('td')
        out=out+[x.text for x in td]

    ls=['Ticker','Sector','Sub-Sector','Country']+out[::2]  

    dict_ls={k:ls[k] for k in range(len(ls))}
    df=pd.DataFrame()

    for j in range(len(symbols)):
        req = requests.get("https://finviz.com/quote.ashx?t="+symbols[j])
        if req.status_code !=200:
            continue
        soup = BeautifulSoup(req.content, 'html.parser')
        table = soup.find_all(lambda tag: tag.name=='table') 
        
        rows=table[6].findAll(lambda tag: tag.name=='tr')
        sector=[]
        for i in range(len(rows)): 
            td=rows[i].find_all('td')
            sector=sector+[x.text for x in td]
        sector=sector[2].split('|')
        rows = table[8].findAll(lambda tag: tag.name=='tr')
        out=[]
        for i in range(len(rows)): 
            td=rows[i].find_all('td')
            out=out+[x.text for x in td]
        out=[symbols[j]]+sector+out[1::2]
        out_df=pd.DataFrame(out).transpose()
        df=df.append(out_df,ignore_index=True)

    df=df.rename(columns=dict_ls)  
    
    output.put(df)

    
def main():
    
    # Define default save path
    default_path='C:/SnP500.csv'
    if sys.argv[1] is not None:
        default_path=sys.argv[1]
    # Define an output queue
    output = Queue()
    spy=pd.read_csv('https://datahub.io/core/s-and-p-500-companies/r/constituents.csv')
    spy_list=spy['Symbol'].tolist()


    ### Split into 4 lists of Symbols
    num=4
    div=[spy_list[i::num] for i in range(num)]
    start=time.time()
    
    ### Multiprocessing with Process
    processes=[Process(target=scrape_finviz,args=(div[i],output)) for i in range(num)]
    
    # Run processes
    for p in processes:p.start()

    # Get process results from the output queue
    results = [output.get() for p in processes]
    results_df = pd.concat(results)
    print("Time Taken: ",str(time.time()-start))
    results_df.to_csv(default_path)
    # Exit the completed processes
    for p in processes:p.join()

if __name__ == '__main__':
    main()
    


