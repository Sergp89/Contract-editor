"""Main application entry point."""

import flet as ft
from src.ui import create_dashboard


def main(page: ft.Page):
    """Main application function."""
    page.title = "Contract Editor Dashboard"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    
    # Create and add dashboard
    dashboard = create_dashboard()
    page.add(dashboard)


if __name__ == "__main__":
    ft.run(target=main)
