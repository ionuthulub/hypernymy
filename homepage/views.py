from django.shortcuts import render


def get_hypernym(word, lang='en'):
    word = word.strip().lower()

    if lang == 'en':
        if word == 'car':
            return 'vehicle'
        if word == 'lion':
            return 'animal'
        if word == 'house':
            return 'building'
    return None


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
