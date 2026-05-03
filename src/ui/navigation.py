"""Navigation components for the dashboard."""

import flet as ft


class NavigationMenu(ft.UserControl):
    """Left sidebar navigation menu with icons."""

    def __init__(self, on_nav_change=None, collapsed=False):
        super().__init__()
        self._on_nav_change = on_nav_change
        self._collapsed = collapsed
        self._selected_index = 0

    def _get_destinations(self):
        """Get navigation destinations with icons."""
        return [
            ft.NavigationRailDestination(
                icon=ft.icons.PEOPLE_OUTLINE,
                selected_icon=ft.icons.PEOPLE,
                label="Клиенты",
                label_content_padding=ft.padding.only(left=8),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.DESCRIPTION_OUTLINED,
                selected_icon=ft.icons.DESCRIPTION,
                label="Договоры",
                label_content_padding=ft.padding.only(left=8),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.ART_TRACK_OUTLINED,
                selected_icon=ft.icons.ART_TRACK,
                label="Шаблоны",
                label_content_padding=ft.padding.only(left=8),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PSYCHOLOGY_OUTLINED,
                selected_icon=ft.icons.PSYCHOLOGY,
                label="AI-помощник",
                label_content_padding=ft.padding.only(left=8),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon=ft.icons.SETTINGS,
                label="Настройки",
                label_content_padding=ft.padding.only(left=8),
            ),
        ]

    def _handle_destination_change(self, e):
        """Handle navigation destination change."""
        self._selected_index = e.control.selected_index
        if self._on_nav_change:
            self._on_nav_change(e)
        self.update()

    def _build(self):
        """Build the navigation rail."""
        # TODO: интегрировать с моделью данных для получения пунктов меню
        
        self._rail = ft.NavigationRail(
            extended=not self._collapsed,
            min_width=70 if self._collapsed else 200,
            min_extended_width=200,
            leading=(
                ft.IconButton(
                    icon=ft.icons.MENU,
                    icon_size=24,
                    tooltip="Свернуть меню",
                    on_click=self._toggle_collapse,
                )
                if not self._collapsed
                else None
            ),
            trailing=(
                ft.Column(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.EXPAND_LESS,
                            icon_size=24,
                            tooltip="Развернуть меню",
                            on_click=self._toggle_collapse,
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
                if self._collapsed
                else None
            ),
            selected_index=self._selected_index,
            destinations=self._get_destinations(),
            on_destination_change=self._handle_destination_change,
            bgcolor=ft.colors.SURFACE,
        )

        return self._rail

    def _toggle_collapse(self, e):
        """Toggle collapsed state with animation."""
        self._collapsed = not self._collapsed
        self._rail.extended = not self._collapsed
        self._rail.min_width = 70 if self._collapsed else 200
        self._rail.leading = (
            ft.IconButton(
                icon=ft.icons.MENU,
                icon_size=24,
                tooltip="Свернуть меню",
                on_click=self._toggle_collapse,
            )
            if not self._collapsed
            else None
        )
        self._rail.trailing = (
            ft.Column(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.EXPAND_LESS,
                        icon_size=24,
                        tooltip="Развернуть меню",
                        on_click=self._toggle_collapse,
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            if self._collapsed
            else None
        )
        self.update()

    @property
    def selected_index(self):
        """Get current selected index."""
        return self._selected_index

    @selected_index.setter
    def selected_index(self, value):
        """Set selected index."""
        self._selected_index = value
        if hasattr(self, "_rail"):
            self._rail.selected_index = value
        self.update()
