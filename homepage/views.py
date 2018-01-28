import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import pymongo
client = pymongo.MongoClient(settings.MONGO_CONNECTION_STRING)
db = client.hypernyms

import spacy
nlp_en = spacy.load('en')
nlp_es = spacy.load('es')
nlp_it = spacy.load('it')


def get_lemma(word, lang='en'):
    if lang == 'en':
        doc = nlp_en(unicode(word))
    elif lang == 'es':
        doc = nlp_es(unicode(word))
    elif lang == 'it':
        doc = nlp_it(unicode(word))
    else:
        raise ValueError('language {} not supported'.format(lang))
    return [t.lemma_ for t in doc]


def get_hypernym(words, lang='en'):
    words = [w.strip() for w in words]
    words = reversed(words)

    hypernyms = list()

    for word in words:
        if lang == 'en':
            query = {
                'lemma': word,
                '$or': [
                    {'lang': {'$exists': False}},
                    {'lang': 'en'}
                ]
            }
        else:
            query = {
                'lemma': word,
                'lang': lang
            }
        docs = db.hypernyms.find(query)

        for d in docs:
            for h in d['hypernyms']:
                if h not in hypernyms:
                    hypernyms.append(h)

    return hypernyms


def homepage(request):
    context = {
        'lang': 'en'
    }

    if request.method == 'POST':
        search_keyword = request.POST['search_keywords']
        lang = request.POST['lang']
        lemma = get_lemma(search_keyword, lang=lang)
        hypernyms = get_hypernym(lemma, lang=lang)
        context['hyponym'] = search_keyword
        context['hypernym'] = ', '.join(hypernyms)
        context['lang'] = lang

    return render(request, 'homepage/homepage.html', context)


@csrf_exempt
def hypernymy(request):
    word = json.loads(request.body)['word']
    lang = json.loads(request.body).get('lang', 'en')
    lemma = get_lemma(word, lang=lang)
    hypernyms = get_hypernym(lemma, lang=lang)
    response = {
        'word': word,
        'lemma': lemma,
        'lang': lang,
        'hypernyms': list(hypernyms)
    }
    return HttpResponse(json.dumps(response))
