import codecs
import random
import os
from collections import Counter

import constants
from utils import string_utils
from utils import os_utils


def make_quizlet_formatted_sentence(words, keyword_id):
    raw_word = words[keyword_id]
    keyword, punctuation = string_utils.split_ending_punctuation(raw_word)
    words[keyword_id] = '_____________'
    if len(punctuation) > 0:
        words[keyword_id] += ' ' + punctuation
    return keyword + '|' + ' '.join(words)


def parse_data_file(file_path, blacklist, length_threshold, size_threshold, max_iterations):
    chapter_titles = list()
    chapter_contents = list()

    reader = codecs.open(file_path, 'r', 'utf8')

    chapter_content = list()
    for line in reader.readlines():
        # string.strip() is a function which remove whitespace and newline characters from string
        line = line.strip()

        if len(line) == 0:
            continue

        if line.startswith('---'):
            if len(chapter_content) > 0:
                chapter_contents.append(chapter_content)
                chapter_content = list()
            else:
                chapter_titles.pop()
        else:
            if len(chapter_contents) == len(chapter_titles):
                chapter_titles.append(line)
            else:
                raw_words = line.split()
                words = [string_utils.remove_non_alpha_characters(word) for word in raw_words]

                keyword_id = string_utils.get_keyword_id(words, blacklist, length_threshold, size_threshold, max_iterations)

                if keyword_id < 0:
                    continue

                formatted_sentence = make_quizlet_formatted_sentence(raw_words, keyword_id)
                chapter_content.append(formatted_sentence)

    return chapter_titles, chapter_contents


def process(data_dir, approved_extensions, blacklist, length_threshold, size_threshold, max_iterations):
    collection_names = list()
    collection_titles = list()
    collection_contents = list()

    data_files = os_utils.list_files(data_dir, approved_extensions)
    for file_path in data_files:
        chapter_titles, chapter_contents = parse_data_file(file_path, blacklist, length_threshold, size_threshold, max_iterations)
        collection_name = os_utils.get_file_name(file_path)

        collection_names.append(collection_name)
        collection_titles.append(chapter_titles)
        collection_contents.append(chapter_contents)

    return collection_names, collection_titles, collection_contents


def show_chapter(collection_names, collection_titles):
    for collection_id, collection_name in enumerate(collection_names):
        print(collection_id, collection_name)
        for chapter_id, chapter_title in enumerate(collection_titles[collection_id]):
            print('\t' + str(collection_id) + ' ' + str(chapter_id) + ', ' + chapter_title)


def show_contents(collection_names, collection_titles, collection_contents):
    for collection_id, collection_name in enumerate(collection_names):
        print(collection_name)
        for chapter_id, chapter_title in enumerate(collection_titles[collection_id]):
            print('\t' + chapter_title)
            for sentence in collection_contents[collection_id][chapter_id]:
                print('\t\t' + sentence)


def generate_quizlet(collection_names, collection_titles, collection_contents, collection_id, chapter_id, num_prev_sentences, num_current_sentences):
    if collection_id < 0 or chapter_id < 0:
        print('Error!!! ID of a collection or chapter must be a positive integer!')
        return

    if collection_id >= len(collection_titles):
        print('Error!!! We only have ' + str(len(collection_titles)) + ' collections')
        return

    collection_name = collection_names[collection_id]
    chapter_titles = collection_titles[collection_id]
    chapter_contents = collection_contents[collection_id]

    if chapter_id >= len(chapter_titles):
        print('Error!!! The collection ' + collection_name + ' only have ' + str(len(chapter_titles)) + ' chapters')
        return

    chapter_title = chapter_titles[chapter_id]
    chapter_content = chapter_contents[chapter_id]

    sentences = list()
    for prev_chapter_id in range(chapter_id):
        for sentence in chapter_contents[prev_chapter_id]:
            sentences.append(sentence)
    if len(sentences) > num_prev_sentences:
        sentences = random.sample(sentences, num_prev_sentences)
    chosen_sentences = sentences

    sentences = chapter_content
    if len(sentences) > num_current_sentences:
        sentences = random.sample(sentences, num_current_sentences)
    chosen_sentences.extend(sentences)

    # generate questions
    print('\n\n' + chapter_title + '\n\n')
    for sentence in chosen_sentences:
        print(sentence)
    save_content(chosen_sentences, collection_id, chapter_id)


def save_content(content, collection_id, chapter_id, stored_dir=None):
    if stored_dir is None:
        stored_dir = constants.DEFAULT_STORED_LESSONS_DIR
    if not os.path.exists(stored_dir):
        os.makedirs(stored_dir)

    stored_file = str(collection_id) + '_' + str(chapter_id) + constants.CONTENT_EXTENSION
    stored_file = os.path.join(stored_dir, stored_file)

    writer = os_utils.create_writer(stored_file)
    for sentence in content:
        writer.write(sentence + '\n')
    writer.close()


def statistic_learned_words(stored_dir=None, backup_dir=None):
    if stored_dir is None:
        stored_dir = constants.DEFAULT_STORED_LESSONS_DIR
    if backup_dir is None:
        backup_dir = constants.DEFAULT_BACKUP_DIR

    content_files = os_utils.list_files(stored_dir, constants.CONTENT_EXTENSION, backup_dir)
    learned_words = list()
    for f in content_files:
        for line in open(f, 'r'):
            line = line.strip()
            keyword, sentence = line.split('|')
            learned_words.append(keyword)
    word_counter = Counter(learned_words)
    print('Learned Words:')
    for word in sorted(word_counter.items(), key=lambda x: x[1], reverse=True):
        print(word[0] + '\t' + str(word[1]))
