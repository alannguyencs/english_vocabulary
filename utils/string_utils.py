import string
import random


def is_valid_keyword(candidate_word, blacklist, length_threshold):
    return not (len(candidate_word) < length_threshold or candidate_word in blacklist)


def get_keyword_id(words, blacklist, length_threshold, size_threshold, max_iterations):
    num_words = len(words)
    if num_words <= size_threshold:
        return -1

    keyword_id = -1
    for _ in range(max_iterations):
        # random.sample is a function which chooses randomly one element in a given list
        candidate_id = random.choice(range(num_words))

        candidate_word = words[candidate_id]
        if is_valid_keyword(candidate_word, blacklist, length_threshold):
            keyword_id = candidate_id
            break

    return keyword_id


def remove_non_alpha_characters(text):
    return ''.join(c for c in text if c.isalpha())


def split_ending_punctuation(word):
    pos = len(word)
    for i in range(len(word) - 1, -1, -1):
        if word[i].isalpha():
            pos = i + 1
            break
    return word[:pos], word[pos:]


def main():
    print(split_ending_punctuation(' 1b2sc,,..'))


if __name__ == '__main__':
    main()
