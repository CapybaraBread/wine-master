import argparse
from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape  # pyright: ignore[reportMissingImports]


EXCEL_PATH = "wine_catalog.xlsx"
TEMPLATE_PATH = "template.html"
OUTPUT_PATH = "index.html"
HOST = "0.0.0.0"
PORT = 8000
FOUNDATION_YEAR = 1920


def get_years_word(years: int) -> str:
    years = abs(years)
    if 11 <= years % 100 <= 14:
        return "лет"
    last_digit = years % 10
    if last_digit == 1:
        return "год"
    if 2 <= last_digit <= 4:
        return "года"
    return "лет"


def load_wines(excel_path: str) -> list[dict]:
    data_frame = pd.read_excel(excel_path)
    return data_frame.to_dict(orient="records")


def has_value(value: object) -> bool:
    if value is None:
        return False
    if pd.isna(value):
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return True


def prepare_wines(wines: list[dict]) -> list[dict]:
    prepared_wines = []
    for wine in wines:
        prepared_wine = dict(wine)
        prepared_wine["show_offer"] = has_value(prepared_wine.get("Акция"))
        prepared_wine["show_grape"] = has_value(prepared_wine.get("Сорт"))
        prepared_wines.append(prepared_wine)
    return prepared_wines


def group_wines_by_category(wines: list[dict]) -> dict[str, list[dict]]:
    wines_by_category: dict[str, list[dict]] = defaultdict(list)
    for wine in wines:
        category_name = wine.get("Категория", "Без категории")
        wines_by_category[category_name].append(wine)
    return dict(wines_by_category)


def render_index_page(wines_by_category: dict[str, list[dict]]) -> None:
    environment = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"]),
    )
    template = environment.get_template(TEMPLATE_PATH)
    age = datetime.now().year - FOUNDATION_YEAR
    years_word = get_years_word(age)
    rendered_page = template.render(
        age=age,
        years_word=years_word,
        wines_by_category=wines_by_category,
    )
    with open(OUTPUT_PATH, "w", encoding="utf8") as file:
        file.write(rendered_page)


def run_server() -> None:
    server = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
    server.serve_forever()


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Запуск сайта магазина вина")
    parser.add_argument("--excel-path", default=EXCEL_PATH)
    return parser.parse_args()


def main() -> None:
    args = get_args()
    wines = load_wines(args.excel_path)
    prepared_wines = prepare_wines(wines)
    wines_by_category = group_wines_by_category(prepared_wines)
    render_index_page(wines_by_category)
    run_server()


if __name__ == "__main__":
    main()
