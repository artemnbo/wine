from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict
import datetime
import pandas


def year_ending(year):
    endings = ["лет", "год", "года"]
    num = year % 100
    if 21 > num > 4:
        return f"{year} {endings[0]}"
    num = num % 10
    if num == 1:
        return f"{year} {endings[1]}"
    if 1 < num < 5:
        return f"{year} {endings[2]}"
    return f"{year} {endings[0]}"


current_year = datetime.datetime.now().year
winery_age = current_year - 1920

drinks_data_frame = pandas.read_excel("wine.xlsx", keep_default_na=False)
drinks_records = drinks_data_frame.to_dict('records')

drinks = defaultdict(list)
for drink in drinks_records:
    drinks[drink['Категория']].append(drink)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
rendered_page = template.render(
    winery_age=year_ending(winery_age),
    drinks=drinks
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
