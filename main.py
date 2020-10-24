from bigram_indexing import build_index
from preprocess import *


if __name__ == '__main__':
    titles, descriptions, most_common_english = find_most_common_words()
    title_tokens = parse_all_docs(titles, most_common_english)
    description_tokens = parse_all_docs(descriptions, most_common_english)
    build_index(title_tokens, "title_bigram", "title")
    build_index(description_tokens, "description_bigram", "description")
