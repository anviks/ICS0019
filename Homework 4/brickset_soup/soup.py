import json
import re

from bs4 import BeautifulSoup
import requests


def parse(url: str, bricks_data: list = None):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    brick_list = soup.find_all("article", class_="set")

    if bricks_data is None:
        bricks_data = []

    for brick in brick_list:
        title = brick.h1.get_text()
        if title == "{?}":
            continue

        rrp = brick.find("dt", string="RRP")

        if rrp is None:
            continue

        price = re.findall(r"(?<= )[\d.]+€", rrp.find_next("dd").get_text())

        if not price:
            continue

        img_src = brick.a["href"]

        data = {
            "Title": title,
            "Price": price[0],
            "Picture href": img_src
        }

        bricks_data.append(data)

    next_page = soup.find("li", class_="next").a
    if next_page is not None:
        parse(next_page["href"], bricks_data)

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(bricks_data, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    parse("https://brickset.com/sets/year-2023")
