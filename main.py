import os
import time

import stanza

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
            for line in iter_f:  # 遍历文件，一行行遍历，读取文本
                line_num += 1  # 自加1
                if line_num % 3 == 1:
                    line = str(line).strip()  # 删除前后空格
                    line = line.replace("\n", "")  # 删除末尾换行符号
                    for index in range(len(line)):
                        if not line[index].isdigit():
                            line = line[index:]
                            break
                    line = line.strip()
                    if line in sentence_dict:
                        continue
                    sentence_dict[line] = 1
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
    # 初始化Stanza的Pipeline
    nlp = stanza.Pipeline('en', model_dir=custom_dir, download_method=None, processors='tokenize,pos,lemma,depparse',
                          use_gpu=True)
    dependency_result = []
    words_pos_result = []
    for sentence in sentences_list:
        # 去除标点符号
        sentence = sentence.replace(',', ' ')
        doc = nlp(sentence[:-1])
        # 提取依赖结构
        dependency_relations = []
        words_pos = []
        for sent in doc.sentences:
            for word in sent.words:
                head_word = sent.words[word.head - 1].text if word.head > 0 else word.text
                dependency_relations.append((word.deprel, [head_word, word.text]))
                words_pos.append((word.text, word.xpos))

        dependency_result.append(dependency_relations)
        words_pos_result.append(words_pos)

    return dependency_result, words_pos_result


def save_to_txt(sentences_list, dependency_result, words_pos_result):
    with open("./result/RST.txt", "w") as file:
        for index, sentence in enumerate(sentences_list):
            file.write(f"{index + 1}.{sentence}\n")
            file.write(f"疑问词：\n{question_words[index]}\n")
            dependency_relations = dependency_result[index]
            dep_dict = {}  # 用于收集相同类型的依赖关系
            file.write(f'依赖结构：\n')
            for dep_type, dep_info in dependency_relations:
                if dep_type == 'compound':
                    continue
                file.write(f"({dep_type}: {dep_info})\n")
            file.write(f'词性：\n')
            for words_and_pos in words_pos_result[index]:
                file.write(f"{words_and_pos}\n")
            file.write('\n')


def get_test_sentences(sentences_list):
    word_dict = {}
    test_sentences = []
    for sentence in all_sentences_list:
        # if sentence.find('What') != -1 or sentence.find('When') != -1 or sentence.find('Which') != -1 or sentence.find(
        #         'Who') != -1 or sentence.find('How') != -1 or sentence.find('Where') != -1 \
        #         or sentence.find('In which') != -1:
        #     continue
        temp = sentence.split()
        if temp[0] not in word_dict:
            word_dict[temp[0]] = '1'
            test_sentences.append(sentence)
            print(sentence)
    return test_sentences


if __name__ == "__main__":
    start_time = time.time()

    # 未去除标点符号
    all_sentences_list = read_sentences_to_list('./sentence')
    # dependency_result, words_pos_result = extract_dependency_structure(all_sentences_list)
    # save_to_txt(all_sentences_list, dependency_result, words_pos_result)

    test_sentences = get_test_sentences(all_sentences_list)
    dependency_result, words_pos_result = extract_dependency_structure(test_sentences)
    save_to_txt(test_sentences, dependency_result, words_pos_result)

    end_time = time.time()
    print('执行时间：', end_time - start_time, 's')
