


def is_valid_words(words):
    return len(words) > 5

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False