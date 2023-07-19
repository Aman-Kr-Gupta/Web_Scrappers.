import requests
from bs4 import BeautifulSoup
import re


def get_wikipedia_url(person_name):
    link = f'https://www.google.com/search?q={person_name}+Wikipedia'
    res = requests.get(link)
    soup = BeautifulSoup(res.text, 'html.parser')
    for a in soup.find_all('a'):
        href = a.get('href')
        if href and 'en.wikipedia.org' in href:
            return href[7:].split('&')[0]
    return None


def scrape_wikipedia_content(url):
    if not url:
        return None

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    paragraphs = '\n'.join(p.text for p in soup.find_all('p'))
    return paragraphs.strip()


def main():
    inp = input("Enter Person's name: ")
    wikipedia_url = get_wikipedia_url(inp)
    paragraphs = scrape_wikipedia_content(wikipedia_url)

    if paragraphs:
        # Extract the person's name for the file name
        person_name = re.sub(r'[^\w\s]', '', inp).replace(' ', '_')
        filename = f'{person_name}.txt'

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(paragraphs)
        print(f"Content saved to {filename}")
    else:
        print("No Wikipedia page found for the given person.")


if __name__ == "__main__":
    main()
