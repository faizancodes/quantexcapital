import requests
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from urllib.request import urlopen
from twilio.rest import Client

account_sid = 'ACb93dd3a248d0aa6a2007888a0a4a9ff3'
auth_token = '95761be133406992e00ef73715e0ce6d'
client = Client(account_sid, auth_token)

data = []
smas = ""
priceRatings = []
newsT = []
symbols = []
price = ""
change = ""
prevClose = ""
ps = ""
rsi = ""
earnings = ""
targetPrice = ""
perfWeek = ""
perfMonth = ""
perfQuarter = ""
perfYTD = ""
quarterlyRevGrowth = ""
profitMargin = ""
dividend = ""
roa = ""
tg = ""
stockCounter = 0
c = 1
skip = False
sma20 = 0
sma50 = 0
sma200 = 0
pe = 0
forwardPE = 0
text = ""

def getTechnicals(inURL, sy):
    page = requests.get(inURL + sy)
    soup = BeautifulSoup(page.text, 'html.parser')
    technicals = soup.find_all('tr', {'class' : 'table-dark-row'})
    pts = soup.find_all('table', {'class' : 'fullview-ratings-outer'})
    news = soup.find_all('table', {'class': 'fullview-news-outer'})

    global data
    global smas
    global pes
    global priceRatings
    global ps
    global rsi
    global earnings
    global price
    global change
    global prevClose
    global targetPrice 
    global perfWeek
    global perfMonth
    global perfQuarter
    global perfYTD
    global quarterlyRevGrowth
    global profitMargin
    global dividend
    global roa
    global tg
    global skip
    global sma20
    global sma50
    global sma200
    global pe
    global forwardPE

    for t in range(len(technicals)):
        data.append(technicals[t].text.strip())

    for t in range(len(data)):
        if 'Price' in data[t]:
            price = data[t][data[t].find('Price') + 5 : ].strip()

        if 'Change' in data[t]:
            change = data[t][data[t].find('Change') + 6 : ].strip()

        if 'Prev Close' in data[t]:
            prevClose = data[t][data[t].find('Prev Close') + 10 : ].strip()

        if 'SMA' in data[t]:
            smas = (data[t][data[t].find('SMA') : data[t].find('Volume')])

        if 'P/E' in data[t]:
            if 'Index' in data[t]:
                pe = data[t][data[t].find('P/E') + 3 : data[t].find('EPS')].strip()

        if 'Forward P/E' in data[t]:
            forwardPE = data[t][data[t].find('Forward P/E') + 11 : data[t].find('EPS')].strip()

        if 'P/S' in data[t]:
            ps = data[t][data[t].find('P/S') + 3 : data[t].find('EPS') - 1]

        if 'RSI' in data[t]:
            rsi = data[t][data[t].find('(14)') + 4 : data[t].find('(14)') + 9]
        
        if 'Earnings' in data[t]:
            earnings = data[t][data[t].find('Earnings') + 8 : data[t].find('Earnings') + 18]
        
        if 'Target Price' in data[t]:
            targetPrice = data[t][data[t].find('Target Price') + 12 : data[t].find('Perf') - 1]

        if 'Perf Week' in data[t]:
            perfWeek = data[t][data[t].find('Week') + 4 : ]
        
        if 'Perf Month' in data[t]:
            perfMonth = data[t][data[t].find('Month') + 5 : ]

        if 'Perf Quarter' in data[t]:
            perfQuarter = data[t][data[t].find('Quarter') + 7 :]

        if 'Perf YTD' in data[t]:
            perfYTD = data[t][data[t].find('YTD') + 3 : ]
        
        if 'Sales Q/Q' in data[t]:
            quarterlyRevGrowth = data[t][data[t].find('Sales Q/Q') + 9 : data[t].find('%') + 1]
        
        if 'Profit Margin' in data[t]:
            profitMargin = data[t][data[t].find('Profit Margin') + 13: data[t].find('Profit Margin') + 19].strip()
        
        if 'Dividend' in data[t]:
            dividend = data[t][data[t].find('Dividend') + 10 : data[t].find('.') + 4]

        if 'ROA' in data[t]:
            roa = data[t][data[t].find('ROA') + 3 : data[t].find('ROA') + 9].strip()

        #print(data[t])
    #print()
    #--------------------------------------------------
   
    for t in range(len(pts)):
        priceRatings.append(pts[t].text.strip())
    
    try:
        priceRatings = priceRatings[0].split('\n')
    except:
        #print('Error - Price Ratings')
        priceRatings = []

    for x in range(len(news)):
        tg = news[x].text
    
    s = getSMAs()

    #--------------------------------------------------
    
    #sortValueStocks(sy)

    #bullishMomentum(sy)
    printStats(sy)
    #print(sy, forwardPE)
    #printStats(sy)

    #--------------------------------------------------

def bullishMomentum(symbol):
     if forwardPE < pe and '-' not in forwardPE and '-' not in pe:
        if float(sma20[0 : len(sma20) - 1]) > 1 and float(sma20[0 : len(sma20) - 1]) > float(sma50[0 : len(sma50) - 1]) and float(sma200[0 : len(sma200) - 1]) > 1:
            if float(perfYTD[0 : len(perfYTD) - 1]) > 10:
                printStats(symbol)

def getPriceRatings():  
    for t in range(len(priceRatings)):
        if len(priceRatings[t]) > 1:
            print(priceRatings[t])
    
        if '$' in priceRatings[t] or 'Mkt Perform' in priceRatings[t]:
            print()

def getSMAs():
    global smas
    global sma20
    global sma50
    global sma200

    sma20 = smas[smas.find('SMA20')  + 5 : smas.find("%") + 1]
    smas = smas[smas.find("%") + 1 : ]
    sma50 = smas[smas.find('SMA50') + 5: smas.find("%") + 1]
    smas = smas[smas.find("%") + 1 : ]
    sma200 = smas[smas.find('SMA200') + 6: smas.find("%") + 1]
  
    ss = [sma20, sma50, sma200]
    return ss

def getPerfs():
    perfs = [perfWeek, perfMonth, perfQuarter, perfYTD]
    #print('Perf Week ' + perfWeek + '  Perf Month: ' + perfMonth + '  Perf Quarter: ' + perfQuarter + '  Perf YTD: ' + perfYTD)
    return perfs

def getNews():
    amPM = tg[tg.find(':') + 3 : tg.find(':') + 5]
    stop = False
    x = 1

    while not stop:      
        try:
            if amPM == 'PM':
                pt = tg.split('PM')[x].strip()
            else:
                pt = tg.split('AM')[x].strip()
        except:
            stop = True

        x = x + 1
        newsT.append(pt[0 : pt.find('\n')])
    
    print(newsT)

def getSymbols(inURL, add):
    global stockCounter
    global c
    page = requests.get(inURL)
    soup = BeautifulSoup(page.text, 'html.parser')
    symbs = soup.find_all('a', {'class' : 'screener-link-primary'})

    for x in range(len(symbs)):
        if '&amp;b=1' in str(symbs[x]):
            symbols.append(str(symbs[x])[str(symbs[x]).find('&amp;b=1') + 10 : str(symbs[x]).find('/a') - 1])
            stockCounter = stockCounter + 1

        if stockCounter % 20 == 0:
            c = c + 20
            getSymbols('https://finviz.com/screener.ashx?v=111' + addOn + '&r=' + str(c), addOn)
        
        if stockCounter >= 500:
            break

    return symbols

def sortValueStocks(sy):
    
    global data
    global smas
    global pes
    global priceRatings
    global ps
    global rsi
    global earnings
    global price
    global change
    global prevClose
    global targetPrice 
    global perfWeek
    global perfMonth
    global perfQuarter
    global perfYTD
    global quarterlyRevGrowth
    global profitMargin
    global dividend
    global roa
    global tg
    global skip
    global pe
    global forwardPE
    
    cc = float(price) - float(prevClose)

    pfs = getPerfs()
    s = getSMAs()

    if forwardPE < pe:
        if ('-' not in profitMargin) and (float(profitMargin[0 : len(profitMargin) - 1]) > 10):
            if float(pfs[3][0 : len(pfs[3]) - 1]) > 20:
                if float(quarterlyRevGrowth[0 : len(quarterlyRevGrowth) - 1]) >= 10:
                    printStats(sy)


def printStats(sy):
    
    global data
    global smas
    global pes
    global priceRatings
    global ps
    global rsi
    global earnings
    global price
    global change
    global prevClose
    global targetPrice 
    global perfWeek
    global perfMonth
    global perfQuarter
    global perfYTD
    global quarterlyRevGrowth
    global profitMargin
    global dividend
    global roa
    global tg
    global skip
    global pe
    global forwardPE
    global text
    global sma20
    global sma50
    global sma200
    
    cc = float(price) - float(prevClose)

    pfs = getPerfs()
    
    print('------------------------------------------------------------------------------------')
    
    skip = True
    
    print(sy)
    text += '\n' + sy
    
    print('Price: ' + price)
    text += '\n' + price

    if cc > 0:
        print('+' + str(cc)[0 : 4], change)
        text += '\n+' + str(cc)[0 : 4] + '  ' + change
    else:
        print(str(cc)[0 : 4], change)
        text += '\n' + str(cc)[0 : 4] + '  ' + change

    print('P/E: ' + pe + '  Forward P/E: ' + forwardPE)
    text += '\nP/E: ' + pe + '  Forward P/E: ' + forwardPE
    
    print('Profit Margin: ' + profitMargin)
    text += '\nProfit Margin: ' + profitMargin
    
    print('SMA 20: ' + sma20 + '  SMA 50: ' + sma50 +  '  SMA 200: ' + sma200)
    text += '\nSMA 20: ' + sma20 + '  SMA 50: ' + sma50 +  '  SMA 200: ' + sma200
    
    print('Perf Week ' + pfs[0] + '  Perf Month: ' + pfs[1] + '  Perf Quarter: ' + pfs[2] + '  Perf YTD: ' + pfs[3])
    text += '\nPerf Week ' + pfs[0] + '  Perf Month: ' + pfs[1] + '  Perf Quarter: ' + pfs[2] + '  Perf YTD: ' + pfs[3]
    
    if '-' not in earnings:
        print('Earnings Date: ' + earnings)
        text += '\nEarnings Date: ' + earnings
    
    if '-' not in quarterlyRevGrowth:
        print('Quarterly Revenue Growth: ' + quarterlyRevGrowth)
        text += '\nQuarterly Revenue Growth: ' + quarterlyRevGrowth
    
    print('RSI: ' + rsi)
    text += '\nRSI: ' + rsi
    
    if '-' not in dividend:
        print('Dividend ' + dividend)
        text += '\nDividend ' + dividend + '\n'
    
    text += '\n'

def loop():
    
    global dat
    global smas
    global pes
    global priceRatings
    global ps
    global rsi
    global earnings
    global price
    global change
    global prevClose
    global targetPrice 
    global perfWeek
    global perfMonth
    global perfQuarter
    global perfYTD
    global quarterlyRevGrowth
    global profitMargin
    global dividend
    global roa
    global tg
    global skip
    global addOn
    global sma20
    global sma50
    global sma200
    global pe 
    global forwardPE
    
    ss =  getSymbols('https://finviz.com/screener.ashx?v=111' + addOn + '&r=' + str(c), addOn)

    for x in range(len(ss)):
        getTechnicals('https://finviz.com/quote.ashx?t=', ss[x])

        if skip == True:
            print('\n')
        
        data = []
        smas = ""
        pes = []
        priceRatings = []
        newsT = []
        symbols = []
        price = ""
        change = ""
        prevClose = ""
        ps = ""
        rsi = ""
        earnings = ""
        targetPrice = ""
        perfWeek = ""
        perfMonth = ""
        perfQuarter = ""
        perfYTD = ""
        quarterlyRevGrowth = ""
        profitMargin = ""
        dividend = ""
        roa = ""
        tg = ""
        skip = False
        sma20 = 0
        sma50 = 0
        sma200 = 0
        pe = 0
        forwardPE = 0


#getTechnicals('https://finviz.com/quote.ashx?t=' , 'MSFT')
mA = '&s=ta_mostactive'
tG = '&s=ta_topgainers'
tL = '&s=ta_toplosers'
mV = '&s=ta_mostvolatile'
oB = '&s=ta_overbought'
oS = '&s=ta_oversold'
addOn = mA
loop()

nums = ['+13472386332', '+16467505120']
myNum = '+13472386332'
yashNum = '+19294267244'

#for x in range(len(nums)):
textLen = len(text)

'''
if textLen > 1600:
    t = text[0 : 1500]
    message = client.messages \
        .create(
            body = t,
            from_ = '+16469719976',
            to = myNum
        )

    t = text[1500 : ]
    message = client.messages \
    .create(
        body = t,
        from_ = '+16469719976',
        to = myNum
    )

print(message.sid)

print(text)
'''

#ss = getSymbols('https://finviz.com/screener.ashx?v=111' + addOn + '&r=' + str(c), addOn)
#print(ss)