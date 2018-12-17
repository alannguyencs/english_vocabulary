from random import shuffle
import codecs
import glob
from helper import *

def parse_data_file(file_path):
    data_file = codecs.open(file_path, 'r', 'utf8')
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

            # for ch in stop_words:
            #     sentence = sentence.replace(ch, '')

            key_word = get_valid_words(words)
            if key_word == None:
                continue

            key_id = word_id[key_word]
            raw_list[key_id] = '_____________'
            new_sentence = key_word + '|' + ''.join(raw_list)
            content.append(new_sentence)
    return chapter_title, chapter_content
#==================================================================================

data = glob.glob('./data/*.txt')
collection_name, collection_title, collection_content = [], [], []

for file_path in data:
    file_name = file_path.split('\\')[-1][:-4]
    chapter_title, chapter_content = parse_data_file(file_path)
    collection_name.append(file_name)
    collection_title.append(chapter_title)
    collection_content.append(chapter_content)


#===================================================================================
def show_menu():
    print()
    print("list -- List all chapters")
    print("x y -- "
          "Generate a quizlet set of collection x, chapter number y ")
    print ("quit -- exit the program")

def list_chapters():
    for collection_id, name in enumerate(collection_name):
        print (collection_id, name)
        for chapter_id, title in enumerate(collection_title[collection_id]):
            print('\t' + str(collection_id) + ' ' + str(chapter_id) + ', ' + title)



def generate_quizlet(collection_id = 0, chapter_id=1):
    chapter_title = collection_title[collection_id]
    chapter_content = collection_content[collection_id]
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

        options = option.split(' ')
        if len(options) == 2 and is_int(options[0]) and is_int(options[1]):
            generate_quizlet(collection_id=int(options[0]), chapter_id=int(options[1]))

        if option == 'quit':
            break

        show_menu()

main()