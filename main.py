import processor
import constants


def show_menu():
    print()
    print("list -- List all chapters")
    print("x y -- "
          "Generate a quizlet set of collection x, chapter number y ")
    print("review -- Review learned words")
    print("quit -- exit the program")


def initialize_system(data_dir, approved_extensions, blacklist, length_threshold, size_threshold, max_iterations):
    collection_names, collection_titles, collection_contents = processor.process(data_dir, approved_extensions, blacklist, length_threshold, size_threshold, max_iterations)
    return collection_names, collection_titles, collection_contents


def main():
    data_dir = constants.DATA_DIR
    approved_extensions = constants.APPROVED_FILE_EXTENSIONS
    blacklist = constants.BLACKLIST
    length_threshold = constants.LENGTH_THRESHOLD
    size_threshold = constants.SIZE_THRESHOLD
    max_iterations = constants.MAX_ITERATIONS
    num_prev_sentences = constants.NUM_REVIEWED_SENTENCES
    num_current_sentences = constants.NUM_LEARNED_SENTENCES
    num_repeat_generate = constants.NUM_REPEAT_GENERATE

    collection_names, collection_titles, collection_contents = initialize_system(data_dir, approved_extensions, blacklist, length_threshold, size_threshold, max_iterations)

    while True:
        show_menu()
        option = input("Enter your option: ")
        if option == 'list':
            processor.show_chapter(collection_names, collection_titles)
        elif option == 'review':
            processor.statistic_learned_words()
        elif option == 'quit':
            break
        else:
            options = option.split()
            if len(options) == 2:
                collection_id = options[0]
                chapter_id = options[1]
                if collection_id.isdigit() and chapter_id.isdigit():
                    collection_id = int(collection_id)
                    chapter_id = int(chapter_id)
                    processor.generate_quizlet(collection_names, collection_titles, collection_contents, collection_id, chapter_id, num_prev_sentences, num_current_sentences, num_repeat_generate)


if __name__ == '__main__':
    main()
