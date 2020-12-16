from django.shortcuts import render
from .parser import parsesbor,covid,text_of_sbor_article
import time as t
# Create your views here.
def home(request):
    #page of news
    num = int(request.GET.get('page', 1))
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
    try:
        articles = parsesbor(num)
    except:
        print('error')
        articles = [{'title' : 'Ошибка сервера',
                    'info' : 'На сервере произошла ошибка и статьи невозможно отобразить...',
                    'date' : t.ctime(),
                    'image' : 'https://ak.picdn.net/shutterstock/videos/1012691939/thumb/1.jpg',
                    'source' : '#'}]

    #covid statistic
    covidstats = covid()

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

def postview(request):
    page = int(request.GET.get('page', 1))
    link = request.GET.get('link')
    text = text_of_sbor_article(link)

    data = {
        'page' : page,
        'link' : link,
        'title' : text['title'],
        'text' : text['text'],
    }
    return render(request, 'home/postview.html', data)
