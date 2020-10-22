import pickle


def build_index(tokens, filename, which):
    bigram_dict = {}
    token_count = {}
    for token in tokens:
        for t in token:
            add_to_token_count(t, token_count)
            t_new = '$' + t + '$'
            for i in range(len(t_new) - 1):
                new_key = t_new[i] + t_new[i + 1]
                if new_key in bigram_dict.keys():
                    bigram_dict[new_key].add(t)
                else:
                    bigram_dict[new_key] = {t}
    save(filename, bigram_dict)
    save(which + "_token_count", token_count)


def add_to_token_count(t, token_count):
    if t in token_count.keys():
        token_count[t] += 1
    else:
        token_count[t] = 1


def save(filename, index):
    with open(filename, 'wb') as handle:
        pickle.dump(index, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read(filepath):
    with open(filepath, 'rb') as handle:
        index = pickle.load(handle)
    return index


def add_doc(new_doc, filename, which):
    bigram_index = read(filename)
    token_count = read(which + "_token_count")
    for token in new_doc:
        add_to_token_count(token, token_count)
        t_new = '$' + token + "$"
        for i in range(len(t_new) - 1):
            new_key = t_new[i] + t_new[i + 1]
            if new_key in bigram_index.keys():
                bigram_index[new_key].add(token)
            else:
                bigram_index[new_key] = {token}
    save(filename, bigram_index)
    save(which + "_token_count", token_count)


def delete_doc(doc, filename, which):
    bigram_index = read(filename)
    token_count = read(which + "_token_count")
    for token in doc:
        try:
            token_count[token] -= 1
            t_new = '$' + token + "$"
            for i in range(len(t_new) - 1):
                new_key = t_new[i] + t_new[i + 1]
                if token_count[token] == 0:
                    bigram_index[new_key].remove(token)
            if token_count[token] == 0:
                del token_count[token]
        except Exception:
            print("doc has not been added to the system")
    save(filename, bigram_index)
    save(which + "_token_count", token_count)


# print(read("title_bigram"))
# print(read("title_token_count"))
# # add_doc(['school', 'kill', 'avert', 'climat'], "title_bigram", "title")
# # delete_doc(['school', 'kill', 'avert', 'climat'], "title_bigram", "title")
# print(read("title_bigram"))
# print(read("title_token_count"))
# if "avert" in read("title_bigram")['$a']:
#     print("yohoooooo")
# else:
#     print("nohooooo")
