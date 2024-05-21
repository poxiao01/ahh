# 设置文件编码为UTF-8，以便支持中文字符显示
# -*- coding: utf-8 -*-

# 导入必要的库
import stanza
from src.data.dependency_parsers import find_structure_word
from src.db.DbAccessor import query_and_save_to_list
from src.models.SentenceDataORM import SentencesDataORM

# 自定义Stanza模型存放路径
custom_dir = "F:\\"  # 请根据实际情况替换为你存放模型的路径

# 初始化Stanza的处理管道
nlp = stanza.Pipeline('en', model_dir=custom_dir, download_method=None,
                      processors='tokenize,pos,lemma,depparse', use_gpu=True)

# 查询数据库并将SentencesDataORM表数据转换为列表
data_list = query_and_save_to_list(SentencesDataORM)


# 定义错误处理函数
def handle_error(data_item, message):
    print(f"错误：{message}\n句子ID: {data_item['ID']}, 句子内容: {data_item['SENTENCE']}\n\n")


# 遍历数据列表，执行数据验证逻辑
for data_item in data_list:
    # 使用Stanza处理句子
    doc = nlp(data_item['SENTENCE'][:-1])

    # 查找句型词
    struct_word, struct_pos = find_structure_word(doc.sentences[0])
    data_item['SENTENCE_STRUCTURE_WORD'] = struct_word

    # 验证句型词是否存在
    if data_item['SENTENCE_STRUCTURE_WORD'] not in data_item['SENTENCE']:
        handle_error(data_item, f"句型词 '{data_item['SENTENCE_STRUCTURE_WORD']}' 未在句子中找到!")

    # 验证疑问词是否存在
    if data_item['QUESTION_WORD'] not in data_item['SENTENCE']:
        handle_error(data_item, f"疑问词 '{data_item['QUESTION_WORD']}' 未在句子中找到!")

    # 验证句型标注
    is_question = data_item['SENTENCE'].endswith('?')
    expected_pattern = '疑问句' if is_question else '陈述句'
    if data_item['SENTENCE_PATTERN'] != expected_pattern:
        handle_error(data_item, "句子句型标注错误!")

    sentence_dependency_list = []

    # 验证疑问词与句型词的标注
    same_dependency = same_qs_word = data_item['QUESTION_WORD'] == data_item['SENTENCE_STRUCTURE_WORD']
    for word in doc.sentences[0].words:
        if word.text == data_item['QUESTION_WORD'] and word.xpos != data_item['QUESTION_WORD_POS']:
            handle_error(data_item, f"疑问词 '{word.text}' 的词性标注错误!")
        if word.text == data_item['SENTENCE_STRUCTURE_WORD'] and data_item['SENTENCE_STRUCTURE_WORD_POS'] != word.xpos:
            handle_error(data_item, f"句型词 '{word.text}' 的词性标注错误!")
        head_word = doc.sentences[0].words[word.head - 1].text if word.head > 0 else word.text
        if (word.text == data_item['SENTENCE_STRUCTURE_WORD'] and head_word == data_item['QUESTION_WORD'] or
                head_word == data_item['SENTENCE_STRUCTURE_WORD'] and word.text == data_item['QUESTION_WORD']):
            same_dependency = True

        sentence_dependency_list.append((word.deprel, [head_word, word.text]))

    # 验证疑问词与句型词是否相同
    if same_qs_word != data_item['SAME_QS_WORD']:
        handle_error(data_item, "SAME_QS_WORD(疑问词与句型词是否相同)字段错误！")

    # 验证疑问词与句型词是否同依赖
    if same_dependency != data_item['SAME_DEPENDENCY']:
        handle_error(data_item, "SAME_DEPENDENCY(疑问词与句型词是否同依赖)字段错误！")

    # 定义所有可能的依存关系类型
    all_relations = [
        'NUMMOD', 'OBL_TMOD', 'ADVCL', 'OBL_AGENT', 'CONJ', 'OBL', 'CC',
        'OBL_NPMOD', 'CC_PRECONJ', 'COP', 'NMOD_POSSESS', 'PUNCT', 'XCOMP',
        'EXPL', 'AUX', 'OBJ', 'ACL', 'CCOMP', 'ACL_RELCL', 'DEP', 'APPOS',
        'NSUBJ_PASS', 'FLAT', 'CASE', 'AMOD', 'ROOT', 'NMOD_NPMOD', 'AUX_PASS',
        'MARK', 'ADVCL_RELCL', 'ADVMOD', 'NMOD', 'IOBJ', 'DET_PREDET', 'FIXED',
        'DET', 'COMPOUND', 'NSUBJ'
    ]

    question_pos_position = dict()
    struct_pos_position = dict()

    for relation in all_relations:
        question_str = 'QUESTION_' + relation
        struct_str = 'SENTENCE_' + relation

        for rel, (head, dep) in sentence_dependency_list:
            rel = rel.upper().replace(':', '_')
            if rel == relation and data_item['QUESTION_WORD'] in (head, dep):
                position = 1 if head == data_item['QUESTION_WORD'] else 2
                question_pos_position[question_str] = position

            if rel == relation and data_item['SENTENCE_STRUCTURE_WORD'] in (head, dep):
                position = 1 if head == data_item['SENTENCE_STRUCTURE_WORD'] else 2
                struct_pos_position[struct_str] = position

        if question_str not in question_pos_position:
            question_pos_position[question_str] = 0
        if struct_str not in struct_pos_position:
            struct_pos_position[struct_str] = 0

    for key, val in question_pos_position.items():
        if val != data_item[key]:
            print(f'{key}:{val}    {data_item[key]}')
            handle_error(data_item, f"{key}(疑问词依赖位置)字段错误！")
    for key, val in struct_pos_position.items():
        if val != data_item[key]:
            handle_error(data_item, f"{key}(句型词依赖位置)字段错误！")