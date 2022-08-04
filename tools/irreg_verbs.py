import random

lists_with_tuples = []
wrong_lst = []


def _print_info(lang: str):
    print("Hello, remember that u should use '_' instead ' ' and '/' with two translations.")
    
    if lang == 'en':
        print("There will be random form and u should write forms from left to right and then translation")
    else:
        print("There will be random translation and u should write forms from left to right with spaces")
    
    print("")


with open('word_list.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for el in lines:
    curr_tuple = el.split(" ")
    if '\n' in curr_tuple[-1]:
        curr_tuple[-1] = curr_tuple[-1][:-1]
    lists_with_tuples.append(curr_tuple)
    
if __name__ == '__main__':
    lang = input("Would you like to learn: 'en' or 'ru' ? ")
    _print_info(lang)

    if lang == 'en':
        lst = list(range(0, len(lists_with_tuples)))
        random.shuffle(lst)
        for n, id in enumerate(lst):
            num_from = random.randint(0, 2)
            answer = input(f'{n+1}/{len(lst)}. {lists_with_tuples[id][num_from]}: ').lower()
            currect_answer = lists_with_tuples[id].copy()
            currect_answer.remove(lists_with_tuples[id][num_from])
            for num, words_from_answer in enumerate(answer.split(" ")):
                if words_from_answer != currect_answer[num]:
                    print(f"Sorry, but you are wrong! Right is '{lists_with_tuples[id]}'")
                    if input("Do you want to add the word to the mistakes dict ? ").lower() in ('yes', 'y', 'да', '+', 'д'):
                        wrong_lst.append(lists_with_tuples[id])
                    break
            print('_________________')

    else:
        lst = list(range(0, len(lists_with_tuples)))
        random.shuffle(lst)
        for n, id in enumerate(lst):
            answer = input(f'{n+1}/{len(lst)}. {lists_with_tuples[id][-1]}: ').lower()
            
            for num, forms_from_answer in enumerate(answer.split(" ")):
                if lists_with_tuples[id][num] != forms_from_answer:
                    print(f"Sorry, but you are wrong in {num+1} form! Right is '{lists_with_tuples[id]}'")
                    if input("Do you want to add the word to the mistakes dict ? ").lower() in ('yes', 'y', 'да', '+', 'д'):
                        wrong_lst.append(lists_with_tuples[id])
            
            print('_________________')
    
    print(f'You were wrong in the next words ({wrong_lst.__len__()}/{len(lst)}):')
    for el in wrong_lst:
        print(el)
