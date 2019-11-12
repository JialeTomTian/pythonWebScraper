import requests
from datetime import datetime
from bs4 import BeautifulSoup

tickerSymbol = input('Please enter the ticker symbol ')
webLink = 'http://quotes.wsj.com/' + tickerSymbol

def websiteFetcher(webLink):
    '''
    websiteFetcher fetches a website using the request module and turns it into a beautifulSoup Object
    --param
    webLink: String
    ---return
    beautifulSoupObject
    '''
    myRequest = requests.get(webLink)
    newTest = BeautifulSoup(myRequest.text[20000:100000], 'html.parser')
    return(newTest)
#end of websiteFetcher

webHTML = websiteFetcher(webLink)

def informationSorter(webHTML):
    '''
    informationSorter sorts the website's html to grab needed information
    --param
    webHTML: beautifulSoup Object
    ---return
    dictionary
    '''

    outputDictionary = {}

    #date example: <span class="timestamp_value" id="quote_dateTime">4:00 PM EDT 08/02/19</span>
    outputDictionary["Date Time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #Open Price: <ul class="cr_data_collection"> <li> <span class="data_lbl">Open </span> <span class="data_data">1,157.80</span> </li> <li> <span class="data_lbl">Prior Close </span> <span class="data_data">1,171.08 <span class="data_meta">(08/06/19)</span></span> </li> </ul>
    outerOpenClose = webHTML.find_all('ul', attrs={"class":"cr_data_collection"})[1]
    inner = outerOpenClose.find_all('span', attrs={"class":"data_data"})
    openPrice = inner[0].text
    outputDictionary["Open Price"] = openPrice

    #Previous Close:
    previousClose = inner[1].text.split(" ")[0]
    outputDictionary["Previous Close"] = previousClose

    #current price: <span id="ms_quote_val">1,196.70</span></span>
    currentPrice = webHTML.find('span', attrs={'id':'quote_val'})
    currentPrice = float(currentPrice.text.replace(",",""))
    outputDictionary['Current Price'] = currentPrice



    #Percent Change: <span class="cr_num diff_percent" id="quote_changePer">-1.28%</span>
    percentChange = webHTML.find('span', attrs={'id':'quote_changePer'})
    outputDictionary['Percent Change'] = percentChange.text

    #Amount Change: <span class="cr_num diff_price" id="quote_change">-15.46</span>
    amountChange = webHTML.find('span', attrs={"id":"quote_change"})
    outputDictionary['Change'] = float(amountChange.text.replace(",",""))

    #52 Week High and Low: <div class="cr_data_field"> <span class="data_lbl">52 Week Range</span> <span class="data_data">977.6599 - 1,296.975</span> <span class="data_meta">(12/24/18 - 04/29/19)</span>
    outerHighLow = webHTML.find_all('div', attrs={"class":"cr_data_field"})[3]
    innerHighLow = outerHighLow.find('span', attrs = {"class":"data_data"})
    highLow = innerHighLow.text.split("-")
    low = highLow[0][:-1]
    high = highLow[1][1:]
    outputDictionary["52 Week Low"] = low
    outputDictionary["52 Week High"] = high

    #volume example:<span id="quote_volume_48" class="data_data">1,745,450</span>
    volume = webHTML.find('span', attrs={'id':'quote_volume_48'})
    volume = int(volume.text.replace(",",""))
    outputDictionary["Volume"] = volume

    #Price/Earning Ratio: <ul class="cr_data_collection"><li class="cr_data_row cr_data_row-first"> <div class="cr_data_field"> <h5 class="data_lbl">P/E Ratio (TTM)</h5> <span class="data_data"> 24.15 <small class="data_meta">(08/02/19)</small> </span> </div> </li>
    #child has to be treated differently
    outerLayer = webHTML.find_all("ul", attrs = {"class":"cr_data_collection"})[3]
    innerLayers = outerLayer.find_all("span", attrs ={"class":"data_data"})
    priceEarnings = innerLayers[0].text.split(" ")[1]
    outputDictionary["P/E Ratio"] = priceEarnings

    return(outputDictionary)
#end of informationSorter
retrievedData = (informationSorter(webHTML))
