import requests as req
from bs4 import BeautifulSoup as bs4

def covid():
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

    scode = get.status_code
    if scode == 200:
        print('ok')
        soup = bs4(get.content, 'html.parser')

        articles = soup.find_all('div', attrs = {'class' : 'itemContainer itemContainerLast'})

        titles = [article.find('h3', attrs = {'class' : 'catItemTitle'}).text for article in articles]
        info = [article.find('span', attrs = {'style' : 'font-size: 12px; line-height: 1.3em;'}).text for article in articles]
        dates = [article.find('span', attrs = {'class' : 'catItemDateCreated'}).text for article in articles]
        images = ['https://sbor.ru/' + article.find('img', attrs = {'class' : 'thumb'})['ext'] for article in articles]
        sources = ['https://sbor.ru' + bs4(str(article.find('h3', attrs = {'class' : 'catItemTitle'})), 'html.parser').find('a')['href'] for article in articles]

        for i in range(len(info)):
            info[i] = info[i].replace(dates[i], '')
            info[i] = info[i].replace('\t', '')
            info[i] = info[i].replace('\n', '')
            info[i] = info[i].replace('\r', '')

        for i in range(len(titles)):
            titles[i] = titles[i].replace('\t', '')
            titles[i] = titles[i].replace('\n', '')
            titles[i] = titles[i].replace('\r', '')

            # articles = list(zip(titles,info,dates,images,sources))
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

def text_of_sbor_article(url):

    session = req.Session()

    get = session.get(url, headers = headers)

    scode = get.status_code
    if scode == 200:
        print('ok')
        soup = bs4(get.content, 'html.parser')
        title = soup.find('h2', attrs = {'class' : 'itemTitle'}).text
        text = soup.find('div', attrs = {'class' : 'itemBody'}).text.replace('\xa0', '\n')

        return {'title' : title,
                'text' : text}

def parsemayak(page):
    # FIXME:
    # FIXME:
    # FIXME:
    url = 'https://mayaksbor.ru/news/?PAGEN_2={}'.format(page)
    session = req.Session()

    get = session.get(url, headers = headers)

    scode = get.status_code
    if scode == 200:
        print('ok')
        soup = bs4(get.content, 'html.parser')

        articles = soup.find_all('div', attrs = {'class' : 'col-xs-12 col-sm-6 col-md-3 col-lg-3 article__module article__block__img'})
        print(articles)

        info = [article.find('div', attrs = {'class' : 'col-xs-12 col-sm-6 col-md-3 col-lg-3 article__module article__block__img'}).text for article in articles]
        dates = [article.find('div', attrs = {'class' : 'news__list__item-desc-time'}).text for article in articles]
        images = ['https://mayaksbor.ru/' + article.find('img', attrs = {'class' : 'news__list__item-bg'})['href'] for article in articles]


        for i in range(len(info)):
            info[i] = info[i].replace(dates[i], '')
            info[i] = info[i].replace('\t', '')
            info[i] = info[i].replace('\n', '')
            info[i] = info[i].replace('\r', '')
            info[i] = info[i].strip()
            # articles = list(zip(titles,info,dates,images,sources))
        articles = []
        for i in range(len(info)):
            now_set = {
                'title' : '',
                'info' : info[i],
                'date' : dates[i],
                'image' : images[i],
                'source' : url
            }
            articles += [now_set]
        return articles
# def parsecinema():
#     url = 'http://www.sovremennik.sbor.net/#/seans/'
#     session = req.Session()
#     try:
#         get = session.get(url, headers = headers)
#     except Exception:
#         print('An error of URL')
#     else:
#         scode = get.status_code
#         if scode == 200:
#             print('ok')
#             soup = bs4(get.content, 'html.parser').prettify()
#             print(soup)
headers = {
    'accept' : '*/*'
}

#for debug:
# print(parsesbor(1))
# print(parsemayak(1))
# print(covid())
# print(text_of_sbor_article('https://sbor.ru/news?id=16843'))
