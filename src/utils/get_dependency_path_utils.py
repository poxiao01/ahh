import copy


class DependencyResolver:
    """
    该类用于解析句子中的依存关系，特别是寻找从结构词到问题词的最短依赖路径。
    """

    def __init__(self, question_word, structure_word, dependency_relations, sentence):
        """
        初始化依赖关系解析器。

        :param question_word: 问题词
        :param structure_word: 结构词
        :param dependency_relations: 句子的依存关系列表
        :param sentence: 完整的句子文本
        """
        self.question_word = question_word
        self.structure_word = structure_word
        self.dependency_relations = dependency_relations
        self.sentence = sentence
        self.edge_dict = self._construct_directed_graph()  # 构建有向图
        self.dependency_paths_list = []  # 存储找到的依赖路径
        self._find_shortest_dependency_paths()  # 查找最短依赖路径

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

    def _find_shortest_dependency_paths(self):
        """
        从结构词到问题词查找所有最短的依赖路径。
        """
        visited = set()
        visited.add(self.structure_word)
        self._dfs(self.structure_word, self.question_word, [], set())
        visited.remove(self.structure_word)

        # 如果有多条最短路径，保留它们；否则，保持当前找到的路径
        if self.dependency_paths_list:
            min_path_length = min(len(path) for path in self.dependency_paths_list)
            self.dependency_paths_list = [path for path in self.dependency_paths_list if len(path) == min_path_length]
            # 转换路径表示形式
            self.dependency_paths_list = [' --> '.join(path) for path in self.dependency_paths_list]
            if len(self.dependency_paths_list) > 1:
                print(f'最短路不唯一：{self.sentence}')
        else:
            print(f'未找到路径：{self.sentence}')

    def _dfs(self, current_word, target_word, current_path, visited):
        """
        深度优先搜索查找依赖路径。

        :param current_word: 当前处理的词语
        :param target_word: 目标词语
        :param current_path: 当前路径
        :param visited: 已访问节点集合
        """
        if current_word == target_word:
            self.dependency_paths_list.append(current_path)
            return

        visited.add(current_word)
        if current_word in self.edge_dict:
            for next_word, relation, _ in self.edge_dict[current_word]:
                if next_word not in visited:
                    self._dfs(next_word, target_word, current_path + [f'[{relation}：{_}]'], visited)
        visited.remove(current_word)

    def get_dependency_paths(self):
        """
        获取从结构词到问题词的最短依赖路径。

        :return: 最短依赖路径列表
        """
        if self.question_word == self.structure_word:
            return []
        for ration, words in self.dependency_relations:
            if words[0] == self.question_word and words[1] == self.structure_word \
                    or words[0] == self.structure_word and words[1] == self.question_word:
                return []

        return self.dependency_paths_list if self.dependency_paths_list else None
