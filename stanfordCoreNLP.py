import string
import stanza

custom_dir = "F:\\"  # Adjust this to your actual model directory

# Load English model
def extract_dependency_and_pos(sentences_list):
    """
    Extracts and parses sentences' dependency structures, part-of-speech, and identifies question words.
    :return: POS, dependency structure and question word for each sentence
    """
    # Initialize Stanza Pipeline
    nlp = stanza.Pipeline('en', model_dir=custom_dir, download_method=None,
                          processors='tokenize,pos,lemma,depparse', use_gpu=True)

    results = []
    for sentence in sentences_list:
        # Process the sentence with the pipeline
        doc = nlp(sentence.rstrip(string.punctuation))
        sentence_data = {
            'sentence': sentence,
            'words_and_pos': [],
            'question_word': None,
            'dependencies': []
        }

        # Analyze sentence components
        for sent in doc.sentences:
            print(sent.words)
            for word in sent.words:
                # Append POS for each word
                sentence_data['words_and_pos'].append((word.text, word.xpos))

                # Identify question words
                if word.deprel == 'nsubj' and word.xpos.startswith('W'):
                    sentence_data['question_word'] = word.text

                # Extract dependency structure
                head_word = sent.words[word.head - 1].text if word.head > 0 else word.text
                dependency_relation = (word.deprel, [head_word, word.text])
                sentence_data['dependencies'].append(dependency_relation)

        results.append(sentence_data)

    return results

# Example usage
sentences = ['Which companies are in the computer software industry?']
processed_sentences = extract_dependency_and_pos(sentences)
for data in processed_sentences:
    print(f"Sentence: {data['sentence']}")
    print("Words and POS:")
    for word, pos in data['words_and_pos']:
        print(f"{word}: {pos}")
    if data['question_word']:
        print(f"Question Word: {data['question_word']}")
    for dep in data['dependencies']:
        print(f"({dep[0]}: {dep[1]})")
