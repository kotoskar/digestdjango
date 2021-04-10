import requests as req
from bs4 import BeautifulSoup as bs4

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
        print('sbor - ok')
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
            dates[i] = '.'.join([dates[i].split()[0], '{:0>2}'.format(month.index(dates[i].split()[1])), dates[i].split()[2]])

        articles = []
        for i in range(len(titles)):
            now_set = {
                'title' : titles[i],
                'info' : info[i],
                'date' : dates[i],
                'image' : images[i],
                'source' : sources[i],
                'from' : '"Официальный сайт города Сосновый Бор"'
            }
            articles += [now_set]
        return articles

def parsemysbor(page):
    url = 'https://mysbor.ru/news/?p={}'.format(page*6-6)
    session = req.Session()

    get = session.get(url, headers = headers)

    scode = get.status_code
    if scode == 200:
        print('mysbor - ok')
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
                'source' : sources[i],
                'from' : '"Мой Сосновый Бор"'
            }
            articles += [now_set]
        return articles

def parse_events():
    url = 'https://www.sbdks.ru/afisha'

    session = req.Session()

    get = session.get(url, headers = headers)

    scode = get.status_code
    if scode == 200:
        print('events - ok')
        soup = bs4(get.content, 'html.parser')

        events = soup.find_all('li', attrs = {'class' : '_3TBOu _1UgL3'})
        titles = []
        for event in events:
            try:
                titles += [event.find('a', attrs = {'class' : 'r52AK'}).text]
            except:
                titles += [event.find('div', attrs = {'class' : '_1pdZF'}).text]
        info = [event.find('div', attrs = {'class' : '-JBHS'}).text.replace('\t', '').replace('\n', '').replace('\r', '') for event in events]
        images = ['https://static.wixstatic.com/media/4bd6fa_d30ef15b2c134ffdb07261330ee56cdd~mv2.png/v1/crop/x_174,y_0,w_2653,h_2483/fill/w_143,h_137,al_c,q_85,usm_0.66_1.00_0.01/%D1%8D%D0%BC%D0%B1%D0%BB%D0%B5%D0%BC%D0%B0_%D0%94%D0%9A.webp' for event in events]
        dates = [event.find('div', attrs = {'class' : '_3x_-L'}).text.replace('\t', '').replace('\n', '').replace('\r', '') for event in events]
        places = [event.find('div', attrs = {'class' : '_2-GKu'}).text.replace('\t', '').replace('\n', '').replace('\r', '') for event in events]
        sources = []
        for event in events:
            try:
                sources += [event.find('a', attrs = {'class' : 'r52AK'})['href']]
            except:
                sources += ['https://www.sbdks.ru/afisha']

        events = []
        for i in range(len(titles)):
            now_set = {
                'title' : titles[i],
                'info' : info[i],
                'image' : images[i],
                'date' : dates[i],
                'place' : places[i],
                'source' : sources[i],
                'from' : '"Дворец культуры "Строитель""'
            }
            events += [now_set]
        return events

headers = {
    'accept' : '*/*'
}
