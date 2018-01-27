import time

import spacy
from spacy import displacy

nlp = spacy.load('en')

print time.time()

doc = nlp(
    u'The cat was a beast.'
    u'The dog was a small animal.'
    u'The dog was animal.'
    u'The dog was in the house.'
    u'The dog and some other pretty animals live happily at the farm.'
    u'Colin and others involved died.'
    u'People\'s property and other people\' lives are complicated.'
    u'He and other rescuers are alive.'
)

hypernyms = dict()

for token in doc:

    # X and/or other Y
    if token.dep_ == 'conj':
        if token.pos_ == 'NOUN' and token.head.pos_ == 'NOUN':
            for c in token.children:
                if c.dep_ == 'amod' and c.lemma_ == 'other':
                    for c in token.head.children:
                        if c.dep_ == 'cc' and c.lemma_ in ['and', 'or']:
                            hypernyms[token.head.lemma_] = token.lemma_

    # X is a Y
    if token.pos_ == 'VERB' and token.lemma_ == 'be':
        for c in token.children:
            if c.dep_ == 'nsubj' and c.pos_ == 'NOUN':
                for c2 in token.children:
                    if c2.dep_ == 'attr' and c2.pos_ == 'NOUN':
                        hypernyms[c.lemma_] = c2.lemma_


# for token in doc:
#     print(token, token.text, token.dep_, token.head, token.head.text, token.head.pos_,
#           [child for child in token.children])

print hypernyms
print time.time()

displacy.serve(doc, style='dep')
