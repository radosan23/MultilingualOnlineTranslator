from bs4 import BeautifulSoup
import requests


class Translator:
    languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch',
                 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']

    def __init__(self, id1=None, id2=None, word=None):
        self.id1 = id1
        self.id2 = id2
        self.word = word
        self.trans_list = None
        self.sent_list = None

    @property
    def url(self):
        return f'https://context.reverso.net/translation/' \
               f'{self.languages[self.id1 - 1].lower()}-{self.languages[self.id2 - 1].lower()}/{self.word}'

    def get_words(self, soup):
        self.trans_list = [x.text for x in soup.find_all('span', {'class': 'display-term'})]

    def get_sentences(self, soup):
        examples = soup.find('section', {'id': 'examples-content'})
        self.sent_list = [x.text.strip() for x in examples.find_all('span', {'class': 'text'})]

    def translate(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(self.url, headers=headers)
        if r.status_code:
            soup = BeautifulSoup(r.content, 'html.parser')
            self.get_words(soup)
            self.get_sentences(soup)

    def print_results(self, words=True, sentences=True, lim=5):
        if words:
            print('\n' + self.languages[self.id2 - 1], 'Translations:')
            print(*self.trans_list[:lim], sep='\n')
        if sentences:
            print('\n' + self.languages[self.id2 - 1], 'Examples:')
            for i, sent in enumerate(self.sent_list[:lim * 2]):
                print(sent + ('\n' if i % 2 == 1 and i != (lim * 2) - 1 else ''))


def main():
    print('Hello, welcome to the translator. Translator supports:')
    for i, lang in enumerate(Translator.languages, start=1):
        print(f'{i}. {lang}')
    lang1 = int(input('Type the number of your language:\n'))
    lang2 = int(input('Type the number of language you want to translate to:\n'))
    word = input('Type the word you want to translate:\n')
    trans = Translator(lang1, lang2, word)
    print(trans.url)
    trans.translate()
    trans.print_results()


if __name__ == '__main__':
    main()
