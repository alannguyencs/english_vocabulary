import random

from utils import string_utils


class Sentence:
    def __init__(self, content):
        self.content = content

    def generate_keyword(self, blacklist, length_threshold, size_threshold, max_iterations):
        raw_words = self.content.split()
        words = [string_utils.remove_non_alpha_characters(word) for word in raw_words]

        keyword_id = string_utils.get_keyword_id(words, blacklist, length_threshold, size_threshold, max_iterations)

        if keyword_id < 0:
            return ''

        return string_utils.make_quizlet_formatted_sentence(raw_words, keyword_id)


class Chapter:
    def __init__(self, title, sentences):
        self.title = title
        self.sentences = sentences


class Collection:
    def __init__(self, chapters):
        self.chapters = chapters

    def generate_quizlet(self, chapter_id, num_prev_sentences, num_current_sentences, num_repeat_generate, blacklist, length_threshold, size_threshold, max_iterations):
        learned_sentences = list()
        for i in range(chapter_id):
            learned_sentences.extend(self.chapters[i].sentences)

        current_sentences = self.chapters[chapter_id].sentences

        generated_sentences = list()
        for _ in range(num_repeat_generate):
            formatted_sentences = list()
            for it in range(max_iterations):
                if len(learned_sentences) > num_prev_sentences:
                    learned_sentences = random.sample(learned_sentences, num_prev_sentences)
                if len(current_sentences) > num_current_sentences:
                    current_sentences = random.sample(current_sentences, num_current_sentences)

                formatted_sentences = list()
                for sentence in learned_sentences + current_sentences:
                    formatted_sentences.append(sentence.generate_keyword(blacklist, length_threshold, size_threshold, max_iterations))

                if string_utils.get_percentage_common(formatted_sentences, generated_sentences) == 0:
                    break
            generated_sentences.extend(formatted_sentences)

        return generated_sentences



