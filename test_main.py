import unittest

from main import group_wines_by_category


class GroupWinesByCategoryTests(unittest.TestCase):
    def test_groups_wines_in_expected_order(self) -> None:
        wines = [
            {"Название": "Кокур", "Категория": "Напитки"},
            {"Название": "Белая леди", "Категория": "Белые вина"},
            {"Название": "Черный лекарь", "Категория": "Красные вина"},
        ]

        grouped = group_wines_by_category(wines)

        self.assertEqual(list(grouped.keys()), ["Белые вина", "Красные вина", "Напитки"])
        self.assertEqual(grouped["Белые вина"][0]["Название"], "Белая леди")
        self.assertEqual(grouped["Красные вина"][0]["Название"], "Черный лекарь")
        self.assertEqual(grouped["Напитки"][0]["Название"], "Кокур")

    def test_puts_unknown_category_after_default_groups(self) -> None:
        wines = [
            {"Название": "Эксперимент", "Категория": "Премиум"},
            {"Название": "Без категории"},
        ]

        grouped = group_wines_by_category(wines)

        self.assertEqual(list(grouped.keys()), ["Премиум", "Без категории"])
        self.assertEqual(grouped["Премиум"][0]["Название"], "Эксперимент")
        self.assertEqual(grouped["Без категории"][0]["Название"], "Без категории")


if __name__ == "__main__":
    unittest.main()
