import re
import pandas as pd
import hazm
from collections import Counter


def preprocess_farsi(text):
    prohibitedWords = ['[[', ']]', '{{', '}}', '{|', '|', '*', '==', '=', '\'\'\'' ,'_']
    big_regex = re.compile('|'.join(map(re.escape, prohibitedWords)))
    new_text = big_regex.sub(" ", text)
    # print(new_text)
    ### Remove English characters
    new_text = re.sub(r'[a-zA-Z]','', new_text)
    ### Remove punctuation
    new_text = re.sub(r'[^\w\s]', ' ', new_text)
    normalizer = hazm.Normalizer(remove_extra_spaces=True, persian_style=True, persian_numbers=True, remove_diacritics=True, affix_spacing=True, token_based=False, punctuation_spacing=True)
    new_text = normalizer.normalize(new_text)
    ### Remove numbers
    new_text = re.sub(r'[۱۲۳۴۵۶۷۸۹۰]', ' ', new_text)
    ### Not in HAZM
    # new_text = new_text.replace('گی','ه')
    tokens = hazm.word_tokenize(new_text)
    stemmer = hazm.Stemmer()
    lemmatizer = hazm.Lemmatizer()
    tokens = [word.replace('\u200c', '‌') for word in tokens ]
    tokens = [stemmer.stem(word) for word in tokens]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    tokens = [word for word in tokens if word != '' ]
    return tokens


def find_stopwords(PATH):
    all_text_tokens = []
    all_title_tokens = []
    wikis = pd.read_csv(PATH)
    titles = list(wikis['title'])
    texts = list(wikis['text'])
    processed_texts = []
    processed_titles = []
    for i in range(len(texts)):
        processed_texts.append(preprocess_farsi(texts[i]))
        processed_titles.append(preprocess_farsi(titles[i]))
        all_text_tokens += processed_texts[i]
        all_title_tokens += processed_titles[i]

    all_tokens = all_text_tokens + all_title_tokens
    occurances = dict(Counter(all_tokens))
    stopwords = {k: v for k, v in sorted(occurances.items(), key=lambda item: item[1], reverse=False)}
    most_common = []
    for k in stopwords.keys():
        if stopwords[k] > (0.01 * len(all_tokens)):
            most_common += [k]

    return most_common


def remove_stop_words(tokens, stopwords):
    return [word for word in tokens if word not in stopwords]







