import os
import time

import stanza
from insert import insert_data
from Data.SentenceDataORM import SentenceDataORM
from DependencyResolver import DependencyResolver

custom_dir = "F:\\"  # 更改为你的自定义路径
# stanza.download('en', model_dir=custom_dir)

question_words = []
sentence_dict = dict()


def read_sentences_to_list(path):
    """读取sentence目录下所有txt里的句子并返回
    :return: 读取后的结果
    """
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    sentences_list = []  # 句子集合
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            f = open(path + "/" + file, encoding='utf-8')  # 打开文件
            iter_f = iter(f)  # 创建迭代器
            line_num = 0  # 行数
            flag = False
            for line in iter_f:  # 遍历文件，一行行遍历，读取文本
                line_num += 1  # 自加1
                if flag:
                    flag = False
                    continue

                if line_num % 3 == 1:
                    line = str(line).strip()  # 删除前后空格
                    line = line.replace("\n", "")  # 删除末尾换行符号
                    for index in range(len(line)):
                        if not line[index].isdigit():
                            line = line[index:]
                            break
                    line = line.strip()
                    if line in sentence_dict:
                        flag = True
                        continue
                    sentence_dict[line] = '1'
                    sentences_list.append(line)
                elif line_num % 3 == 2:
                    question_words.append(line.strip())
            f.close()
    return sentences_list


def extract_dependency_structure(sentences_list):
    """
    提取并解析句子的依存关系结构。
    :return: 句子的依存关系结构
    """
    global question_words
    # 初始化Stanza的Pipeline
    nlp = stanza.Pipeline('en', model_dir=custom_dir, download_method=None, processors='tokenize,pos,lemma,depparse',
                          use_gpu=True)
    dependency_result = []
    words_pos_result = []
    words_structure_result = []

    index = 0
    for sentence in sentences_list:
        # 去除标点符号
        sentence = sentence.replace(',', ' ')
        doc = nlp(sentence[:-1])

        # 提取依赖结构
        dependency_relations = []
        words_pos = []
        words_structure = ''
        for sent in doc.sentences:
            for word in sent.words:
                head_word = sent.words[word.head - 1].text if word.head > 0 else word.text
                dependency_relations.append((word.deprel, [head_word, word.text]))
                words_pos.append((word.text, word.xpos, word.upos))
                # print(word)
                if word.text == question_words[index]:
                    question_words[index] = f'疑问词：{word.text}, 词性：{word.xpos}\n'

            if sent.words[0].xpos.find('W') != -1 and sent.words[0].xpos != 'FW':
                words_structure = f'句型词： {sent.words[0].text}, 词性： {sent.words[0].xpos}\n'
            else:
                ok = False
                for word in sent.words:
                    if word.xpos == 'FW': continue
                    if word.xpos.find('W') != -1 and word.text.lower() != 'that':
                        ok = True
                        words_structure = f'句型词：{word.text}, 词性：{word.xpos}\n'
                        break

                if not ok:
                    for word in sent.words:
                        if word.xpos.find('V') != -1:
                            words_structure = f'句型词：{word.text}, 词性：{word.xpos}\n'
                            ok = True
                            break

                if not ok:
                    for word in sent.words:
                        if word.text.islower():
                            words_structure = f'句型词：{word.text}, 词性：{word.xpos}\n'
                            ok = True
                            break

                if not ok:
                    words_structure = f'句型词：Null, 词性：Null\n'
        dependency_result.append(dependency_relations)
        words_pos_result.append(words_pos)
        words_structure_result.append(words_structure)
        index += 1

    return dependency_result, words_pos_result, words_structure_result


def save_to_txt(sentences_list, dependency_result, words_pos_result, words_structure_result, dependency_paths_result):
    global question_words
    temp_dict = {}
    number = 0
    with open("./result/RST.txt", "w") as file:
        for index, sentence in enumerate(sentences_list):
            # if len(dependency_paths_result[index]) != 0:
            #     continue
            # # ----------------------------------
            # begin_position = words_structure_result[index].find('：')  # 找到第一个':'的位置
            # end_position = words_structure_result[index].find(',')  # 找到第一个','的位置
            # temp = words_structure_result[index][begin_position + 1: end_position]  # 从冒号之后的字符开始取到字符串结束
            # temp = temp.strip()
            # if temp in temp_dict:   continue
            # temp_dict[temp] = 1
            # # ----------------------------------
            # print(temp)
            number += 1
            file.write(f"{number}.{sentence}\n")
            file.write(question_words[index])
            file.write(words_structure_result[index])
            file.write(f'依赖路径：{dependency_paths_result[index]}\n')
            file.write(f'依赖结构：\n')
            for dep_type, dep_info in dependency_result[index]:
                # if dep_type == 'compound':
                #     continue
                file.write(f"({dep_type}: {dep_info})\n")
            # file.write(f'全部单词词性：\n')
            # for words_and_pos in words_pos_result[index]:
            #     file.write(f"{words_and_pos}\n")
            file.write('\n')


def get_test_sentences(sentences_list):
    global question_words
    word_dict = {}
    test_sentences = []
    new_question_words = []
    index = 0
    for sentence in sentences_list:
        temp = sentence.split()
        if temp[0] not in word_dict:
            word_dict[temp[0]] = '1'
            test_sentences.append(sentence)
            new_question_words.append(question_words[index])
        index += 1

    question_words = new_question_words
    return test_sentences


def get_dependency_results_and_same_dependency_result(words_structure_result, dependency_result, all_sentences_list):
    global question_words
    dependency_paths_result = []
    for index in range(len(dependency_result)):
        dependencyResolver = DependencyResolver(question_words[index], words_structure_result[index],
                                                dependency_result[index], all_sentences_list[index])
        dependency_path = dependencyResolver.get_dependency_paths()
        dependency_paths_result.append(dependency_path)
    return dependency_paths_result


def get_word_from_str(s):
    return s[s.find('：') + 1: s.find(',')].strip()  # 从冒号之后的字符开始取到字符串结束


def get_word_pos_from_str(s):
    # 查找第一个和第二个冒号的位置
    first_colon_pos = s.find('：')
    if first_colon_pos == -1:  # 如果没有找到第一个冒号，返回原字符串
        return s

    second_colon_pos = s.find('：', first_colon_pos + 1)
    if second_colon_pos == -1:  # 如果没有找到第二个冒号，返回从第一个冒号后到字符串结束的部分
        return s[first_colon_pos + 1:]

    # 保留第二个冒号之后的部分
    return s[second_colon_pos + 1:].strip()


def check_dependency_equality(struct_word_str, question_word_str, dependency_words, sentence):
    struct_word = get_word_from_str(struct_word_str)
    question_word = get_word_from_str(question_word_str)
    if struct_word == question_word: return False
    for relation, words in dependency_words:
        head_word, word = words
        if question_word == head_word and struct_word == word or question_word == word and struct_word == head_word:
            return True
    return False


def get_all_question_word_pos(question_word, dependency_relations_and_words):
    all_pos = [
        'NUMMOD', 'OBL_TMOD', 'ADVCL', 'OBL_AGENT', 'CONJ', 'OBL', 'CC',
        'OBL_NPMOD', 'CC_PRECONJ', 'COP', 'NMOD_POSSESS', 'PUNCT', 'XCOMP',
        'EXPL', 'AUX', 'OBJ', 'ACL', 'CCOMP', 'ACL_RELCL', 'DEP', 'APPOS',
        'NSUBJ_PASS', 'FLAT', 'CASE', 'AMOD', 'ROOT', 'NMOD_NPMOD', 'AUX_PASS',
        'MARK', 'ADVCL_RELCL', 'ADVMOD', 'NMOD', 'IOBJ', 'DET_PREDET', 'FIXED',
        'DET', 'COMPOUND', 'NSUBJ'
    ]
    have_relations = set()
    for relation_and_words in dependency_relations_and_words:
        relation, (head_word, word) = relation_and_words
        if word == question_word or head_word == question_word:
            have_relations.add(relation.upper().replace(':', '_'))
    # print(have_relations)
    result = []
    for relation in all_pos:
        if relation in have_relations:
            result.append(True)
        else:
            result.append(False)
    return result


if __name__ == "__main__":
    start_time = time.time()
    # 未去除标点符号
    all_sentences_list = read_sentences_to_list('./sentence')
    # all_sentences_list = get_test_sentences(all_sentences_list)
    # 依赖结构              疑问词及词性         句型词及词性
    dependency_result, words_pos_result, words_structure_result = extract_dependency_structure(all_sentences_list)
    dependency_paths_result = (
        get_dependency_results_and_same_dependency_result(words_structure_result, dependency_result,
                                                          all_sentences_list))
    # print(dependency_paths_result)
    save_to_txt(all_sentences_list, dependency_result, words_pos_result, words_structure_result,
                dependency_paths_result)

    data_list = []
    for index in range(len(all_sentences_list)):
        temp_list = []

        # 句子
        temp_list.append(all_sentences_list[index])

        # 是否同依赖
        temp_list.append(check_dependency_equality(words_structure_result[index], question_words[index], dependency_result[index], all_sentences_list[index]))

        # 依赖路径
        dependencyResolver = DependencyResolver(question_words[index], words_structure_result[index],
                                                dependency_result[index], all_sentences_list[index])
        temp_list.append(dependencyResolver.get_dependency_paths())

        # 句子类型(疑问句 or 陈述句)
        temp_list.append('疑问句' if all_sentences_list[index][-1] == '?' else '陈述句')

        # 句型词
        temp_list.append(get_word_from_str(words_structure_result[index]))

        # 句型词词性
        temp_list.append(get_word_pos_from_str(words_structure_result[index]))

        # 疑问词词性
        temp_list.append(get_word_pos_from_str(question_words[index]))

        # 返回值(1, 0, 0, 1, ...) 表示疑问词是否存在第i个依赖关系中
        all_relations_pos = get_all_question_word_pos(get_word_from_str(question_words[index]), dependency_result[index])
        for pos in all_relations_pos: temp_list.append(pos)

        data_list.append(temp_list)
        sentece_data = SentenceDataORM()
        sentece_data.create_sentence_data_from_list(temp_list)
        # print(sentece_data)

    insert_data(data_list)
    end_time = time.time()
    print('执行时间：', end_time - start_time, 's')
