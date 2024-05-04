class DependencyResolver:
    def __init__(self, question_word, structure_word, dependency_relations):
        self.question_word = question_word
        self.structure_word = structure_word
        self.dependency_relations = dependency_relations

    def output(self):
        print("Question: " + self.question_word)
        print("Structure: " + self.structure_word)
        print("Dependencies:" + str(self.dependency_relations))


