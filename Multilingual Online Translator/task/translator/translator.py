from bs4 import BeautifulSoup
from io import StringIO
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
        self.buffer = StringIO()

    @property
    def url(self):
        return f'https://context.reverso.net/translation/' \
               f'{self.languages[self.id1 - 1].lower()}-{self.languages[self.id2 - 1].lower()}/{self.word}'

    def print_f(self, msg, sep=' '):
        print(msg, sep=sep)
        print(msg, file=self.buffer, sep=sep)

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
            self.print_f('\n' + self.languages[self.id2 - 1] + ' Translations:')
            self.print_f(' '.join(self.trans_list[:lim]), sep='\n')
        if sentences:
            self.print_f('\n' + self.languages[self.id2 - 1] + ' Examples:')
            for i, sent in enumerate(self.sent_list[:lim * 2]):
                self.print_f(sent + ('\n' if i % 2 == 1 and i != (lim * 2) - 1 else ''))

    def save_file(self):
        with open(self.word + '.txt', 'wt', encoding='utf-8') as f:
            f.write(self.buffer.getvalue())

    def multiple(self):
        for lang in range(1, 14):
            if lang == self.id1:
                continue
            self.id2 = lang
            self.translate()
            self.print_results(lim=1)


def main():
    print('Hello, welcome to the translator. Translator supports:')
    for i, lang in enumerate(Translator.languages, start=1):
        print(f'{i}. {lang}')
    lang1 = int(input('Type the number of your language:\n'))
    lang2 = int(input("Type the number of language you want to translate to or '0' to translate to all languages:\n"))
    word = input('Type the word you want to translate:\n')
    trans = Translator(lang1, lang2, word)
    if trans.id2 == 0:
        trans.multiple()
    else:
        trans.translate()
        trans.print_results(lim=1)
    trans.save_file()


if __name__ == '__main__':
    main()
