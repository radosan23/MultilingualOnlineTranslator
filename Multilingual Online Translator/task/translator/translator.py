from bs4 import BeautifulSoup
import requests


class Translator:
    lang_url = {'en': 'french-english', 'fr': 'english-french'}

    def __init__(self, lang=None, word=None):
        self.lang = lang
        self.word = word
        self.trans_list = None
        self.sent_list = None

    @property
    def url(self):
        return f'https://context.reverso.net/translation/{self.lang_url[self.lang]}/{self.word}'

    def get_words(self, soup):
        self.trans_list = [x.text for x in soup.find_all('span', {'class': 'display-term'})]
        print(self.trans_list)

    def get_sentences(self, soup):
        examples = soup.find('section', {'id': 'examples-content'})
        self.sent_list = [x.text.strip() for x in examples.find_all('span', {'class': 'text'})]
        print(self.sent_list)

    def translate(self, words=True, sentences=True):
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(self.url, headers=headers)
        print(r.status_code, 'OK' if r.status_code else 'unable to connect')
        if r.status_code:
            print('Translations')
            soup = BeautifulSoup(r.content, 'html.parser')
            if words:
                self.get_words(soup)
            if sentences:
                self.get_sentences(soup)


def main():
    trans = Translator()
    trans.lang = input('Type "en" if you want to translate from French into English, or "fr" if '
                       'you want to translate from English into French:\n')
    trans.word = input('Type the word you want to translate:\n')
    print(f'You chose "{trans.lang}" as a language to translate "{trans.word}".')
    trans.translate()


if __name__ == '__main__':
    main()
