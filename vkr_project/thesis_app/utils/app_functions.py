import re
import spacy
from thesis_app.models import TranslatedToken
import pymorphy3
from nltk.tokenize import word_tokenize
from owlready2 import *
russian_names = {
    "ADJ": "прилагательное",
    "NOUN": "существительное",
    "VERB": "глагол",
    "AUX": "глагол",
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
    "Case": "<b>Падеж</b>",
    "Gender": "<b>Род</b>",
    "Number": "<b>Число</b>",
    "Definite": "<b>Определённость</b>",
    "Degree": "<b>Степень</b>",
    "Aspect": "<b>Вид</b>",
    "VerbForm": "<b>Форма глагола</b>",
    "Mood": "<b>Наклонение</b>",
    "Tense": "<b>Время</b>",
    "Voice": "<b>Залог</b>",
    "Person": "<b>Лицо</b>",
    "PronType": "<b>Тип местоимения</b>",
    "PunctType": "<b>Тип знака препинания</b>",
    "Poss": "притяжательное",
    "NumType": "<b>Тип числительного</b>",
    "AdpType": "<b>Тип предлога</b>",
    "NumForm": "<b>Форма числительного</b>",
    "Variant": "<b>Вариант</b>",
    "Animacy": "<b>Одушевлённость</b>",
    "Nom": "именительный",
    "Gen": "родительный",
    "Dat": "дательный",
    "Acc": "винительный",
    "Ins": "творительный",
    "Loc": "предложный",
    "Voc": "звательный",
    "Masc": "мужской",
    "Fem": "женский",
    "Neut": "средний",
    "Sing": "единственное",
    "Plur": "множественное",
    "Ptan": "множественное",
    "1": "первое",
    "2": "второе",
    "3": "третье",
    "Pos": "положительная",
    "Comp": "сравнительная",
    "Sup": "превосходная",
    "Imp": "неопределённый",
    "Perf": "совершенный",
    "Imperf": "несовершенный",
    "Hum": "одуш.",
    "Nhum": "неодуш.",
    "Inan": "неодуш.",
    "Fin": "личная",
    "Inf": "инфинитив",
    "Part": "причастие",
    "Ger": "деепричастие",
    "Ind": "изъявительное",
    "Imp": "несовершенный",
    "Pres": "настоящее",
    "Past": "прошедшее",
    "Fut": "будущее",
    "Act": "действительный",
    "Pass": "страдательный",
    "Prs": "личное",
    "Dem": "указательное",
    "Int": "вопросительное",
    "Rel": "относительное",
    "NumType": "тип числительного",
    "Card": "количественное",
    "Ord": "порядковое",
    "Prep": "предлог",
    "Post": "постпозиционный",
    "Digit": "цифровая",
    "Word": "словесная",
    "Short": "краткая форма",
    "Conv": "деепричастие",
    "Polarity": "Полярность",
    "Neg": "отрицательная",
    "Vnoun": "отглагольное существительное",
    'part_of_speech': "<b>Часть речи</b>"
}
morph_mapping = {
    'NOUN': '<b>Часть речи</b>: существительное',
    'ADJF': '<b>Часть речи</b>: прилагательное',
    'ADJS': '<b>Часть речи</b>: прилагательное',
    'COMP': '<b>Часть речи</b>: сравнительная',
    'VERB': '<b>Часть речи</b>: глагол',
    'INFN': '<b>Часть речи</b>: глагол',
    'PRTF': '<b>Часть речи</b>: причастие',
    'PRTS': '<b>Часть речи</b>: причастие',
    'GRND': '<b>Часть речи</b>: деепричастие',
    'NUMR': '<b>Часть речи</b>: числительное',
    'ADVB': '<b>Часть речи</b>: наречие',
    'NPRO': '<b>Часть речи</b>: местоимение',
    'PRED': '<b>Часть речи</b>: предикатив',
    'PREP': '<b>Часть речи</b>: предлог',
    'CONJ': '<b>Часть речи</b>: союз',
    'PRCL': '<b>Часть речи</b>: частица',
    'INTJ': '<b>Часть речи</b>: междометие',
    'Pltm': 'только',
    'Sgtm': 'только',
    'masc': '<b>Род</b>: мужской',
    'femn': '<b>Род</b>: женский',
    'neut': '<b>Род</b>: средний',
    'GNdr': '<b>Род</b>: невыраженный',
    'ms-f': 'общий',
    'sing': '<b>Число</b>: единственное',
    'plur': '<b>Число</b>: множественное',
    'nomn': '<b>Падеж</b>: именительный',
    'gent': '<b>Падеж</b>: родительный',
    'datv': '<b>Падеж</b>: дательный',
    'accs': '<b>Падеж</b>: винительный',
    'ablt': '<b>Падеж</b>: творительный',
    'loct': '<b>Падеж</b>: предложный',
    'voct': '<b>Падеж</b>: звательный',
    'gen1': '<b>Падеж</b>: первый родительный',
    'gen2': '<b>Падеж</b>: второй родительный',
    'acc2': '<b>Падеж</b>: второй винительный',
    'loc1': '<b>Падеж</b>: первый предложный',
    'loc2': '<b>Падеж</b>: второй предложный',
    'pres': '<b>Время</b>: настоящее',
    'past': '<b>Время</b>: прошедшее',
    'futr': '<b>Время</b>: будущее',
    'perf': '<b>Вид</b>: совершенный',
    'impf': '<b>Вид</b>: несовершенный',
    'tran': '<b>Переходность</b>: переходный',
    'intr': '<b>Переходность</b>: непереходный',
    'actv': '<b>Залог</b>: действительный',
    'pssv': '<b>Залог</b>: страдательный',
    '1per': '<b>Лицо</b>: первое',
    '2per': '<b>Лицо</b>: второе',
    '3per': '<b>Лицо</b>: третье',
    'indc': '<b>Наклонение</b>: изъявительное',
    'impr': '<b>Наклонение</b>: повелительное',
    'incl': '<b>Форма</b>: говорящий включен',
    'excl': '<b>Форма</b>: говорящий не включен',
    'poss': '<b>Форма</b>: притяжательное',
    'inan': '<b>Одушевленность</b>: неодушевленное',
    'anim': '<b>Одушевленность</b>: одушевленное',
    'Qual': '<b>Качество</b>: качественное',
    'Apro': '<b>Тип</b>: местоименное',
    'Anum': '<b>Тип</b>: порядковое числительное',
    'Prdx': '<b>Тип</b>: предикативное',
    'Coun': '<b>Тип</b>: счетное',
    'Coll': '<b>Тип</b>: собирательное',
    'V-ej': '<b>Суффикс</b>: с суффиксом -ей-',
    'Cmp2': '<b>Сравнительная степень</b>: сравнительная степень на по-',
    'V-be': '<b>Суффикс</b>: с суффиксом -бе-',
    'Supr': 'превосходная'
}
pos_mapping = {
    "ruNOUN": "существительное",
    "ruVERB": "глагол",
    "ruADJ": "прилагательное",
    "ruADV": "наречие",
    "ruPRT": "причастие",
    "ruGRND": "деепричастие",
    "ruPREP": "предлог",
    "ruCONJ": "союз",
    "ruPRONOUN": "местоимение",
    "plNOUN": "существительное",
    "plVERB": "глагол",
    "plADJ": "прилагательное",
    "plADV": "наречие",
    "plPRT": "причастие",
    "plGRND": "деепричастие",
    "plPREP": "предлог",
    "plCONJ": "союз",
    "plPRONOUN": "местоимение"
}
key_translation = {
    'hasNumber': '<b>Число</b>',
    'hasGender': '<b>Род</b>',
    'hasCase': '<b>Падеж</b>',
    'hasTense': '<b>Время</b>',
    'hasAspect': '<b>Вид</b>',
    'hasMood': '<b>Наклонение</b>',
    'hasPerson': '<b>Лицо</b>'
}

def rename_keys(dictionary, key_translation):
    """
    Renames the keys of a dictionary based on a translation dictionary.
    """
    return {key_translation.get(k, k): v for k, v in dictionary.items()}

def get_russian_name(tag, pos=False):
    return russian_names.get(tag, tag) if pos else russian_names.get(tag, None)

nlp_pl = spacy.load("pl_core_news_lg")
nlp_ru = spacy.load("ru_core_news_lg")

punctuation_marks_end = set([".", "?", ":", "!", ",", ")", "]", "}", "”"])
punctuation_marks_start = set(["(","[","{","„"])

def split_paragraphs(file_path, nlp):    
    paragraph_splitter = re.compile(r'\s*\n+\s*')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            
        paragraphs = paragraph_splitter.split(text)
        paragraphs_dict = {}
        
        for i, paragraph in enumerate(paragraphs, 1):
            doc = nlp(paragraph)
            sentences = [sent.text for sent in doc.sents]
            sentences_with_words = []
            for sentence in sentences:
                words = []
                previous_word = None
                start_mark = None
                hyphen = False
                for token in nlp(sentence):
                    if token.text in punctuation_marks_end:
                        if previous_word:
                            words[-1] += token.text
                    elif token.text in punctuation_marks_start:
                        start_mark = token.text
                    elif token.text == '-':
                        hyphen = True
                        if previous_word:
                            words[-1] += token.text
                        previous_word = token.text
                    else:
                        if hyphen:
                            words[-1] += token.text
                            previous_word = token.text
                            hyphen = False
                        elif start_mark is None:
                            words.append(token.text)
                            previous_word = token.text
                        else:
                            words.append(start_mark + token.text)
                            previous_word = token.text
                            start_mark = None
                        
                sentences_with_words.append(words)
            paragraphs_dict[f"{i}"] = sentences_with_words
        return paragraphs_dict

    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
        paragraphs_dict = {"Абзац 1": "Файл не найден, невозможно извлечь текст"}
        return paragraphs_dict

# Паттерн для clean_word
clean_pattern = r'[@\(\)\[\]>;:".,?!„”\'/|\\]'

# Очистка слова от "мусора"
def clean_word(word):
    word = str(word)
    if word is not None:
        cleaned_word = re.sub(clean_pattern, '', word.lower())
    else:
        cleaned_word = None
    return cleaned_word

# Анализ польского слова
def analyze_polish_word(word):
    cleaned_word = clean_word(word)
    doc_pl = nlp_pl(cleaned_word)
    result = []

    for token in doc_pl:
        lemma = token.lemma_
        pos = get_russian_name(token.pos_, pos=True)
        morph_description = {"<b>Часть речи</b>": pos}

        for tag, value in token.morph.to_dict().items():
            description_key = get_russian_name(tag, pos=False)
            description_value = get_russian_name(value, pos=False)
            if description_key and description_value:
                morph_description[description_key] = description_value
        
        if '<b>Форма глагола</b>' in morph_description:
            form_of_verb = morph_description['<b>Форма глагола</b>']
            if form_of_verb in ['причастие', 'деепричастие']:
                morph_description['<b>Часть речи</b>'] = morph_description['<b>Форма глагола</b>']
        if '<b>Тип местоимения</b>' in morph_description:
            morph_description['<b>Часть речи</b>'] = 'местоимение'

        result.append({
            'token': token.text,
            'lemma': lemma,
            'morphological_description': morph_description
        })

    return result

# Initialize pymorphy3
morph = pymorphy3.MorphAnalyzer()
# Анализ русского слова
def analyze_russian_word(word):
    cleaned_word = clean_word(word)
    result = []
    tokens = word_tokenize(cleaned_word)

    for token in tokens:
        parsed_word = morph.parse(token)[0]
        gender = parsed_word.tag.gender
        number = parsed_word.tag.number
        lemma = parsed_word.normal_form

        # Перевод морфологической характеристики на русский
        morph_tags = str(parsed_word.tag).split(',')
        if gender or number is not None:
            morph_tags.append(gender)
            morph_tags.append(number)
        morph_description = {}

        for tag in morph_tags:
            if tag is not None:
                tag = tag.strip()
            description = morph_mapping.get(tag)
            if description and description not in morph_description:
                key, value = description.split(':')
                morph_description[key] = value.strip()
        if '<b>Тип</b>' in morph_description:
            if morph_description['<b>Часть речи</b>'] == "прилагательное":
                morph_description['<b>Часть речи</b>'] = "местоимение"
        result.append({
            'token': token,
            'lemma': lemma,
            'morphological_description': morph_description
        })
    return result

# Сбор переведённого предложения из слов в БД
def translate_sentence(token_id):
    token = TranslatedToken.objects.get(id=token_id)
    sentence_id = token.sentence_id
    translated_token_index = token.translated_token_index
    tokens = TranslatedToken.objects.filter(sentence_id=sentence_id)
    tokens = tokens.order_by('translated_token_index')

    translated_sentence = ""
    for t in tokens:
        if t.translated_token_index == translated_token_index and t.word_translated is not None:
            translated_sentence += f"<strong>{t.word_translated}</strong> "
        elif t.word_translated is not None:
            translated_sentence += f"{t.word_translated} "

    return [translated_sentence.strip()]

# Извлечение данных из онтологии по ID в таблице
def get_info_by_table_id(table_id, onto):
    table_instances = onto.search(type=onto.TableID, iri="*" + str(table_id))
    if not table_instances:
        print(f"Не найдены данные в онтологии = {table_id}")
        return {}
    
    table_instance = table_instances[0]
    
    # Поиск всех связанных объектов
    linked_instances = onto.search(isInTable=table_instance)
    
    if not linked_instances:
        print(f"Не найдены связи в онтологии = {table_id}")
        return {}
    
    result = {}
    
    for linked_instance in linked_instances:
        instance_info = {}
        for prop in linked_instance.get_properties():
            values = [value.name for value in prop[linked_instance]]
            instance_info[prop.name] = values
        instance_type = next(iter(linked_instance.is_a)).name
        pos = pos_mapping.get(instance_type, "Unknown")
        instance_info["POS"] = pos
        instance_info["isTranslationOf"] = translate_sentence(table_id)
        instance_info = rename_keys(instance_info, key_translation)
        result[linked_instance.name] = instance_info
    return result