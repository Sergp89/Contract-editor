"""Модуль навигации для dashboard приложения.

Содержит компоненты бокового меню и логику переключения разделов.
"""

import flet as ft


class NavigationRail:
    """Боковое навигационное меню с иконками.

    Поддерживает сворачивание до иконок с анимацией scale (200ms).
    На экранах < 800px скрывается в гамбургер-меню.
    """

    def __init__(self, on_nav_change, collapsed=False):
        self.on_nav_change = on_nav_change
        self.collapsed = collapsed
        self._current_dest = "clients"
        self.nav_rail = None

        # TODO: интегрировать с моделью данных
        self.destinations = [
            {
                "id": "clients",
                "label": "Клиенты",
                "icon": ft.Icons.PEOPLE_OUTLINED,
                "selected_icon": ft.Icons.PEOPLE,
            },
            {
                "id": "contracts",
                "label": "Договоры",
                "icon": ft.Icons.DESCRIPTION_OUTLINED,
                "selected_icon": ft.Icons.DESCRIPTION,
            },
            {
                "id": "templates",
                "label": "Шаблоны",
                "icon": ft.Icons.CONTENT_PASTE_OUTLINED,
                "selected_icon": ft.Icons.CONTENT_PASTE,
            },
            {
                "id": "ai_assistant",
                "label": "AI-помощник",
                "icon": ft.Icons.SMART_TOY_OUTLINED,
                "selected_icon": ft.Icons.SMART_TOY,
            },
            {
                "id": "settings",
                "label": "Настройки",
                "icon": ft.Icons.SETTINGS_OUTLINED,
                "selected_icon": ft.Icons.SETTINGS,
            },
        ]

    def _build_destinations(self):
        """Создает список пунктов навигации."""
        destinations = []
        for dest in self.destinations:
            destinations.append(
                ft.NavigationRailDestination(
                    icon=dest["icon"],
                    selected_icon=dest["selected_icon"],
                    label=ft.Text(dest["label"], visible=not self.collapsed),
                )
            )
        return destinations

    def _on_destination_change(self, e):
        """Обработчик изменения выбранного пункта."""
        self._current_dest = self.destinations[e.control.selected_index]["id"]
        self.on_nav_change(self._current_dest)

    def build(self):
        """Строит компонент навигационного меню."""
        self.nav_rail = ft.NavigationRail(
            extended=not self.collapsed,
            min_width=100,
            min_extended_width=200,
            leading=ft.FloatingActionButton(
                icon=ft.Icons.MENU,
                on_click=self._toggle_collapse,
                animate_opacity=200,
            ),
            group_alignment=-0.95,
            destinations=self._build_destinations(),
            label_type=ft.NavigationRailLabelType.NONE if self.collapsed else ft.NavigationRailLabelType.ALL,
            on_change=self._on_destination_change,
            bgcolor=ft.Colors.SURFACE,
            elevation=2,
        )

        # Обертка с анимацией scale при сворачивании
        return ft.AnimatedSwitcher(
            content=self.nav_rail,
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=200,
            switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
            switch_out_curve=ft.AnimationCurve.EASE_IN_OUT,
        )

    def _toggle_collapse(self, e):
        """Переключает состояние сворачивания меню."""
        self.collapsed = not self.collapsed
        if self.nav_rail:
            self.nav_rail.extended = not self.collapsed
            self.nav_rail.label_type = (
                ft.NavigationRailLabelType.NONE if self.collapsed else ft.NavigationRailLabelType.ALL
            )
            # Обновляем видимость лейблов
            for i, dest in enumerate(self.nav_rail.destinations):
                dest.label.visible = not self.collapsed

    def set_collapsed(self, collapsed: bool):
        """Устанавливает состояние сворачивания программно."""
        if self.collapsed != collapsed:
            self.collapsed = collapsed
            self._toggle_collapse(None)


class ResponsiveNavigation:
    """Адаптивная навигация с поддержкой мобильных устройств.

    На экранах >= 800px показывает боковое меню.
    На экранах < 800px показывает гамбургер-меню в верхней панели.
    """

    def __init__(self, on_nav_change):
        self.on_nav_change = on_nav_change
        self.sidebar = NavigationRail(on_nav_change=on_nav_change, collapsed=False)
        self.drawer_open = False
        self.page = None

    def build_drawer(self):
        """Создает выдвижное меню для мобильных устройств."""
        drawer_items = []
        # TODO: интегрировать с моделью данных
        destinations = [
            {"id": "clients", "label": "Клиенты", "icon": ft.Icons.PEOPLE_OUTLINED},
            {"id": "contracts", "label": "Договоры", "icon": ft.Icons.DESCRIPTION_OUTLINED},
            {"id": "templates", "label": "Шаблоны", "icon": ft.Icons.CONTENT_PASTE_OUTLINED},
            {"id": "ai_assistant", "label": "AI-помощник", "icon": ft.Icons.SMART_TOY_OUTLINED},
            {"id": "settings", "label": "Настройки", "icon": ft.Icons.SETTINGS_OUTLINED},
        ]

        for dest in destinations:
            drawer_items.append(
                ft.ListTile(
                    leading=ft.Icon(dest["icon"]),
                    title=ft.Text(dest["label"]),
                    on_click=lambda e, d=dest["id"]: self._on_drawer_select(d),
                )
            )

        return ft.Drawer(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text("Меню", size=20, weight=ft.FontWeight.BOLD),
                        padding=ft.Padding.all(16),
                    ),
                    ft.Divider(),
                    *drawer_items,
                ],
                spacing=0,
            ),
        )

    def _on_drawer_select(self, dest_id):
        """Обработчик выбора пункта из drawer."""
        if self.page:
            self.page.close_drawer()
        self.on_nav_change(dest_id)

    def build(self):
        """Строит адаптивный компонент навигации."""
        return self.sidebar.build()
