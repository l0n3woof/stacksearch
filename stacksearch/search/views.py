from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse

import requests
from datetime import datetime, timedelta

# Create your views here.

cache_dict = {}

def search(request):
    global cache_dict
    accepted = request.GET.get('accepted', '').strip()
    answers = request.GET.get('answers', '').strip()
    body = request.GET.get('body', '').strip()
    closed = request.GET.get('closed', '').strip()
    migrated = request.GET.get('migrated', '').strip()
    notice = request.GET.get('notice', '').strip()
    nottagged = request.GET.get('nottagged', '').strip().replace(',', ';')
    tagged = request.GET.get('tagged', '').strip().replace(',', ';')
    title = request.GET.get('title', '').strip()
    user = request.GET.get('user', '').strip()
    url = request.GET.get('url', '').strip()
    views = request.GET.get('views', '').strip()
    wiki = request.GET.get('wiki', '').strip()
    order = request.GET.get('order', 'desc').strip()
    sort = request.GET.get('sort', 'activity').strip()
    pno = request.GET.get('page', 1)
    now = datetime.now()
    shell_life = now + timedelta(hours=4)
    query = 'https://api.stackexchange.com/2.2/search/advanced?order=%s&sort=%s&accepted=%s&answers=%s\
            &body=%s&closed=%s&migrated=%s&notice=%s&nottagged=%s&tagged=%s&title=%s&user=%s&url=%s&views=%s&wiki=%s\
            &site=stackoverflow' %(order, sort, accepted, answers, body, closed, migrated, notice, nottagged, tagged,\
            title, user, url, views, wiki)
    query_prams = order+sort+accepted+answers+body+closed+migrated+notice+nottagged+tagged+title+user+url+views+wiki
    if query_prams in cache_dict:
        if list(cache_dict[query_prams])[0] < now.strftime('%s'):
            resp = requests.get(query).json()['items']
            del cache_dict[query_prams]
            cache_dict[query_prams] = {shell_life.strftime('%s') : resp}
            pages = Paginator(resp, 5)
            return JsonResponse({'page_num':pno, 'number_of_pages':pages.num_pages, 'result':pages.page(pno).object_list})
        else:
            resp = list(cache_dict[query_prams].values())[0]
            pages = Paginator(resp, 5)
            return JsonResponse({'page_num':pno, 'number_of_pages':pages.num_pages, 'result':pages.page(pno).object_list})
    else:
        resp = requests.get(query).json()['items']
        cache_dict[query_prams] = {shell_life.strftime('%s') : resp}
        pages = Paginator(resp, 5)
        return JsonResponse({'page_num':pno, 'number_of_pages':pages.num_pages, 'result':pages.page(pno).object_list})

