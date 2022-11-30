import requests
from bs4 import BeautifulSoup
from typing import Tuple
import argparse


TEST = 0

def build_url(year: int, day: int, type: str = "input") -> str:
    assert type in ["input", "answer"]
    return f"https://adventofcode.com/{year}/day/{day}/{type}"

def get_cookie(fp: str = ".env-sample") -> str:
    with open(fp, "r") as f:
        line = f.readlines()[0]
        line = line[:-1]
        toks = line.split('session=')
        return toks[1]


def get_input(url: str, output_fp: str = "input.txt") -> str:
    response = requests.get(url, cookies = {"session": get_cookie()})
    open(output_fp, "wb").write(response.content)
    print(f"Saved input for {url=} to {output_fp=}")

    return response.content


def submit_answer(url: str, answer: str, level: str) -> Tuple[bool, str]:

    data = {"level": level, "answer": answer}
    r = requests.post(url, data=data, cookies = {"session": get_cookie()})

    status_code = r.status_code
    if status_code != 200:
        print(f"Something went wrong with the request")
        return False, f"{status_code=}\n" + "---" * 100 + "\n" + r.content
    else:
        soup = BeautifulSoup(r.content, "html.parser")
        article = soup.find('article')
        paragraphs = article.find_all('p')
        response = ""
        for paragraph in paragraphs:
            response += paragraph.text

        print(f"{response=}")
        if "right answer" in response:
            return True, response
        else:
            return False, response



if __name__ == '__main__':

    parser = argparse.ArgumentParser("AOC CLI")
    parser.add_argument("--download_input", action="store_true")
    parser.add_argument("--submit_answer", action="store_true")
    parser.add_argument("--year", '-y', type=int, default=2022)
    parser.add_argument("--day", '-d', type=int, required=True)
    parser.add_argument("--level", '-l', type=int, required=True)

    args = parser.parse_args()


    if args.submit_answer:
        answer = input("Provide answer: ")

        status, msg = submit_answer(
            url=build_url(year=args.year, day=args.day, type="answer"),
            answer=answer,
            level=args.level
        )
        print(f"{status=}\n{msg=}")
    elif args.download_input:
        get_input(url=build_url(year=args.year, day=args.day))
