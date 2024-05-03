import string

import stanza

custom_dir = "F:\\"  # 更改为你的自定义路径


# 加载英文模型

def extract_dependency_and_pos(sentences_list):
    """
    提取并解析句子的依存关系结构以及每个词的词性。
    :return: 每个句子的词性与依存关系结构
    """
    # 初始化Stanza的Pipeline
    nlp = stanza.Pipeline('en', model_dir=custom_dir, download_method=None,
                          processors='tokenize,pos,lemma,depparse', use_gpu=True)

    result_with_pos_and_dependency = []
    for sentence in sentences_list:
        # 去除标点符号，这里假设句子以标点结束，根据实际情况调整
        doc = nlp(sentence.rstrip(string.punctuation))

        # 初始化存储该句子词性与依赖关系的数据结构
        sentence_data = {
            'words': [],
            'dependencies': []
        }

        # 提取词性与依赖结构
        for sent in doc.sentences:
            for word in sent.words:
                # 收集词性信息
                pos_info = (word.text, word.xpos)
                sentence_data['words'].append(pos_info)

                # 提取依赖结构
                head_word = sent.words[word.head - 1].text if word.head > 0 else word.text
                dependency_relations = (word.deprel, [head_word, word.text])
                sentence_data['dependencies'].append(dependency_relations)

        result_with_pos_and_dependency.append(sentence_data)

    return result_with_pos_and_dependency


sentence = ['Which companies are in the computer software industry?']
print(extract_dependency_and_pos(sentence))
