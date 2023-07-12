import random
import time
import sys
import os
import json

with open('settings.local.json', 'r', encoding='utf-8') as f:
    settings = json.load(f)

TIME_FOR_SLEEP = settings['TIME_FOR_SLEEP']
IGNORED_FILES_LISTS = settings['IGNORED_FILES_LISTS']


class CurrentVocabulary:
    """Voc."""
    
    def __init__(self, en: list, ru: list):
        """init."""
        if len(en) != len(ru):
            raise IndexError("'en' and 'ru' vocs are not similar")
        self._print_info()
        self.en = en
        self.ru = ru
        self.len = len(en)  # is refered many times
    
    @staticmethod
    def _print_info():
        print('info:')
        print('1. just one word in answer.')
        print("2. don't write excess whitespaces in answer.")
        print("Let's start")
        print()

    @staticmethod
    def _read_text(file_name: str,
                   shuffle_flag: bool = True):
        """_summary_."""
        with open(file_name, 'r', encoding='utf-8') as f:
            text = f.read()
        text = text.split('\n')

        en, ru = [], []
        for el in text:
            curr = el.split('\t')
            en.append(curr[0])
            ru.append(curr[1])

        result = {'en': en, 'ru': ru}
        return result

    @staticmethod
    def dct_to_lists(dct: dict, first_country: str = None) -> dict:
        """It's used just after sequency mode for mistakes."""
        if first_country is None:
            return None
        elif first_country.lower() == 'ru':
            ru = list(dct.keys())
            en = list(dct.values())
        elif first_country.lower() == 'en':
            en = list(dct.keys())
            ru = list(dct.values())
        else:
            raise ValueError('Please, input correct country')
        return {'ru': ru, 'en': en}

    def infinity_mode(self, type: str = 'en'):
        """start."""
        if type == 'en':
            while True:
                id = random.randint(0, self.len - 1)
                answer = input(f'{self.en[id]}: ').lower()
                
                if answer in [word[1:] if word[0] == ' ' else word for word in self.ru[id].split(',')]:
                    print(f"Currect! '{self.ru[id]}'.")
                    print('_________________')
                else:
                    print(f"Sorry, but you are wrong! Right is '{self.ru[id]}'")
                    time.sleep(TIME_FOR_SLEEP)
                    print('_________________')
                    
        elif type == 'ru':
            while True:
                id = random.randint(0, self.len - 1)
                answer = input(f'{self.ru[id]}: ').lower()

                if answer == self.en[id]:
                    print(f"Currect! '{self.en[id]}'.")
                    print('_________________')
                else:
                    print(f"Sorry, but you are wrong! Right is '{self.en[id]}'")
                    time.sleep(TIME_FOR_SLEEP)
                    print('_________________')
        else:
            raise ValueError("Sorry, but u put incorrect 'ru' or 'en' mode")
    
    def sequence_mode(self, type: str = 'en'):
        """sequence."""
        wrong_dct = {}
        lst = list(range(0, self.len))
        random.shuffle(lst)
        if type == 'en':
            for n, id in enumerate(lst):
                try:
                    answer = input(f'{n+1}/{len(lst)}. {self.en[id]}: ').lower()
                except KeyboardInterrupt:
                    break
                
                if answer in [word[1:] if word[0] == ' ' else word for word in self.ru[id].split(',')]:
                    print(f"Currect! '{self.ru[id]}'.")
                    print('_________________')
                else:
                    print(f"Sorry, but you are wrong! Right is '{self.ru[id]}'")
                    if input("Do you want to add the word to the mistakes dict ? ").lower() in ('yes', 'y', 'да', '+', 'д', '++', '+++'):
                        wrong_dct[self.en[id]] = self.ru[id]
                    print('_________________')
        elif type == 'ru':
            for n, id in enumerate(lst):
                try:
                    answer = input(f'{n+1}/{len(lst)}. {self.ru[id]}: ').lower()
                except KeyboardInterrupt:
                    break
                        
                if answer == self.en[id]:
                    print(f"Currect! '{self.en[id]}'.")
                    print('_________________')
                else:
                    print(f"Sorry, but you are wrong! Right is '{self.en[id]}'")
                    if input("Do you want to add the word to the mistakes dict ? ").lower() in ('yes', 'y', 'да', '+', 'д', '++', '+++'):
                        wrong_dct[self.en[id]] = self.ru[id]
                    print('_________________')
        else:
            raise ValueError("Sorry, but u put incorrect 'ru' or 'en' mode")
        print(f'\nYou were wrong in the next words ({wrong_dct.__len__()}/{n}):')
        for word in wrong_dct:
            print('"' + f'{word}' + '": "' + f'{wrong_dct[word]}' + '",')


en = settings['en']
ru = settings['ru']

en = list(map(lambda x: x.lower(), en))
ru = list(map(lambda x: x.lower(), ru))

# just for mistakes
# u cat put here dict with mistakes and on next time the training will be happening with the dict of mistakes
dct_with_mistakes = settings['mistakes_dict'][1]
dct_with_mistakes = CurrentVocabulary.dct_to_lists(dct_with_mistakes, settings['mistakes_dict'][0])
if dct_with_mistakes['ru'].__len__() != 0:
    if len(sys.argv) <= 1:
        print("There is working with dict of mistakes!")
    en = dct_with_mistakes['en']
    ru = dct_with_mistakes['ru']


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_names = sys.argv[1:]
        if 'all' in file_names:
            # all mode
            lst_files = [file for file in os.listdir('./dicts') if '.txt' in file and file not in IGNORED_FILES_LISTS]
            print("There will be words from ", lst_files)
            en, ru = [], []
            for file_name in lst_files:
                curr_en, curr_ru = CurrentVocabulary._read_text('./dicts/' + file_name).values()
                en += curr_en
                ru += curr_ru
        else:
            # just some vocabularies
            en, ru = [], []
            for file in file_names:
                curr_words = list(CurrentVocabulary._read_text('./dicts/' + f'{file}.txt').values())
                en += curr_words[0]
                ru += curr_words[1]

    voc = CurrentVocabulary(en, ru)
    mode = input("what's mode do you want ? 1. infinity, 2. sequence - ")
    if mode == '1':
        voc.infinity_mode(input("Would you like to learn: 'en' or 'ru' ? ").lower())
    elif mode == '2':
        voc.sequence_mode(input("Would you like to learn: 'en' or 'ru' ? ").lower())
    else:
        raise ValueError("Sorry, but u put incorrect number of mode")
