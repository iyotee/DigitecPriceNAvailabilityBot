import requests
from bs4 import BeautifulSoup
import telegram
import linecache

api_key = '5541825850:AAGldFcgZBndMJ4_g3uasLVWoEloBpQ9mZo'
user_id = '1011416325'

bot = telegram.Bot(token=api_key)

productIDs = [
              '13689634',
              '13823466',
              '16234727',
              ]

class Article:
    def __init__(self, title, price, sale, availability):
        self.title = title
        self.price = price
        self.sale = sale
        self.availability = availability

def getProductDetailFromURL(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    html = list(soup.children)[1]
    body = list(html.children)[1]
    productDetail = body.find('div', class_='productDetail')

    return productDetail

def getPrice(productDetail):
    childrenDivs = productDetail.findChildren('div', recursive=False)
    priceDiv = childrenDivs[0]
    price = priceDiv.find('strong').getText()

    return price.strip()

def getAvailability(productDetail):
    childrenDivs = productDetail.findChildren('div', recursive=False)
    availability = childrenDivs[4].getText()
    return availability

def checkIfSaleAndGetOldPrice(productDetail):
    sale = [False, 0]
    childrenDivs = productDetail.findChildren('div', recursive=False)
    priceDiv = childrenDivs[0]
    spans = priceDiv.findChildren('span')
    if len(spans) > 1:
        sale[0] = True
        sale[1] = spans[1].getText()[-7:].strip()

    return sale

def getTitle(productDetail):
    header = productDetail.findChildren('h1', recursive=False)
    title = header[0].find('strong').getText()+' '+header[0].find('span').getText()

    return title

def buildURL(articleID):
    pre = "https://www.digitec.ch/fr/s1/product/"

    return pre+str(articleID)

def buildArticle(url):
    productDetail = getProductDetailFromURL(url)
    title = getTitle(productDetail)
    price = getPrice(productDetail)
    sale = checkIfSaleAndGetOldPrice(productDetail)
    availability = getAvailability(productDetail)
    return Article(title, price, sale, availability)

def sendMessage(message):
    bot.send_message(chat_id=user_id, text='Article: ' + message.title + '\n' + 'Prix: ' + message.price +  '\n' + 'En solde: ' + str(message.sale[0]) + ' -> ' + str(message.sale[1]) + '\n' + 'Disponible: ' + message.availability)

# def sendMessageIfChanged (not used anymore)
def sendMessageIfChanged(message):
    bot.send_message(chat_id=user_id, text='Price is now diffenterent from last price' + str(message))
    
def getActualPrices():
    a = 0
    b = 3
    while a <productIDs.__len__():    
        actualPrice = linecache.getline('out.txt', b).strip()
        print("Actual Price article " + str(a) + " -> " + str(actualPrice))
        b+=6
        a+=1

def lineReturn():
    print("\n")

def hashTags():
    print("############################################################")

lineReturn()
getActualPrices()
lineReturn()
hashTags()

products = []
for p in productIDs:
    art = buildArticle(buildURL(p))
    products.append(art)
    print('Article: ' + art.title + '\n' + 'Prix: ' + art.price +  '\n' + 'En solde: ' + str(art.sale[0]) + ' -> ' + str(art.sale[1]) + '\n' + 'Disponible: ' + art.availability)
    hashTags()
    sendMessage(art)

# print(products) in a local file named out.txt ->  The file is opened in "a" mode, which means that the script will append to the file instead of overwriting it every time the script is run (if the file already exists) or create a new file if it doesn't exist yet. This is useful for keeping a log of the script's output. The file is opened in the same directory as the script. The file is closed after the script is finished.
with open('out.txt', 'r+') as f:
    for p in products:
        print('Article: ', file=f)
        print(p.title, file=f)
        print(p.price, file=f)
        print(p.sale[0], file=f)
        print(p.sale[1], file=f)
        print('####################', file=f)


# .translate({ ord(c): None for c in "._!–-" })
