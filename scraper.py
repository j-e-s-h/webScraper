import requests
import lxml.html as html
import string
import os
import datetime

home_url = 'https://www.larepublica.co/'

'''Change "h2" to "text-fill" in "xpath_link_to_article"'''
xpath_link_to_article = '//text-fill/a/@href'
xpath_title = '//div[@class="mb-auto"]/text-fill/span/text()'
xpath_summary = '//div[@class="lead"]/p/text()'
xpath_body = '//div[@class="html-content"]/p[not(@class)]/text()'

def delete_punctuation(sentence):
    for c in '?¿\"':
        sentence = sentence.replace(c, "")
    return sentence


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parse = html.fromstring(notice)

            try:
                title = parse.xpath(xpath_title)[0]
                new_title = delete_punctuation(title)
                summary = parse.xpath(xpath_summary)[0]
                body = parse.xpath(xpath_body)
            except IndexError:
                return 
            
            with open(f'{today}/{new_title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(home_url)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(xpath_link_to_article)
            #print(links_to_notices, len(links_to_notices))

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()

if __name__ == '__main__':
    run()