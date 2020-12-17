import requests as req
from bs4 import BeautifulSoup as bs4

def parse_covid():
    url = 'https://2020-koronavirus.ru/goroda/koronavirus-sosnovyj-bor-zabolevshie-koronavirusom-v-sosnovom-boru-poslednie-novosti/'
    session = req.Session()

    get = session.get(url, headers = headers)

    scode = get.status_code
    if scode == 200:
        print('ok')
        soup = bs4(get.content, 'html.parser')
        sbor = soup.find('a', attrs = {'class' : 'btn btn-lg cfa-button1'}).text.split()[0]
        oblzar, oblheal = soup.find_all('div', attrs = {'class' : 'covid-panel-view__stat-item-value1'})[:2]
        return {
        'sbor' : sbor,
        'oblzar' : oblzar.text,
        'oblheal' : oblheal.text
        }

def parsesbor(page):
    url = 'https://sbor.ru/news?start={}'.format(page*6-6)
    session = req.Session()

    get = session.get(url, headers = headers)

    month = [
    'января',
    'февраля',
    'марта',
    'апреля',
    'мая',
    'июня',
    'июля',
    'августа',
    'сентября',
    'октября',
    'ноября',
    'декабря']

    scode = get.status_code
    if scode == 200:
        print('ok')
        soup = bs4(get.content, 'html.parser')

        articles = soup.find_all('div', attrs = {'class' : 'itemContainer itemContainerLast'})

        dates = [article.find('span', attrs = {'class' : 'catItemDateCreated'}).text for article in articles]
        info = [article.find('span', attrs = {'style' : 'font-size: 12px; line-height: 1.3em;'}).text.replace('\t', '').replace('\n', '').replace('\r', '') for article in articles]
        titles = [article.find('h3', attrs = {'class' : 'catItemTitle'}).text.replace('\r', '').replace('\n', '').replace('\t', '') for article in articles]
        images = ['https://sbor.ru' + article.find('img', attrs = {'class' : 'thumb'})['ext'] for article in articles]
        sources = ['https://sbor.ru' + bs4(str(article.find('h3', attrs = {'class' : 'catItemTitle'})), 'html.parser').find('a')['href'] for article in articles]

        for i in range(len(info)):
            info[i] = info[i].replace(dates[i], '')
            
        for i in range(len(dates)):
            print('{:0>2}'.format(month.index(dates[i].split()[1])))
            dates[i] = '.'.join([dates[i].split()[0], '{:0>2}'.format(month.index(dates[i].split()[1])), dates[i].split()[2]])

        articles = []
        for i in range(len(titles)):
            now_set = {
                'title' : titles[i],
                'info' : info[i],
                'date' : dates[i],
                'image' : images[i],
                'source' : sources[i]
            }
            articles += [now_set]
        return articles

def text_of_article(url):

    session = req.Session()

    get = session.get(url, headers = headers)

    scode = get.status_code
    if scode == 200:
        print('ok')
        soup = bs4(get.content, 'html.parser')
        content = soup.find('div', attrs = {'class' : 'news-view-content'})
        print(content)
        if content == None:
            content = soup.find('div', attrs = {'class' : 'ja-content-main clearfix'})
            print(content)

        return content

def parsemysbor(page):
    url = 'https://mysbor.ru/news/?p={}'.format(page*6-6)
    session = req.Session()

    get = session.get(url, headers = headers)

    scode = get.status_code
    if scode == 200:
        print('ok')
        soup = bs4(get.content, 'html.parser')

        articles = soup.find_all('div', attrs = {'class' : 'news-item-content'})[::2]

        dates = [bs4(str(article.find('div', attrs = {'class' : 'date'})), 'html.parser').find('time')['datetime'].split()[0] for article in articles]
        info = [article.find('div', attrs = {'class' : 'anons'}).text.replace('\t', '').replace('\n', '').replace('\r', '') for article in articles]
        titles = [article.find('div', attrs = {'class' : 'title'}).text.replace('\r', '').replace('\n', '').replace('\t', '') for article in articles]
        try:
            images = ['https://mysbor.ru/news' + article.find('img', attrs = {'class' : 'preview'})['src'] for article in articles]
        except:
            images = ['https://lh3.googleusercontent.com/DHjC5tcukdQGKwoW1DxZx1AwgNEZn3r4oUCaW2D_eWGpaRRXgrpr0ObbvD9wYEUNwEk=w600-h300-pc0xffffff-pd' for article in articles]

        sources = ['https://mysbor.ru' + article.find_all('a', attrs = {'class' : 'news-item-a'})[1]['href'] for article in articles]
        # for i in range(len(info)):
        #     info[i] = info[i].replace(dates[i], '')

        articles = []
        for i in range(len(titles)):
            now_set = {
                'title' : titles[i],
                'info' : info[i],
                'date' : dates[i],
                'image' : images[i],
                'source' : sources[i]
            }
            articles += [now_set]
        return articles

headers = {
    'accept' : '*/*'
}

#for debug:
# print(parsesbor(1))
# print(parsemayak(1))
# print(parsemysbor(1))
# print(covid())
# print(text_of_article('https://sbor.ru/news?id=16843'))
# print(parse_all(1))
