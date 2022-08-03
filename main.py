import requests
from bs4 import BeautifulSoup
import telegram

api_key = '5541825850:AAGldFcgZBndMJ4_g3uasLVWoEloBpQ9mZo'
user_id = '1011416325'

bot = telegram.Bot(token=api_key)


productIDs = ['10332039',
              '13689634',
              ]


class Article:
    def __init__(self, title, price, sale):
        self.title = title
        self.price = price
        self.sale = sale


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
    pre = "https://www.digitec.ch/de/s1/product/"

    return pre+str(articleID)


def buildArticle(url):
    productDetail = getProductDetailFromURL(url)
    title = getTitle(productDetail)
    price = getPrice(productDetail)
    sale = checkIfSaleAndGetOldPrice(productDetail)
    return Article(title, price, sale)


products = []
for p in productIDs:
    art = buildArticle(buildURL(p))
    products.append(art)
    print('Article: ')
    print(art.title)
    print(art.price)
    print(art.sale[0])
    print(art.sale[1])
    print('####################')
    bot.send_message(chat_id=user_id, text='Article: ' + art.title + ' Prix: ' + art.price + ' En stock: ' + str(art.sale[0]))


with open('out.txt', 'w') as f:
    for p in products:
        print('Article: ', file=f)
        print(p.title, file=f)
        print(p.price, file=f)
        print(p.sale[0], file=f)
        print(p.sale[1], file=f)
        print('####################', file=f)

