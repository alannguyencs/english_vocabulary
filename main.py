from random import shuffle
import codecs
from helper import *


stop_words = "0123456789.,;:!@#'$%^&*()_-=+<>?‘"
data_file = codecs.open('phrase_collection.txt', 'r', 'utf8')
lines = list(data_file)

chapter_title = []
chapter_content = []

# extract data_file
id_line = 0
while id_line < len(lines) and len(lines[id_line]) > 8:
    chapter_title.append(lines[id_line][:-1])
    content = []
    while True:
        id_line += 1
        if lines[id_line][:3] == '---':
            chapter_content.append(content)
            id_line += 1
            break

        sentence = lines[id_line].replace('\n', '').replace('\r', '')
        raw_list, words = [], []
        word_id = {}
        run_id = 0
        run_word = ''
        while(run_id < len(sentence)):
            if sentence[run_id].isalpha():
                run_word += sentence[run_id]
            else:
                raw_list.append(run_word)
                run_word = ''
                raw_list.append(sentence[run_id])
            run_id += 1
        if run_word != '':
            raw_list.append(run_word)
        for raw_id in range(len(raw_list)):
            if raw_list[raw_id].isalpha():
                words.append(raw_list[raw_id])
                word_id[raw_list[raw_id]] = raw_id

        for ch in stop_words:
            sentence = sentence.replace(ch, '')

        key_word = get_valid_words(words)
        if key_word == None:
            continue

        key_id = word_id[key_word]
        raw_list[key_id] = '_____________'
        new_sentence = key_word + '|' + ''.join(raw_list)
        content.append(new_sentence)


#===================================================================================
def show_menu():
    print()
    print("list -- List all chapters")
    print("k -- Generate a quizlet set of chapter number k ")
    print ("quit -- exit the program")

def list_chapters():
    for chapter_id in range(len(chapter_title)):
        print (str(chapter_id) + ', ' + chapter_title[chapter_id])

def generate_quizlet(chapter_id=1):
    #collect questions
    if chapter_id >= len(chapter_title):
        return

    #collect from previous chapters
    out_sentences = []
    for chap_id in range(chapter_id):
        for sentence in chapter_content[chap_id]:
            out_sentences.append(sentence)
    shuffle(out_sentences)
    out_sentences = out_sentences[:5]

    #collect from this chapter
    shuffle(chapter_content[chapter_id])
    out_sentences += chapter_content[chapter_id][:10]


    #generate questions
    print ('\n\n' + chapter_title[chapter_id] + '\n\n')
    for out_sentence in out_sentences:
        print (out_sentence)


def main():
    show_menu()
    while(True):
        option = input("Enter your option: ")
        if option == 'list':
            list_chapters()

        if is_int(option):
            generate_quizlet(chapter_id=int(option))

        if option == 'quit':
            break

        show_menu()

main()