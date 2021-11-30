# web scrape buoy data from python
# raw_df = data scraped from web


import requests
from bs4 import BeautifulSoup as bs 
import pandas as pd
import matplotlib.pyplot as plt



def raw_df(buoy_number, ext):
    general_URL = "https://www.ndbc.noaa.gov/data/realtime2/"
    URL = general_URL + buoy_number + ext

    # Load the webpage content
    r = requests.get(URL)
    
    # Convert to beautiful soup object
    soup = bs(r.content, features='lxml')
    
    # Print out our html to find content we want
    # print(soup.prettify())
    
    # filter out where data is in <p>
    content = soup.find("p")
    content = str(content)
    
    # convert content to a list
    vals = content.split('\n') # creates list of each row in content
    
    # start df 
    row1 = vals[0].split()
    row2 = vals[1].split()
    
    d = {row1[i] : row2[i] for i in range(len(row1))}
    df = pd.DataFrame([d])
    
    # append rows in vals to df
    for x in range(len(vals)-1): # need to subtract 1 to get rid of html <p>
        row = vals[x].split()
        df.loc[len(df)] = row
    
    df = df.drop([0,1,2])
    df = df.reset_index(drop=True)
    df = df.rename({'<p>#YY':'#YY'}, axis=1)
        
    return df


def clean_df(df):  
    # df = raw_df(URL)
    df = df.head(100) # last 3 days of data
    df = df.iloc[::4, :] # every 4th row to prevent over plotting
    df = df.reset_index(drop=True)

    # convert SwH m to ft
    df['SwH'] = df['SwH'].astype(float) 
    df['SwH'] = df['SwH'] * 3.28
    df['SwH'] = df['SwH'].round(1)
    
    # convert WWH to ft
    df['WWH'] = df['WWH'].astype(float) 
    df['WWH'] = df['WWH'] * 3.2804
    df['WWH'] = df['WWH'].round(1)
    
    # convert periods to floats
    df['SwP'] = df['SwP'].astype(float)
    df['APD'] = df['APD'].astype(float)
        
    # create date col
    df['date'] = df['MM'] + '-' + df['DD'] + '-' + df['hh'] + ':' + df['mm']

    return df


def plot(df):

    df['date'] = df['date'].iloc[::-1]
    df['WWH'] = df['WWH'].iloc[::-1]
    df['SwH'] = df['SwH'].iloc[::-1]
    df['APD'] = df['APD'].iloc[::-1]
    df['SwP'] = df['SwP'].iloc[::-1]
    df = df.reset_index(drop=True)

    plt.style.use('seaborn-darkgrid')
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    ax1.plot(df['date'], df['WWH'], label='Wind Swell')
    ax1.plot(df['date'], df['SwH'], label='Ground Swell')
    ax1.legend(loc='upper center', shadow=True)
    ax1.tick_params(axis='x', rotation=45)
    ax1.set_ylabel('ft')
    ax1.set_title("Swell Height")
    # plt.gca().invert_xaxis()

    ax2.plot(df['date'], df['APD'], label='Wind Swell')
    ax2.plot(df['date'], df['SwP'], label='Ground Swell')
    ax2.set_ylabel('sec')
    ax2.tick_params(axis='x', rotation=45)
    ax2.set_title("Swell Period")
    ax2.legend(loc='best')

    plt.gca().invert_xaxis()

    fig.tight_layout()
    return plt.show()
    

# general_URL = "https://www.ndbc.noaa.gov/data/realtime2/"
# buoy_number = "41110"
# URL = general_URL + buoy_number + '.spec'



    
    
    
    
    
    
    
    
    
    
    
    
    
