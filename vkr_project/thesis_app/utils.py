import re

def split_paragraphs(file_path):
    paragraph_splitter = re.compile(r'\s*\n+\s*')
    sentence_splitter = re.compile(r'\.\s*(?=[A-ZА-Я])')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        paragraphs = paragraph_splitter.split(text)

        paragraphs_dict = {}

        for i, paragraph in enumerate(paragraphs, start=1):
            sentences = sentence_splitter.split(paragraph)
            words_list = []
            for sentence in sentences:
                words = sentence.split()
                words_list.append(words)
            paragraphs_dict[f"Абзац {i}"] = words_list

        return paragraphs_dict

    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
        return None