from owlready2 import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Создать структуру онтологии (без данных)"

    def handle(self, *args, **options):
        onto = get_ontology("http://test.org/pl_ru_ontology.owl")
        with onto:
            # класс слова
            class Word(Thing):
                pass

            # подкласс для слов на русском и польском
            class ruWord(Word):
                pass

            class plWord(Word):
                pass

            # подклассы для слов на русском и польском по частям речи
            class ruNOUN(ruWord):
                pass
            class ruVERB(ruWord):
                pass
            class ruADJ(ruWord):
                pass
            class ruADV(ruWord):
                pass
            class ruPRT(ruWord):
                pass
            class ruGRND(ruWord):
                pass
            class ruPREP(ruWord):
                pass
            class ruCONJ(ruWord):
                pass
            class ruPRONOUN(ruWord):
                pass

            class plNOUN(plWord):
                pass
            class plVERB(plWord):
                pass
            class plADJ(plWord):
                pass
            class plADV(plWord):
                pass
            class plPRT(plWord):
                pass
            class plGRND(plWord):
                pass
            class plPREP(plWord):
                pass
            class plCONJ(plWord):
                pass
            class plPRONOUN(plWord):
                pass

            # класс для происхождения слов
            class Etymology(Thing):
                pass
            class french(Etymology):
                pass
            class proto_slavic(Etymology):
                pass
            class latin(Etymology):
                pass
            class english(Etymology):
                pass
            class german(Etymology):
                pass
            # класс для морфологических признаков
            class Morphology(Thing):
                pass
            class wordForm(Morphology):
                pass
            class gender(Morphology):
                pass
            class case(Morphology):
                pass
            class number(Morphology):
                pass
            class aspect(Morphology):
                pass
            class person(Morphology):
                pass
            class tense(Morphology):
                pass
            class mood(Morphology):
                pass
            #класс для id
            class TableID(Thing):
                pass
            
            #отношения
            class isSynonym(ObjectProperty):
                domain = [Word]
                range = [Word]
            class isFalseFriend(ObjectProperty):
                domain = [Word]
                range = [Word]
            class hasSameEtymology(ObjectProperty):
                domain = [Word]
                range = [Etymology]
            class isTranslationOf(ObjectProperty):
                domain = [Word]
                range = [Word]
            class isFormOf(ObjectProperty):
                domain = [Word]
                range = [wordForm]
            class isInTable(ObjectProperty):
                domain = [Word]
                range = [TableID]
            class hasCase(ObjectProperty):
                domain = [Word]
                range = [case]
            class hasGender(ObjectProperty):
                domain = [Word]
                range = [gender]
            class hasNumber(ObjectProperty):
                domain = [Word]
                range = [number]
            class hasAspect(ObjectProperty):
                domain = [Word]
                range = [aspect]
            class hasPerson(ObjectProperty):
                domain = [Word]
                range = [person]
            class hasTense(ObjectProperty):
                domain = [Word]
                range = [tense]
            class hasMood(ObjectProperty):
                domain = [Word]
                range = [mood]
            class isFrom(ObjectProperty):
                domain = [Word]
                range = [Etymology]

            именительный = case("именительный")
            родительный = case("родительный")
            дательный = case("дательный")
            винительный = case("винительный")
            творительный = case("творительный")
            предложный = case("предложный")
            звательный = case("звательный")
            masculine = gender("мужской")
            femenine = gender("женский")
            neitral = gender("средний")
            единственное = number("единственное")
            множественное = number("множественное")
            первое = person("первое")
            второе = person("второе")
            третье = person("третье")
            совершенный = aspect("совершенный")
            несовершенный = aspect("несовершенный")
            прошедшее = tense("прошедшее")
            настоящее = tense("настоящее")
            будущее = tense("будущее")
            изъявительное = mood("изъявительное")
            повелительное = mood("повелительное")
            f = proto_slavic('праслав. *čęstь')
            a = latin('лат. elementum')
            g = french('франц. détail')

        onto.save(file="pl_ru_ontology_empty.owl", format="rdfxml")
