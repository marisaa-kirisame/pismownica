import webbrowser
import requests
import bs4
import pykakasi
import itertools
import json
import sys
import csv

from time import sleep
from tabulate import tabulate
from dataclasses import dataclass


url = "https://www.japonski-pomocnik.pl/wordDictionarySearch?word={word}&wordPlace=START_WITH&searchIn=GRAMMA_FORM_AND_EXAMPLES&searchIn=NAMES&searchIn=KANJI&searchIn=KANA&searchIn=ROMAJI&searchIn=TRANSLATE&searchIn=INFO&_searchIn=1&dictionaryTypeStringList=WORD_VERB_IRREGULAR&dictionaryTypeStringList=WORD_VERB_AUX&dictionaryTypeStringList=WORD_VERB_ZURU&dictionaryTypeStringList=WORD_ADJECTIVE_I&dictionaryTypeStringList=WORD_AUX_ADJECTIVE_I&dictionaryTypeStringList=WORD_NAME&dictionaryTypeStringList=WORD_MALE_NAME&dictionaryTypeStringList=WORD_FEMALE_NAME&dictionaryTypeStringList=WORD_COUNTER&dictionaryTypeStringList=WORD_ADJECTIVE_NA&dictionaryTypeStringList=WORD_WORK&dictionaryTypeStringList=WORD_COMPANY_NAME&dictionaryTypeStringList=WORD_PLACE&dictionaryTypeStringList=WORD_ORGANIZATION_NAME&dictionaryTypeStringList=WORD_PRODUCT_NAME&dictionaryTypeStringList=WORD_STATION_NAME&dictionaryTypeStringList=WORD_PROPER_NOUN&dictionaryTypeStringList=WORD_SURNAME_NAME&dictionaryTypeStringList=WORD_UNCLASS_NAME&dictionaryTypeStringList=WORD_PERSON&dictionaryTypeStringList=WORD_PARTICULE&dictionaryTypeStringList=WORD_PREFIX&dictionaryTypeStringList=WORD_SUFFIX&dictionaryTypeStringList=WORD_ADVERB&dictionaryTypeStringList=WORD_ADVERB_TO&dictionaryTypeStringList=WORD_VERB_RU&dictionaryTypeStringList=WORD_NOUN&dictionaryTypeStringList=WORD_NOUN_PREFIX&dictionaryTypeStringList=WORD_NOUN_SUFFIX&dictionaryTypeStringList=WORD_TEMPORAL_NOUN&dictionaryTypeStringList=WORD_ADVERBIAL_NOUN&dictionaryTypeStringList=WORD_ADJECTIVE_NO&dictionaryTypeStringList=WORD_ADJECTIVE_F&dictionaryTypeStringList=WORD_CONJUNCTION&dictionaryTypeStringList=WORD_AUX&dictionaryTypeStringList=WORD_ADJECTIVE_TARU&dictionaryTypeStringList=WORD_VERB_TE&dictionaryTypeStringList=WORD_VERB_U&dictionaryTypeStringList=WORD_INTERJECTION&dictionaryTypeStringList=WORD_EXPRESSION&dictionaryTypeStringList=WORD_PRONOUN&_dictionaryTypeStringList=1"
kanjiapi_url = "https://kanjiapi.dev/v1/kanji/{kanji}"
kks = pykakasi.kakasi()

@dataclass
class LookupResult:
    word: str
    reading: str
    meaning: str

def log(string: str):
    with open("debug.log", "a+") as logfile:
        logfile.write(string + "\n")
    return

def determine_reading(word: str):
    kakashi_result = kks.convert(word)[0]
    response = requests.get(kanjiapi_url.format(kanji = word[0]))
    kanjiapi_result = json.loads(response.content)
    if not "on_readings" in kanjiapi_result:
        return 'kun' 
    on_readings = kanjiapi_result["on_readings"]
    for reading in on_readings:
        if kakashi_result['kana'].startswith(reading):
            return 'on'
    return 'kun'

def main():
    if len(sys.argv) < 2:
        print("Please provie arguments")
        return
    words = sys.argv[1:]
    results = []
    for word in words:
        results.append(lookup(word))
        sleep(0.2)
    #print(tabulate(results, tablefmt="pretty"))
    with open("out.csv", "w+", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";", quotechar="\"")
        for res in results:
            writer.writerow([res.word, res.reading, res.meaning])
    return

def lookup(word: str):
    log("Looking up: " + word)
    r = requests.get(url.format(word = word))
    log("Response: " + str(r.status_code))
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    log("Result: " + str(soup.contents))
    table = soup.find(id="wordDictionaryFindWordResult")
    if table.tfood.tr == None:
        raise Exception("No results")
    stripped_meanings = table.tfood.tr.find_all('td')[1].div.stripped_strings
    meanings_list = list(stripped_meanings)
    meanings = meanings_list[0:2]
    log("\n")
    
    for keyword in ["rzeczownik", "przymiotnik", "czasownik", "wyjaśnienie"]:
        if keyword in meanings[1]:
            meanings.pop(1)
            break

    meanings_str = ", ".join(meanings)

    match determine_reading(word):
        case 'on':
            reading = kks.convert(word)[0]['kana']
        case 'kun':
            reading = kks.convert(word)[0]['hira']

    lookup_result = LookupResult(word, reading, meanings_str)
    return lookup_result




if __name__ == "__main__":
    main()
