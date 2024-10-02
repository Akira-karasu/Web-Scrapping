from bs4 import BeautifulSoup
import requests 

html_content = requests.get('https://quotes.toscrape.com/').text

soup = BeautifulSoup(html_content, 'lxml')

card = soup.find_all('div', class_='quote')

for quote_card in card:
    author_small = quote_card.small.text

    # Filtering
    # if "Albert Einstein" in author_small:

    quote_span = quote_card.span.text

    tags_div = quote_card.find('div', class_='tags')

    tag_a = tags_div.find_all('a', class_ = 'tag')

    print(f'\n\n{quote_span} by {author_small}')

    print('Tag: ')
    for tag in tag_a:
        print(f'{tag.text}', end=" / ")

    





