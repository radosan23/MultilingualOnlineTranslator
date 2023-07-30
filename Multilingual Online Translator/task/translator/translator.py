from bs4 import BeautifulSoup
from io import StringIO
import requests
from sys import argv


class Translator:
    languages = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch',
                 'polish', 'portuguese', 'romanian', 'russian', 'turkish']

    def __init__(self, lang1=None, lang2=None, word=None):
        self.lang1 = lang1.lower()
        self.lang2 = lang2.lower()
        self.word = word
        self.trans_list = None
        self.sent_list = None
        self.buffer = StringIO()

    @property
    def url(self):
        return f'https://context.reverso.net/translation/' \
               f'{self.lang1}-{self.lang2}/{self.word}'

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
            self.print_f('\n' + self.lang2.capitalize() + ' Translations:')
            self.print_f('\n'.join(self.trans_list[:lim]))
        if sentences:
            self.print_f('\n' + self.lang2.capitalize() + ' Examples:')
            for i, sent in enumerate(self.sent_list[:lim * 2]):
                self.print_f(sent + ('\n' if i % 2 == 1 and i != (lim * 2) - 1 else ''))

    def save_file(self):
        with open(self.word + '.txt', 'wt', encoding='utf-8') as f:
            f.write(self.buffer.getvalue())

    def multiple(self):
        for lang in self.languages:
            if lang == self.lang1:
                continue
            self.lang2 = lang
            self.translate()
            self.print_results(lim=1)


def main():
    lang1, lang2, word = argv[1:]
    trans = Translator(lang1, lang2, word)
    if trans.lang2 == 'all':
        trans.multiple()
    else:
        trans.translate()
        trans.print_results(lim=5)
    trans.save_file()


if __name__ == '__main__':
    main()
