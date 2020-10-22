from bigram_indexing import build_index
from preprocess import english_preprocess


if __name__ == '__main__':
    title_tokens, description_tokens, most_common_word = english_preprocess()
    build_index(title_tokens, "title_bigram", "title")
    build_index(description_tokens, "description_bigram", "description")
