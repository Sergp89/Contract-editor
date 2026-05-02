"""Точка входа приложения Flet.

Пример использования dashboard с главной страницей.
"""

import flet as ft

from src.ui import create_dashboard


def main(page: ft.Page):
    """Основная функция приложения.

    Args:
        page: Экземпляр страницы Flet.
    """
    page.title = "Dashboard App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0

    # Создаем и добавляем dashboard
    dashboard = create_dashboard(page)
    page.add(dashboard)


if __name__ == "__main__":
    ft.app(target=main)
