def save_to_txt(sentences_list, question_words_and_pos_list, structure_words_and_pos_list, dependencies_paths, sentences_dependencies_relations):
    with open("E:/python_stanford_NLP/result/RST.txt", "w") as file:
        for index, sentence in enumerate(sentences_list):
            file.write(f"{index + 1}.{sentence}\n")
            file.write(f'疑问词：{question_words_and_pos_list[index][0]}, 词性：{question_words_and_pos_list[index][1]}\n')
            file.write(f'句型词：{structure_words_and_pos_list[index][0]}, 词性：{structure_words_and_pos_list[index][1]}\n')
            file.write(f'依赖路径：{dependencies_paths[index]}\n')
            formatted_relations = '\n '.join([f"{rel[0]}: [{', '.join(rel[1])}]" for rel in sentences_dependencies_relations[index]])
            file.write(f'依赖结构：\n{formatted_relations}\n\n')
    print('文件保存成功！')