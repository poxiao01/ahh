def check_dependency_equality(struct_word, question_word, sentence_dependency_relations, sentence):
    """
    检查结构词与问题词之间是否存在直接的依存关系。

    :param struct_word: 结构关键词
    :param question_word: 问题关键词
    :param sentence_dependency_relations: 句子的依存关系列表
    :param sentence: 句子文本（当前未使用，但保留以便未来扩展）
    :return: 如果两词存在直接依存关系则返回True，否则返回False
    """
    # 如果结构词和问题词相同，则直接返回True
    if struct_word == question_word:
        return True

    # 遍历依存关系列表，检查是否存在直接关联结构词和问题词的依存关系
    for relation_info in sentence_dependency_relations:
        _, (head_word, word) = relation_info  # 解构依赖关系元组
        # 检查两种情况：问题词是否依赖于结构词，或者结构词是否依赖于问题词
        if (question_word == head_word and struct_word == word) or (question_word == word and struct_word == head_word):
            return True

    # 如果遍历完依存关系列表仍未发现直接关联，则返回False
    return False
