import requests
from bs4 import BeautifulSoup

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = "https://habr.com/ru/all/"


def keywords_in(contents):
    for content in contents:
        text_lower = content.text.strip().lower()
        if any([desired in text_lower for desired in KEYWORDS]):
            return True
    return False


def main():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('article', class_='post')

    for post in posts:
        post_title_link = post.find_all(class_='post__title_link')
        hubs = post.find_all('a', class_='hub-link')
        preview = post.find_all('div', class_="post__text-html")
        post_title = post_title_link[0].text
        href = post_title_link[0].attrs.get('href')
        post_time = post.find('span', class_='post__time')
        if keywords_in(post_title_link) or keywords_in(hubs) or keywords_in(preview):
            print(post_time.text, post_title, href)
        else:
            res = requests.get(href)
            soup_body = BeautifulSoup(res.text, 'html.parser')
            post_body = soup_body.find_all('div', class_='post__text')
            if keywords_in(post_body):
                print(post_time.text, post_title, href)


if __name__ == '__main__':
    main()
