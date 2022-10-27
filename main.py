from http import HTTPStatus
from typing import List

import requests
from bs4 import BeautifulSoup


def parse_response(response) -> List[str]:
    result = list()
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find('ol').find_all('li')

    for element in elements:
        result.append(element.text)

    return result


def get_ideas() -> List[str]:
    base_url = 'https://www.ideasgrab.com/'
    responses = list()

    while True:
        count = len(responses)
        response = requests.get(url=f'{base_url}ideas-{count * 1000}-{count * 1000 + 1000}')
        if response.status_code == HTTPStatus.NOT_FOUND:
            break
        responses.append(response)

    responses.reverse()
    responses.append(requests.get(url=base_url))

    ideas = list()

    for response in responses:
        result = parse_response(response)
        result.reverse()

        ideas += result

    return ideas


def main():
    ideas = get_ideas()

    for seq, idea in enumerate(ideas, 1):
        print(f'{seq}. {idea}')


if __name__ == '__main__':
    main()
