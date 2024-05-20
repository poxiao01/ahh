from src.data.dependency_parsers import map_question_word_positions_to_relations
from src.utils.dependency_comparison_utils import check_dependency_equality
from src.utils.get_dependency_path_utils import DependencyResolver


class SentenceAnalyzer:
    @staticmethod
    def analyze_sentence(sentence, question_word_and_pos, structure_word_and_pos, dependency_relations):
        """
        分析句子类型、词性等信息
        :param sentence: 待分析的句子
        :param question_word_and_pos: 疑问词及其词性
        :param structure_word_and_pos: 句型词及其词性
        :param dependency_relations: 依赖关系
        :return: 分析结果列表
        """
        result_list = []

        # 句子
        result_list.append(sentence)

        # 疑问词与句型词是否相同
        result_list.append(question_word_and_pos[0] == structure_word_and_pos[0])

        # 是否同依赖
        result_list.append(
            check_dependency_equality(structure_word_and_pos[0], question_word_and_pos[0], dependency_relations,
                                      sentence))

        # 依赖路径
        dependency_resolver = DependencyResolver(
            question_word=question_word_and_pos[0],  # 当前句子的问题词
            structure_word=structure_word_and_pos[0],  # 当前句子的结构词
            dependency_relations=dependency_relations,  # 当前句子的依赖关系列表
            sentence=sentence  # 当前句子文本
        )
        sentence_dependency_paths = dependency_resolver.get_dependency_paths()
        result_list.append(sentence_dependency_paths)

        # 句子类型(疑问句 or 陈述句)
        result_list.append('疑问句' if sentence[-1] == '?' else '陈述句')

        # 句型词
        if structure_word_and_pos[1] == 'VB':
            result_list.append('VB')
        else:
            result_list.append('How many' if structure_word_and_pos[0] == 'How' and sentence.find('How many') != -1 else
                               structure_word_and_pos[0])

        # 句型词词性
        result_list.append(structure_word_and_pos[1])

        # 疑问词
        result_list.append(question_word_and_pos[0])

        # 疑问词词性
        result_list.append(question_word_and_pos[1])

        # 句型词在依赖关系中的位置
        structure_word_dependency_positions = map_question_word_positions_to_relations(structure_word_and_pos[0],
                                                                                       dependency_relations)
        for positions in structure_word_dependency_positions:
            result_list.append(positions)

        # 疑问词在依赖关系中的位置
        question_word_dependency_positions = map_question_word_positions_to_relations(question_word_and_pos[0],
                                                                                      dependency_relations)
        for positions in question_word_dependency_positions:
            result_list.append(positions)

        return result_list
