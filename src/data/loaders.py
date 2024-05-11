import os


def read_sentences_and_questions_from_directory(directory_path):
    """
        该函数旨在从给定目录中的所有.txt文件里提取特定格式的句子及其对应的疑问词。
        **重要提示**: 使用前，请确保每个.txt文件内的内容遵循以下格式约定：
            - 每个有效条目由两行组成：第一行为以数字开头的句子，数字后紧跟一个空格和句子内容；
            - 第二行为对应的疑问词，不允许出现某句子无疑问词的情况。
            示例正确格式:
                1 Which countries have more than two official languages?
                countries

        功能描述：
            - 遍历指定目录，读取所有.txt文件。
            - 解析每份文件内容，根据上述格式收集句子和疑问词。
            - 进行句子去重处理，确保返回的句子列表中每一项都是唯一的。

        参数:
            directory_path (str): 指向存放.txt文件的目录路径。

        返回:
            tuple: 一个包含两个元素的元组，第一个元素是去重后的句子列表，第二个元素是疑问词列表。
                   疑问词列表的长度等于句子列表长度。

        示例调用:
            directory_path = 'your/directory/path'
            sentences_list, questions_list = read_sentences_and_questions_from_directory(directory_path)
    """
    sentences_list = []  # 存储所有独特的句子
    question_words_list = []  # 存储所有疑问词
    sentences_set = set()  # 用于去重句子的集合

    # 遍历目录下的所有文件
    for filename in os.listdir(directory_path):
        full_path = os.path.join(directory_path, filename)  # 构建文件的完整路径
        if os.path.isfile(full_path) and filename.endswith('.txt'):  # 确保是txt文件
            with open(full_path, 'r', encoding='utf-8') as file:
                # 逐行读取文件内容
                for line in file:
                    stripped_line = line.strip()  # 去除行首尾空白字符
                    if not stripped_line:  # 跳过空行
                        continue

                    if stripped_line[0].isdigit():  # 判断是否为句子行
                        # 提取句子内容并去重
                        sentence = stripped_line[stripped_line.find(' ') + 1:]
                        if sentence not in sentences_set:
                            sentences_set.add(sentence)
                            sentences_list.append(sentence)
                    else:  # 当前行视为疑问词
                        # 确保疑问词列表不会超过句子的数量
                        if len(question_words_list) < len(sentences_list):
                            question_words_list.append(stripped_line)

    print(f"Total unique sentences: {len(sentences_list)}, Total question words: {len(question_words_list)}")

    return sentences_list, question_words_list

