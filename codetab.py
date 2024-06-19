import os, time, random, argparse, sys, threading, json
from os import system, name
from colorama import Fore, init, Style

init(autoreset=True)

CONFIG_FOLDER = 'config'
JSON_FILE = os.path.join(CONFIG_FOLDER, 'languages.json')

red = Fore.RED + Style.BRIGHT
green = Fore.GREEN + Style.BRIGHT
cyan = Fore.CYAN + Style.BRIGHT
yellow = Fore.YELLOW + Style.BRIGHT
black = Fore.BLACK + Style.BRIGHT
reset = Fore.RESET + Style.RESET_ALL

wrong_words = []
correct_words = []

correct = 0
wrong = 0
start_time = None
stop_test = False

def refresh(correct, wrong, elapsed_time):
    system(f'title Correct: {correct}, Wrong: {wrong}, Time: {elapsed_time:.0f}s')
    return

def file(path):
    with open(path, 'r') as file:
        lines_list = file.readlines()
    return [line.strip() for line in lines_list]

def typing_test(words):
    global correct, wrong, stop_test
    try:
        word = random.choice(words)
        print(cyan + f'{word:.^30}')
        ans = input(yellow + '>> ')
        if ans.replace(" ", "") == word:
            correct_words.append(word)
            correct += 1
        else:
            wrong_words.append(word)
            wrong += 1
        elapsed_time = time.time() - start_time
        refresh(correct, wrong, elapsed_time)
        system('cls' if name == 'nt' else 'clear')
    except KeyboardInterrupt:
        stop_test = True
    except EOFError:
        stop_test = True

def timer():
    while not stop_test:
        elapsed_time = time.time() - start_time
        refresh(correct, wrong, elapsed_time)
        time.sleep(1)

def calculate_wpm(correct, elapsed_time):
    return (correct / elapsed_time) * 60

def main():
    global start_time, stop_test
    parser = argparse.ArgumentParser(description='Programming language typing test')
    parser.add_argument('-w', '--words', help='Number of the words.', type=int)
    parser.add_argument('-l', '--language', help='Programming language.', required=True)

    args = parser.parse_args()
    num_words = args.words
    language = args.language

    json_path = os.path.join(CONFIG_FOLDER, 'languages.json')
    with open(json_path, 'r') as json_file:
        languages = json.load(json_file)

    if language not in languages:
        print(red + f"Error: Language '{language}' is not supported.")
        sys.exit(1)

    language_file = languages[language]
    language_file_path = os.path.join(CONFIG_FOLDER, language_file)
    words = file(language_file_path)

    if '-h' in sys.argv or '--help' in sys.argv:
        parser.print_help()
        return

    start_time = time.time()
    timer_thread = threading.Thread(target=timer)
    timer_thread.daemon = True
    timer_thread.start()

    if num_words:
        for _ in range(num_words):
            if stop_test:
                break
            print(f'{green}Correct: {correct}{reset},{red} Wrong: {wrong}{reset},{black} Left: {num_words - (correct + wrong)}')
            typing_test(words)
    else:
        while not stop_test:
            try:
                print(black + f'{green}Correct: {correct}{reset},{red} Wrong: {wrong}{reset}')
                typing_test(words)
            except KeyboardInterrupt:
                stop_test = True
            except EOFError:
                stop_test = True

    elapsed_time = time.time() - start_time
    wpm = calculate_wpm(correct, elapsed_time)

    print(f'{red}Mistake:{reset} {", ".join(wrong_words)}')
    print(f'{green}Correct:{reset} {", ".join(correct_words)}')

    print(f"\n{green}Correct words: {correct}")
    print(f"{red}Wrong words: {wrong}")
    print(f"{cyan}Words per minute: {wpm:.0f}\n")

if __name__ == '__main__':
    system('cls' if name == 'nt' else 'clear')
    main()
