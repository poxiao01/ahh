# -*- coding: utf-8 -*-
from src.data.DbAccessor import insert_data, clear_table
from src.data.dependency_parsers import extract_dependency_structure, get_sentences_dependencies_paths
from src.data.loaders import read_sentences_and_questions_from_directory
from src.data.sentence_analyzer import SentenceAnalyzer
from src.utils.file_utils import save_to_txt

if __name__ == '__main__':
    sentences_list, questions_words_list = read_sentences_and_questions_from_directory(
        'E:/python_stanford_NLP/sentence')
    all_words_dependencies_relations, all_words_pos_list, structure_words_and_pos_list, question_words_and_pos_list \
        = extract_dependency_structure(sentences_list, questions_words_list)
    print(len(all_words_dependencies_relations), len(all_words_pos_list), len(structure_words_and_pos_list),
          len(question_words_and_pos_list))
    for index, sentence in enumerate(sentences_list):
        if question_words_and_pos_list[index][0] != questions_words_list[index]:
            print(f'Error：疑问词列表不符合！{index + 1}.{sentence}')

    sentences_dependencies_paths = get_sentences_dependencies_paths(sentences_list, questions_words_list,
                                                                    structure_words_and_pos_list,
                                                                    all_words_dependencies_relations)

    save_to_txt(sentences_list, question_words_and_pos_list, structure_words_and_pos_list, sentences_dependencies_paths,
                all_words_dependencies_relations)

    result_data = []
    for (index, sentence) in enumerate(sentences_list):
        sentenceAnalyzer = SentenceAnalyzer()
        # def analyze_sentence(sentence, question_word_and_pos, structure_word_and_pos, dependency_relations):
        result_data.append(sentenceAnalyzer.analyze_sentence(sentence, question_words_and_pos_list[index],
                                                             structure_words_and_pos_list[index],
                                                             all_words_dependencies_relations[index]))
    # for data in result_data:
    #     print(data)
    insert_data(result_data)
    # print(result_data)
    # clear_table()
