class DependencyResolver:
    def __init__(self, question_word, structure_word, dependency_relations):
        self.question_word = self.custom_format(question_word).strip()
        self.structure_word = self.custom_format(structure_word).strip()
        self.dependency_relations = dependency_relations
        self.edge_dict = dict()
        self.used_word = dict()
        self.dependency_paths_list = []
        self.make_directed_graph(dependency_relations)
        # self.output()

    def custom_format(self, s):
        begin_position = s.find('：')  # 找到第一个':'的位置
        end_position = s.find(',')  # 找到第一个','的位置

        if begin_position != -1 and end_position != -1 and begin_position < end_position:  # 确保字符串中有冒号
            return s[begin_position + 1: end_position]  # 从冒号之后的字符开始取到字符串结束
        else:
            return s  # 如果没有找到，返回原字符串

    def make_directed_graph(self, dependency_relations):
        for ration, words in dependency_relations:
            head_word, word = words[0], words[1]
            # print(ration, head_word, word)
            if word not in self.edge_dict:
                self.edge_dict[word] = [(head_word, ration)]
            else:
                self.edge_dict[word].append((head_word, ration))

    def output(self):
        pass
        # if len(self.dependency_paths_list) == 0 and self.question_word != self.structure_word:
        #     print('\n--------------------------------begin---------------------------------------\n')
        #     print("Question: " + self.question_word)
        #     print("Structure: " + self.structure_word)
        #     # print("Dependencies:" + str(self.dependency_relations))
        #     for word, relation in self.edge_dict.items():
        #         print(word, relation)
        #
        #     print('依赖路径：')
        #     for path in self.dependency_paths_list:
        #         print(path)
        #
        #     print('\n--------------------------------end---------------------------------------\n\n')

    def find_dependency_paths(self, word, target_word, path):
        if word == target_word:
            self.dependency_paths_list.append(path)
            return
        if word not in self.edge_dict:
            return
        for word_and_relation in self.edge_dict[word]:
            next_word, next_relation = word_and_relation[0], word_and_relation[1]
            if next_word in self.used_word and self.used_word[next_word] == True: continue
            dependency_structure = f'[{next_relation}：{next_word},{word}] '
            self.used_word[next_word] = True
            self.find_dependency_paths(next_word, target_word, path + dependency_structure)
            self.used_word[next_word] = False

    def get_dependency_paths(self):
        word, target_word = self.question_word, self.structure_word
        self.used_word[word] = True
        self.find_dependency_paths(word, target_word, '')
        self.used_word[word] = False

        word,target_word = target_word, word
        self.used_word[word] = True
        self.find_dependency_paths(word, target_word, '')
        self.used_word[word] = False

        return self.dependency_paths_list
