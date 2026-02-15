from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape # pyright: ignore[reportMissingImports]
import pandas as pd
from pprint import pprint


exel_file = pd.read_excel('wine2.xlsx')
data = exel_file.to_dict(orient='records')
grouped = {}

for item in data:   # data = df.to_dict(orient="records")
    category = item["Категория"]

    if category not in grouped:
        grouped[category] = []

    grouped[category].append(item)

pprint(grouped, sort_dicts=False)
env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('template.html')
age = "{}".format(datetime.datetime.now().year - 1920)
def years_word(n: int) -> str:
    n = abs(n)  
    if 11 <= n % 100 <= 14:
        return "лет"
    last = n % 10
    if last == 1:
        return "год"
    if 2 <= last <= 4:
        return "года"
    return "лет"


rendered_page = template.render(
    age=age,
    years_word=years_word(int(age)),
    data=data,
    
)
with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)
server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
