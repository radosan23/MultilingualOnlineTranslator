class Translator:
    def __init__(self):
        self.lang = None
        self.word = None


def main():
    trans = Translator()
    trans.lang = input('Type "en" if you want to translate from French into English, or "fr" if'
                       'you want to translate from English into French:\n')
    trans.word = input('Type the word you want to translate:\n')
    print(f'You chose "{trans.lang}" as a language to translate "{trans.word}".')


if __name__ == '__main__':
    main()
