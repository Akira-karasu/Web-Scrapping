from bs4 import BeautifulSoup
import requests 
import time 

def find_author():
    html_content = requests.get('https://quotes.toscrape.com/page/2/').text

    soup = BeautifulSoup(html_content, 'lxml')


    print('Enter the Author: ')
    prompt = input('> ')

    cards = soup.find_all('div', class_='quote')

    for card in cards:

        quote = card.find('span', class_='text').text

        author = card.small.text

        if prompt in author:

            about_author = card.a['href']

            tags = card.find('div', class_='tags')
            a_tag = tags.find_all('a', class_='tag')

            with open(f'Python_Scrapping/Quote_Author/{prompt}.txt', 'w') as f:
                f.write(f'{quote} \n')
                f.write(f'By {author} \n')
                f.write(f'About: {about_author} \n')
                f.write("Tags: ")
                for tag in a_tag:
                    f.write(f'{tag.text} / ')
                print('\n')
        


if__name__ = '__main__';

while True:
    find_author()
    time_wait = 10
    print(f'Time wait {time_wait}... sec')
    time.sleep(time_wait)




