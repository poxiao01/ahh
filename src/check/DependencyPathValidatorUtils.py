# 设置文件编码为UTF-8，以便支持中文字符显示
# -*- coding: utf-8 -*-
class DependencyPathValidator:
    def __init__(self, question_word, structure_word, dependency_relations, dependency_paths_list):
        """
        初始化依赖关系解析器。

        :param question_word: 问题词
        :param structure_word: 结构词
        :param dependency_relations: 句子的依存关系列表
        :param dependency_paths_list: 句子的依赖路径
        """
        self.question_word = question_word
        self.structure_word = structure_word
        self.dependency_relations = dependency_relations
        self.edge_dict = self._construct_directed_graph()  # 构建有向图
        self.dependency_paths_list = dependency_paths_list  # 存储需要check的依赖路径
        self.ok = False

    def _construct_directed_graph(self):
        """
        根据依存关系构建有向图。

        :return: 有向图字典，键为节点（词语），值为（目标节点，关系，方向）的列表
        """
        edge_dict = {}
        for relation, words in self.dependency_relations:
            head_word, word = words
            edge_dict.setdefault(head_word, []).append((word, relation, '-->'))
            edge_dict.setdefault(word, []).append((head_word, relation, '<--'))
        return edge_dict

    def _dfs(self, current_word, target_word, index, visited):

        if current_word == target_word and index == len(self.dependency_paths_list):
            self.ok = True

        if self.ok or index >= len(self.dependency_paths_list):
            return

        for next_word, relation, direction in self.edge_dict[current_word]:
            if next_word not in visited and relation == self.dependency_paths_list[index][0] and direction == \
                    self.dependency_paths_list[index][1]:
                visited.add(next_word)
                self._dfs(next_word, target_word, index + 1, visited)
                visited.remove(next_word)

    def check_dependency_path(self):
        current_word, target_word = self.structure_word, self.question_word
        visited = set()
        visited.add(current_word)
        self._dfs(current_word, target_word, 0, visited)
        visited.remove(current_word)
        return self.ok
