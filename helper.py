from random import randint

def is_valid_key_word(key_word):
    if len(key_word) < 3:
        return False
    black_list = ['doesn', 'can', 'isn', 'aren']
    if key_word in black_list:
        return False
    return True

def get_valid_words(words):
    key_word = None
    if len(words) <= 5:
        return key_word
    cnt_loop = 0
    while (True):
        blank_id = randint(0, len(words) - 1)
        key_word = words[blank_id]
        if is_valid_key_word(key_word):
            break
        cnt_loop += 1
        if cnt_loop > 49:
            return key_word
    return key_word



def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False