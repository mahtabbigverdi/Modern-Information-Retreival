import re
import pandas as pd
import hazm

def preprocess_farsi (text):

    prohibitedWords = ['[[', ']]', '{{', '}}', '{|', '|', '*', '==', '=', '\'\'\'' ,'_']
    big_regex = re.compile('|'.join(map(re.escape, prohibitedWords)))
    new_text = big_regex.sub(" ", text)
    # print(new_text)

    ### Remove English characters
    new_text = re.sub(r'[a-zA-Z]','', new_text)

    ### Remove punctuation
    new_text = re.sub(r'[^\w\s]', ' ', new_text)

    ### Remove numbers
    new_text = re.sub(r'[۱۲۳۴۵۶۷۸۹۰]', ' ', new_text)

    normalizer = hazm.Normalizer(remove_extra_spaces=True, persian_style=True, persian_numbers=True, remove_diacritics=True, affix_spacing=True, token_based=False, punctuation_spacing=True)
    new_text = normalizer.normalize(new_text)

    ### Not in HAZM
    new_text = new_text.replace('گی','ه')

    tokens = hazm.word_tokenize(new_text)
    stemmer = hazm.Stemmer()
    lemmatizer = hazm.Lemmatizer()


    tokens = [stemmer.stem(word) for word in tokens]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    tokens = [word for word in tokens if word != '' ]
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print(tokens)









wikis = pd.read_csv('data/out.csv')
titles = list(wikis['title'])
texts = list(wikis['text'])
preprocess_farsi(texts[0])

