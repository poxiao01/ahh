def save_to_txt(sentences_list, question_words_and_pos_list, structure_words_and_pos_list, dependencies_paths,
                sentences_dependencies_relations):
    """
    将处理后的句子数据写入到文本文件中，包括句子内容、疑问词信息、句型词信息、
    依赖路径以及依赖结构等详情。每部分信息通过换行分隔，便于阅读。

    参数:
    - sentences_list: List[str]，存储所有句子的列表。
    - question_words_and_pos_list: List[Tuple[str, str]]，每个元素为一个元组，包含疑问词及其词性。
    - structure_words_and_pos_list: List[Tuple[str, str]]，每个元素为一个元组，包含句型关键词及其词性。
    - dependencies_paths: List[str]，每个元素为一个句子的依存关系路径字符串。
    - sentences_dependencies_relations: List[List[Tuple[str, List[str]]]]，表示每个句子的依赖关系，
      内部每个元组第一个元素为关系类型，第二个元素为关系所涉及的词语列表。
    """
    with open("E:/python_stanford_NLP/result/RST.txt", "w") as file:
        for index, sentence in enumerate(sentences_list):
            # 写入句子序号及内容
            file.write(f"{index + 1}.{sentence}\n")
            # 写入疑问词及其词性
            file.write(
                f'疑问词：{question_words_and_pos_list[index][0]}, 词性：{question_words_and_pos_list[index][1]}\n')
            # 写入句型词及其词性
            file.write(
                f'句型词：{structure_words_and_pos_list[index][0]}, 词性：{structure_words_and_pos_list[index][1]}\n')
            # 写入依赖路径
            file.write(f'依赖路径：{dependencies_paths[index]}\n')
            # 格式化并写入依赖结构信息
            formatted_relations = '\n '.join(
                [f"{rel[0]}: [{', '.join(rel[1])}]" for rel in sentences_dependencies_relations[index]])
            file.write(f'依赖结构：\n{formatted_relations}\n\n')
    print('文件保存成功！')
