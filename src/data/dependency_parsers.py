import stanza

from src.utils.get_dependency_path_utils import DependencyResolver

custom_dir = "F:\\"  # Stanza NLP模型的自定义目录位置，需替换为实际路径


def extract_dependency_structure(sentences_list, question_words_list):
    """
    分析并提取给定句子列表的依存关系结构，包括句子中每个单词的依存关系、词性信息，
    识别句型起始词及其词性，以及对应疑问词的词性信息。

    参数:
    - sentences_list (list[str]): 待分析的句子列表。
    - question_words_list (list[str]): 每个句子对应的疑问词列表。

    返回:
    tuple: 四个列表的元组，分别包含：
        - 所有句子中单词间的依赖关系列表。
        - 所有句子中每个单词的词性信息列表。
        - 每个句子的句型起始词及其词性信息列表。
        - 疑问词及其词性信息列表。
    """
    # 初始化Stanza的Pipeline，用于英语自然语言处理
    nlp = stanza.Pipeline('en', model_dir=custom_dir, download_method=None,
                          processors='tokenize,pos,lemma,depparse', use_gpu=True)

    # 初始化结果列表
    question_words_and_pos = []  # 存储疑问词及其词性
    structure_words_and_pos = []  # 存储句型起始词及其词性
    all_words_dependencies = []  # 存储所有单词的依存关系
    all_words_pos = []  # 存储所有单词的词性信息

    for index, sentence in enumerate(sentences_list):
        # 使用NLP模型处理句子
        doc = nlp(sentence[:-1])

        # 初始化当前句子的依存关系列表和词性列表
        sentence_dependencies = []
        sentence_words_pos = []

        # 识别句型起始词
        structure_word = find_structure_word(doc.sentences[0])

        # 提取依赖关系和词性信息
        for word in doc.sentences[0].words:
            # 依赖关系处理
            head_word = doc.sentences[0].words[word.head - 1].text if word.head > 0 else word.text
            sentence_dependencies.append(((word.deprel, [head_word, word.text])))

            # 词性信息处理
            sentence_words_pos.append((word.text, word.xpos, word.upos))

            # 确认并记录疑问词及其词性
            if word.text == question_words_list[index] and len(question_words_and_pos) < index + 1:
                question_words_and_pos.append((word.text, word.xpos))
        # 记录句型起始词及其词性
        structure_words_and_pos.append(structure_word)

        # 将当前句子的结果添加到总列表中
        all_words_dependencies.append(sentence_dependencies)
        all_words_pos.append(sentence_words_pos)

    return all_words_dependencies, all_words_pos, structure_words_and_pos, question_words_and_pos


def find_structure_word(sentence):
    """
    根据给定句子识别句型起始词及其词性。

    参数:
    - sentence (stanza.models.common.doc.Sentence): Stanza处理过的句子对象。

    返回:
    tuple: 句型起始词及其词性，或('null', 'null')如果未能识别。
    """
    auxiliary_set = {'who', 'what', 'when', 'which', 'how', 'where', 'whose'}

    # 若句首为动词, 选择句首动词为句型词
    if sentence.words[0].xpos == 'VB':
        return sentence.words[0].text, sentence.words[0].xpos

    for word in sentence.words:
        # 以 auxiliary_set 内的词为句型词
        if word.text.lower() in auxiliary_set:
            return word.text, word.xpos

    # 尝试查找动词作为句型词
    for word in sentence.words:
        if word.xpos.startswith('V'):
            return word.text, word.xpos

    # 最后尝试寻找小写词作为句型词
    for word in sentence.words:
        if word.text.islower():
            return word.text, word.xpos

    return ('null', 'null')  # 无法识别时的默认返回值


def get_sentences_dependencies_paths(sentences_list, questions_words_list, structure_words_and_pos_list,
                                     all_words_dependencies_relations):
    """
    计算并收集每个句子的依赖路径列表。

    此函数遍历给定的句子列表，并为每个句子利用`DependencyResolver`类计算依赖路径，
    然后将这些路径收集到一个列表中返回。依赖路径反映了句型词到疑问词的最短路径。

    :param sentences_list: 句子列表，每个元素是一个字符串。
    :param questions_words_list: 疑问词列表，对应于每个句子的疑问词。
    :param structure_words_and_pos_list: 句型词及其词性列表，每个元素是一个元组，对应于每个句子的句型词和其词性。
    :param all_words_dependencies_relations: 所有单词的依赖关系列表，与句子一一对应，每个元素是该句子的依赖关系列表。
    :return: 二维列表，每个内部列表包含单个句子的所有依赖路径。
    """
    # 初始化存储所有句子依赖路径的列表
    sentences_dependencies_paths = []

    # 遍历句子列表
    for index in range(len(sentences_list)):
        # 创建DependencyResolver实例，用于解析当前句子的依赖关系
        dependency_resolver = DependencyResolver(
            question_word=questions_words_list[index],  # 当前句子的问题词
            structure_word=structure_words_and_pos_list[index][0],  # 当前句子的结构词
            dependency_relations=all_words_dependencies_relations[index],  # 当前句子的依赖关系列表
            sentence=sentences_list[index]  # 当前句子文本
        )

        # 使用DependencyResolver计算依赖路径，并将其添加到结果列表
        sentence_dependency_paths = dependency_resolver.get_dependency_paths()
        sentences_dependencies_paths.append(sentence_dependency_paths)

    # 返回所有句子的依赖路径列表
    return sentences_dependencies_paths


def map_question_word_positions_to_relations(word, dependency_relations):
    """
    映射给定词在各种依存关系中的位置至相应的位置标记列表中。

    该函数遍历给定的依存关系列表，检查给定词是否作为关系的头部词汇或依存词汇出现，
    并记录每种依存关系类型（如'NUMMOD', 'OBL_TMOD'等）中给定词的位置。结果是一个列表，
    列表中的每个元素对应于'all_pos'列表中的一个依存关系类型，值为1表示给定词位于关系的头部，
    值为2表示给定词是依存词汇，值为0表示给定词未出现在该类型的依存关系中。

    :param question_word: str, 分析的目标给定词
    :param dependency_relations: list of tuples, 每个元组包含关系类型和一个元组(头部词汇, 依存词汇)
    :return: list, 给定词在所有可能依存关系类型中的位置标记列表
    """
    # 定义所有可能的依存关系类型
    all_relations = [
        'NUMMOD', 'OBL_TMOD', 'ADVCL', 'OBL_AGENT', 'CONJ', 'OBL', 'CC',
        'OBL_NPMOD', 'CC_PRECONJ', 'COP', 'NMOD_POSSESS', 'PUNCT', 'XCOMP',
        'EXPL', 'AUX', 'OBJ', 'ACL', 'CCOMP', 'ACL_RELCL', 'DEP', 'APPOS',
        'NSUBJ_PASS', 'FLAT', 'CASE', 'AMOD', 'ROOT', 'NMOD_NPMOD', 'AUX_PASS',
        'MARK', 'ADVCL_RELCL', 'ADVMOD', 'NMOD', 'IOBJ', 'DET_PREDET', 'FIXED',
        'DET', 'COMPOUND', 'NSUBJ'
    ]
    # 收集给定词出现的关系及位置信息
    detected_relations = set()

    for rel, (head, dep) in dependency_relations:
        if word in (head, dep):
            position = 1 if head == word else 2
            detected_relations.add((rel.upper().replace(':', '_'), position))

    # 初始化结果列表，根据所有可能的依存关系类型填充
    position_markers = []
    for relation in all_relations:
        if (relation, 1) in detected_relations:
            position_markers.append(1)
        elif (relation, 2) in detected_relations:
            position_markers.append(2)
        else:
            position_markers.append(0)
    return position_markers