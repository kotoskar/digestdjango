from django.shortcuts import render
from .parser import parsesbor,parse_covid,parsemysbor,parse_events
import time as t
import threading as td
# Create your views here.
def parse_all(num):
    def sborfun(page):
        global sbor
        sbor = parsesbor(page)
    def mysborfun(page):
        global mysbor
        mysbor = parsemysbor(page)
    def covidfun():
        global covid
        covid = parse_covid()
    threads = [
        td.Thread(target = sborfun, name = sborfun, args = [num]),
        td.Thread(target = mysborfun, name = mysborfun, args = [num]),
        td.Thread(target = covidfun, name = covidfun)]

    for thread in threads:
        thread.start()

    while True in [thread.is_alive() for thread in threads]:
        pass

    output = {
        'sbor' : sbor,
        'mysbor' : mysbor,
        'covid' : covid
    }

    return output

def gen_pages(num):
    if num<1:
        num = 1
    pages = []
    count = 0
    ind = -2
    while count != 5:
        if num + ind>0:
            pages += [num+ind]
            count += 1
        ind += 1
    return pages

def home(request):
    #page of news
    num = int(request.GET.get('page', 1))
    if num<1:
        num = 1
    pages = gen_pages(num)
    response = parse_all(num)
    try:
        articles = sorted(response['mysbor'] + response['sbor'], key = lambda x: ''.join(x['date'].split('.')[::-1]), reverse = True)
    except:
        print('error')
        articles = [{'title' : 'Ошибка сервера',
                    'info' : 'На сервере произошла ошибка и статьи невозможно отобразить...',
                    'date' : t.ctime(),
                    'image' : 'https://ak.picdn.net/shutterstock/videos/1012691939/thumb/1.jpg',
                    'source' : '#'}]

    #covid statistic
    covidstats = response['covid']

    data = {
        'title' : 'Новости',
        'news' : articles,
        'pages' : pages,
        'num' : num,
        'pre_num' : num-1,
        'next_num' : num+1,
        'sbor' : covidstats['sbor'],
        'oblzar' : covidstats['oblzar'],
        'oblheal' : covidstats['oblheal']
    }

    return render(request, 'home/main.html', data)

def events(request):
    num = int(request.GET.get('page', 1))
    if num<1:
        num = 1
    pages = gen_pages(num)
    covidstats = parse_covid()
    events = parse_events

    data = {
        'num' : num,
        'pre_num' : num-1,
        'next_num' : num+1,
        'pages' : pages,
        'title' : 'Афиша',
        'sbor' : covidstats['sbor'],
        'oblzar' : covidstats['oblzar'],
        'oblheal' : covidstats['oblheal'],
        'events' :  events
    }

    return render(request, 'home/events.html', data)
