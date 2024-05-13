import re

def split_paragraphs(file_path):
    paragraph_splitter = re.compile(r'\s*\n+\s*')
    sentence_splitter = re.compile(r'[\.\?!]\s*(?=[A-ZА-Я])')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        paragraphs = paragraph_splitter.split(text)

        paragraphs_dict = {}
        paragraphs_dict = {f"Абзац {i}": [sentence.split() for sentence in sentence_splitter.split(paragraph)] 
                   for i, paragraph in enumerate(paragraphs, start=1)}
        return paragraphs_dict

    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
        paragraphs_dict = {"Абзац 1": "Файл не найден, невозможно извлечь текст"}
        return paragraphs_dict
    
import spacy

# Load spaCy model for Polish
nlp_pl = spacy.load("pl_core_news_lg")
def get_russian_name(tag, pos=False):
    russian_names = {
        "ADJ": "прилагательное",
        "NOUN": "существительное",
        "VERB": "глагол",
        "ADV": "наречие",
        "PRON": "местоимение",
        "ADP": "предлог",
        "DET": "определитель",
        "CCONJ": "союз",
        "SCONJ": "подчинительный союз",
        "NUM": "числительное",
        "PART": "частица",
        "INTJ": "междометие",
        "SYM": "символ",
        "X": "неизвестная категория",
        "PROPN": "имя собственное",
        "Case": "Падеж",
        "Gender": "Род",
        "Number": "Число",
        "Definite": "Определённость",
        "Degree": "Степень",
        "Aspect": "Вид",
        "VerbForm": "Форма глагола",
        "Mood": "Наклонение",
        "Tense": "Время",
        "Voice": "Залог",
        "Person": "Лицо",
        "PronType": "Тип местоимения",
        "Poss": "Притяжательное",
        "NumType": "Тип числительного",
        "AdpType": "Тип предлога",
        "NumForm": "Форма числительного",
        "Variant": "Вариант",
        "Animacy": "Одушевлённость",
        "Nom": "Именительный",
        "Gen": "Родительный",
        "Dat": "Дательный",
        "Acc": "Винительный",
        "Ins": "Творительный",
        "Loc": "Предложный",
        "Voc": "Звательный",
        "Masc": "Мужской",
        "Fem": "Женский",
        "Neut": "Средний",
        "Sing": "Единственное",
        "Plur": "Множественное",
        "1": "Первое",
        "2": "Второе",
        "3": "Третье",
        "Pos": "Положительная",
        "Comp": "Сравнительная",
        "Sup": "Превосходная",
        "Imp": "Неопределённый",
        "Perf": "Совершенный",
        "Imperf": "Несовершенный",
        "Hum": "Одуш.",
        "Nhum": "Неодуш.",
        "Inan": "Неодуш.",
        "Fin": "Личная",
        "Inf": "Инфинитив",
        "Part": "Причастие",
        "Ger": "Деепричастие",
        "Ind": "Изъявительное",
        "Imp": "Повелительное",
        "Pres": "Настоящее",
        "Past": "Прошедшее",
        "Fut": "Будущее",
        "Act": "Действительный",
        "Pass": "Страдательный",
        "Prs": "Личное",
        "Dem": "Указательное",
        "Int": "Вопросительное",
        "Rel": "Относительное",
        "NumType": "Тип числительного",
        "Card": "Количественное",
        "Ord": "Порядковое",
        "Prep": "Предлог",
        "Post": "Постпозиционный",
        "Digit": "Цифровая",
        "Word": "Словесная",
        "Short": "Краткая форма",
        "Conv": "Конверб",
        "Polarity": "Полярность",
        "Neg": "Отрицательная",
        "Vnoun": "Отглагольное существительное",
        "Ptan": "??"


    }
    if pos:
        return russian_names.get(tag, "неизвестно")
    else:
        return russian_names.get(tag, None)
def russian_morph_to_str(russian_morph_description):
    morph_str = ""
    for key, value in russian_morph_description.items():
        morph_str += f"{key}: {value}, "
    # Remove the trailing comma and space
    morph_str = morph_str.rstrip(", ")
    return morph_str
# Function to analyze a cleaned Polish word
def analyze_polish_word(word):
    # Define a pattern to remove specific characters
    pattern = r'[@\(\)>;:".,?!„”\'/|\\]'  # Updated pattern
    cleaned_word = re.sub(pattern, '', word)
    
    # Analyze the cleaned word with spaCy
    doc_pl = nlp_pl(cleaned_word)
    
    # Get lemma, POS, and morphological description
    analyzed_word = None
    for token in doc_pl:
        lemma = token.lemma_
        pos = get_russian_name(token.pos_, pos=True)
        morph_description = token.morph.to_dict()
        print(morph_description)
        russian_morph_description = russian_morph_to_str({get_russian_name(key): get_russian_name(value) for key, value in morph_description.items()})
        analyzed_word = (cleaned_word, lemma, pos, russian_morph_description)
    
    return analyzed_word

# Function to print analysis result
def get_analysis_result(word):
    analyzed_word = analyze_polish_word(word)
    if analyzed_word:
        word, lemma, pos, morph_description = analyzed_word
        print(f"Original Word: {word}, Lemma: {lemma}, POS: {pos}, Morph: {morph_description}")
        return [word, lemma, f'Часть речи: {pos}', morph_description]
    else:
        print("Error: Word could not be analyzed.")
        return ["Word could not be analyzed."]
