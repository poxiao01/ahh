import os
import time

import stanza

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
                words_structure = f'句型词： {sent.words[0].text}, 词性: {sent.words[0].xpos}\n'
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
            if len(dependency_paths_result[index]) != 0:
                continue
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
    for sentence in all_sentences_list:
        temp = sentence.split()
        if temp[0] not in word_dict:
            word_dict[temp[0]] = '1'
            test_sentences.append(sentence)
            new_question_words.append(question_words[index])
        index += 1

    question_words = new_question_words
    return test_sentences


if __name__ == "__main__":
    start_time = time.time()
    # 未去除标点符号
    all_sentences_list = read_sentences_to_list('./sentence')
    # all_sentences_list = get_test_sentences(all_sentences_list)
    dependency_result, words_pos_result, words_structure_result = extract_dependency_structure(all_sentences_list)
    dependency_paths_result = []
    same_dependency_result = []
    for index in range(len(dependency_result)):
        dependencyResolver = DependencyResolver(question_words[index], words_structure_result[index],
                                                dependency_result[index], all_sentences_list[index])
        same_dependency, dependency_path = dependencyResolver.get_dependency_paths()
        dependency_paths_result.append(dependency_path)
        same_dependency_result.append(same_dependency)
    all_relations = set()
    for x in dependency_result:
        for relation_and_words in x:
            relation = relation_and_words[0]
            all_relations.add(relation)

    for relation in all_relations:
        print(relation)

    # save_to_txt(all_sentences_list, dependency_result, words_pos_result, words_structure_result, dependency_paths_result)

    end_time = time.time()
    print('执行时间：', end_time - start_time, 's')
