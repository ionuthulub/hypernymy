import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import pymongo
client = pymongo.MongoClient(settings.MONGO_CONNECTION_STRING)
db = client.test

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
    return doc.tokens[0].lemma_


def get_hypernym(word, lang='en'):
    word = word.strip().lower()

    if lang == 'en':
        query = {
            'lemma': word,
            '$or': {
                '$exists': {'lang': False},
                'lang': 'en',
            }
        }
    else:
        query = {
            'lemma': word,
            'lang': lang
        }
    docs = db.hypernyms.find(query)
    hypernyms = set()
    for d in docs:
        hypernyms += set(d['hypernyms'])
    return hypernyms


def homepage(request):
    context = {
        'lang': 'en'
    }

    if request.method == 'POST':
        search_keyword = request.POST['search_keywords']
        lang = request.POST['lang']
        hypernym = get_hypernym(search_keyword, lang=lang)
        context['hyponym'] = search_keyword
        context['hypernym'] = hypernym
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
        'hypernyms': hypernyms
    }
    return HttpResponse(json.dumps(response))
