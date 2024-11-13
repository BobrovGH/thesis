from owlready2 import get_ontology
from django.core.management.base import BaseCommand
from thesis_app.models import TranslatedToken
from thesis_app.utils.app_functions import analyze_polish_word, analyze_russian_word

onto = get_ontology(
    "pl_ru_ontology_empty.owl"
).load()

def assign_properties(word_onto, word_data, properties):
    """
    Присвоение морфологических свойств объекту в онтологии.

    :param word_onto: Объект онтологии.
    :param word_data: Морфологическое описание слова.
    :param properties: Сопоставление свойств объекта онтологии и описания слова(word_data).
    """
    for prop, onto_attr in properties.items():
        value_str = word_data['morphological_description'].get(prop, '')
        value = getattr(onto, value_str, None) if value_str else None
        if value:
            getattr(word_onto, onto_attr).append(value)


def create_word_onto(onto, token, pos, properties):
    """
    Создание объекта и его морфологических характеристик в онтологии.

    :param onto: Заполняемая онтология.
    :param token: Токена.
    :param pos: Часть речи токена.
    :param properties: Морфологические свойства.
    :return: Объект онтологии.
    """
    word_onto = getattr(onto, pos)(token['token'])
    assign_properties(word_onto, token, properties)
    return word_onto


def create_onto_instance(token, onto, word_id, pl_word, ru_word, pos, properties):
    """
    Заполнение объектами и их связями онтологии

    :param token: Токен.
    :param onto: Онтология.
    :param word_id: ID слова в таблице.
    :param pl_word: Данные о польском слове.
    :param ru_word: Данные о русском слове.
    :param pos: Часть речи слова.
    :param properties: Словарь, присваивающий морфологические свойства объекту в онтологии.
    :return: Объект польского слова в онтологии.
    """
    pl_word_onto = create_word_onto(onto, pl_word, pos, properties)

    # Проверка на наличие леммы для польского слова (создаётся объект леммы в онтологии)
    if pl_word['token'] != pl_word['lemma']:
        pl_lemma = analyze_polish_word(pl_word['lemma'])[0]
        pl_lemma_onto = create_word_onto(onto, pl_lemma, pos, properties)
        pl_word_onto.isFormOf.append(pl_lemma_onto)

    # Проверка наличия, создание и заполнение русского слова
    if ru_word['token'] != 'none':
        ru_pos = pos.replace('pl', 'ru')
        ru_word_onto = create_word_onto(onto, ru_word, ru_pos, properties)

        # Проверка на наличие леммы для русского слова (создаётся объект леммы в онтологии)
        if ru_word['token'] != ru_word['lemma']:
            ru_lemma = analyze_russian_word(ru_word['lemma'])[0]
            ru_lemma_onto = create_word_onto(onto, ru_lemma, ru_pos, properties)
            ru_word_onto.isFormOf.append(ru_lemma_onto)

        # Установка связи "перевода" между польским и русским словами
        pl_word_onto.isTranslationOf.append(ru_word_onto)
        ru_word_onto.isInTable.append(word_id)

    # Добавление ссылки на ID записи в таблице
    pl_word_onto.isInTable.append(word_id)
    return pl_word_onto


class Command(BaseCommand):
    help = "Заполнение онтологии данными из текстов и NLP"

    def handle(self, *args, **options):
        onto = get_ontology(
            "pl_ru_ontology_empty.owl"
        ).load()

        # Сопоставление характеристик частей речи морфологического анализа и связей онтологии
        pos_properties = {
            "прилагательное": ("plADJ", {
                "<b>Падеж</b>": "hasCase",
                "<b>Род</b>": "hasGender",
                "<b>Число</b>": "hasNumber"
            }),
            "существительное": ("plNOUN", {
                "<b>Падеж</b>": "hasCase",
                "<b>Род</b>": "hasGender",
                "<b>Число</b>": "hasNumber"
            }),
            "глагол": ("plVERB", {
                "<b>Вид</b>": "hasAspect",
                "<b>Род</b>": "hasGender",
                "<b>Число</b>": "hasNumber",
                "<b>Лицо</b>": "hasPerson",
                "<b>Наклонение</b>": "hasMood",
                "<b>Время</b>": "hasTense"
            }),
            "наречие": ("plADV", {}),
            "союз": ("plCONJ", {}),
            "предлог": ("plPREP", {}),
            "местоимение": ("plPRONOUN", {}),
            "причастие": ("plPRT", {
                "<b>Падеж</b>": "hasCase",
                "<b>Род</b>": "hasGender",
                "<b>Время</b>": "hasTense"
            }),
            "деепричастие": ("plGRND", {
                "<b>Вид</b>": "hasAspect"
            })
        }

        # Заполнение онтологии данными
        translated_tokens = TranslatedToken.objects.all()
        with onto:
            for token in translated_tokens:
                word_id = onto.TableID(str(token.id))

                # Морфологический анализ слов 
                pl_word = analyze_polish_word(token.word_original)[0]
                ru_word = analyze_russian_word(token.word_translated)[0]
                pl_POS = pl_word['morphological_description']['<b>Часть речи</b>']
                
                # Создание объекта в онтологии 
                if pl_POS in pos_properties:
                    pl_pos, properties = pos_properties[pl_POS]
                    create_onto_instance(token, onto, word_id, pl_word, ru_word, pl_pos, properties)

        onto.save("populated_ontology.owl")
