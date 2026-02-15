from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

WINERY_FOUNDATION_YEAR = 1920
EXCEL_PATH = "wine3.xlsx"
TEMPLATE_PATH = "template.html"
OUTPUT_PATH = "index.html"
HOST = "0.0.0.0"
PORT = 8000
CATEGORY_ORDER = ("Белые вина", "Красные вина", "Напитки")


def years_word(years: int) -> str:
    years = abs(years)
    if 11 <= years % 100 <= 14:
        return "лет"
    last_digit = years % 10
    if last_digit == 1:
        return "год"
    if 2 <= last_digit <= 4:
        return "года"
    return "лет"


def load_wines(path: str) -> list[dict]:
    import pandas as pd

    excel_file = pd.read_excel(path)
    return excel_file.to_dict(orient="records")


def group_wines_by_category(wines: list[dict]) -> dict[str, list[dict]]:
    grouped_wines: dict[str, list[dict]] = defaultdict(list)
    for wine in wines:
        category = wine.get("Категория", "Без категории")
        grouped_wines[category].append(wine)

    ordered_grouped_wines: dict[str, list[dict]] = {}
    for category in CATEGORY_ORDER:
        if category in grouped_wines:
            ordered_grouped_wines[category] = grouped_wines[category]

    for category, items in grouped_wines.items():
        if category not in ordered_grouped_wines:
            ordered_grouped_wines[category] = items

    return ordered_grouped_wines


def render_index_page(wines: list[dict], grouped_wines: dict[str, list[dict]]) -> None:
    from jinja2 import Environment, FileSystemLoader, select_autoescape  # pyright: ignore[reportMissingImports]

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template(TEMPLATE_PATH)

    age = datetime.now().year - WINERY_FOUNDATION_YEAR
    rendered_page = template.render(
        age=str(age),
        years_word=years_word(age),
        data=wines,
        grouped_data=grouped_wines,
    )

    with open(OUTPUT_PATH, "w", encoding="utf8") as file:
        file.write(rendered_page)


def run_server() -> None:
    server = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
    server.serve_forever()


def main() -> None:
    wines = load_wines(EXCEL_PATH)
    grouped_wines = group_wines_by_category(wines)
    render_index_page(wines, grouped_wines)
    run_server()


if __name__ == "__main__":
    main()
