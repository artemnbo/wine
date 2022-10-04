from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict
import datetime
import pandas
import os
from dotenv import load_dotenv

YEAR_OF_FOUNDATION = 1920


def format_year_spelling(year):
    if 10 < year / 100 < 20:
        return f"{year} лет"
    elif year % 100 == 1:
        return f"{year} год"
    elif 1 < year % 100 < 5:
        return f"{year} годa"
    else:
        return f"{year} лет"


def main():
    load_dotenv()
    data_xls = os.getenv('WINE_DATA_XLS', default='wine.xlsx')

    drinks_data_frame = pandas.read_excel(data_xls, keep_default_na=False)
    drinks_records = drinks_data_frame.to_dict('records')

    drinks = defaultdict(list)
    for drink in drinks_records:
        drinks[drink['Категория']].append(drink)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    current_year = datetime.datetime.now().year
    winery_age = current_year - YEAR_OF_FOUNDATION
    template = env.get_template('template.html')

    rendered_page = template.render(
        winery_age=format_year_spelling(winery_age),
        drinks=drinks
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
