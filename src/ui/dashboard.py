"""Модуль dashboard приложения.

Содержит главную панель с верхней панелью, боковым меню и областью контента.
"""

import flet as ft


class SkeletonLoader:
    """Скелетон-заглушка для состояния загрузки.

    Использует animate_opacity для плавного появления.
    """

    def __init__(self, height=100, width=None):
        self.height = height
        self.width = width

    def build(self):
        """Строит скелетон-заглушку."""
        return ft.Container(
            height=self.height,
            width=self.width,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.ON_SURFACE),
            border_radius=ft.border_radius.all(8),
            opacity=0.3,
            animate_opacity=300,
        )


class ContentArea:
    """Основная область контента с анимацией переключения разделов.

    Использует ft.AnimatedSwitcher с анимацией fadeThrough + slideLeft (300ms).
    """

    def __init__(self):
        self._current_section = "clients"
        self._loading = True
        self.animated_switcher = None

        # TODO: интегрировать с моделью данных
        self.section_content = {
            "clients": self._build_clients_content,
            "contracts": self._build_contracts_content,
            "templates": self._build_templates_content,
            "ai_assistant": self._build_ai_content,
            "settings": self._build_settings_content,
        }

    def _build_skeleton(self):
        """Создает скелетон-заглушки для состояния загрузки."""
        skeleton = SkeletonLoader()
        return ft.Column(
            controls=[
                skeleton.build(),
                skeleton.build(),
                skeleton.build(),
                skeleton.build(),
            ],
            spacing=16,
        )

    def _build_clients_content(self):
        """Контент раздела Клиенты."""
        return ft.Column(
            controls=[
                ft.Text("Клиенты", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Список клиентов будет загружен здесь"),
                # TODO: интегрировать с моделью данных
            ],
            spacing=16,
        )

    def _build_contracts_content(self):
        """Контент раздела Договоры."""
        return ft.Column(
            controls=[
                ft.Text("Договоры", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Список договоров будет загружен здесь"),
                # TODO: интегрировать с моделью данных
            ],
            spacing=16,
        )

    def _build_templates_content(self):
        """Контент раздела Шаблоны."""
        return ft.Column(
            controls=[
                ft.Text("Шаблоны", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Библиотека шаблонов будет загружена здесь"),
                # TODO: интегрировать с моделью данных
            ],
            spacing=16,
        )

    def _build_ai_content(self):
        """Контент раздела AI-помощник."""
        return ft.Column(
            controls=[
                ft.Text("AI-помощник", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Интерфейс AI-помощника будет загружен здесь"),
                # TODO: интегрировать с моделью данных
            ],
            spacing=16,
        )

    def _build_settings_content(self):
        """Контент раздела Настройки."""
        return ft.Column(
            controls=[
                ft.Text("Настройки", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Панель настроек будет загружена здесь"),
                # TODO: интегрировать с моделью данных
            ],
            spacing=16,
        )

    def _get_current_content(self):
        """Получает контент текущего раздела."""
        if self._loading:
            return self._build_skeleton()
        builder = self.section_content.get(self._current_section, self._build_clients_content)
        return builder()

    def set_section(self, section_id: str):
        """Устанавливает текущий раздел и запускает анимацию переключения."""
        self._current_section = section_id
        self._loading = False
        if self.animated_switcher:
            self.animated_switcher.content = self._get_current_content()

    def set_loading(self, loading: bool):
        """Устанавливает состояние загрузки."""
        self._loading = loading
        if self._loading and self.animated_switcher:
            self.animated_switcher.content = self._build_skeleton()

    def build(self):
        """Строит компонент области контента."""
        self.animated_switcher = ft.AnimatedSwitcher(
            content=self._build_skeleton() if self._loading else self._build_clients_content(),
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=300,
            switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
            switch_out_curve=ft.AnimationCurve.EASE_IN_OUT,
        )

        return ft.Container(
            content=self.animated_switcher,
            padding=ft.padding.all(24),
            expand=True,
        )


class TopAppBar:
    """Верхняя панель с поиском и переключателем темы."""

    def __init__(self, on_theme_toggle, on_search_change=None):
        self.on_theme_toggle = on_theme_toggle
        self.on_search_change = on_search_change
        self._is_dark = False
        self.search_field = None
        self.theme_toggle = None

    def _toggle_theme(self, e):
        """Переключает тему приложения."""
        self._is_dark = not self._is_dark
        self.on_theme_toggle(self._is_dark)

    def _on_search_change(self, e):
        """Обработчик изменения поискового запроса."""
        if self.on_search_change:
            self.on_search_change(e.control.value)

    def build(self):
        """Строит компонент верхней панели."""
        self.search_field = ft.TextField(
            hint_text="Поиск...",
            prefix_icon=ft.icons.SEARCH,
            expand=True,
            on_change=self._on_search_change,
            border_radius=ft.border_radius.all(20),
        )

        self.theme_toggle = ft.IconButton(
            icon=ft.icons.DARK_MODE_OUTLINED,
            on_click=self._toggle_theme,
            tooltip="Переключить тему",
        )

        return ft.Container(
            content=ft.Row(
                controls=[
                    self.search_field,
                    ft.IconButton(icon=ft.icons.NOTIFICATIONS_OUTLINED),
                    self.theme_toggle,
                    ft.CircleAvatar(
                        content=ft.Text("U", size=14),
                        radius=16,
                        bgcolor=ft.colors.PRIMARY,
                        color=ft.colors.ON_PRIMARY,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=8),
            bgcolor=ft.colors.SURFACE,
            elevation=2,
        )


class Dashboard:
    """Главный экран приложения (dashboard).

    Содержит:
    - Левое боковое меню с иконками
    - Верхнюю панель с поиском и переключателем темы
    - Основную область контента с анимацией переключения

    Адаптивность:
    - На экранах >= 800px: боковое меню видно
    - На экранах < 800px: меню скрывается в гамбургер
    """

    def __init__(self, page: ft.Page):
        self.page = page
        self._current_section = "clients"
        self._is_mobile = False
        self.content_area = None
        self.navigation = None
        self.sidebar = None
        self.top_bar = None
        self.main_row = None

    def _on_nav_change(self, section_id: str):
        """Обработчик переключения раздела навигации."""
        self._current_section = section_id
        if self.content_area:
            self.content_area.set_section(section_id)

    def _on_theme_toggle(self, is_dark: bool):
        """Обработчик переключения темы."""
        self.page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        self.page.update()

    def _on_resize(self, e):
        """Обработчик изменения размера окна."""
        window_width = self.page.window.width
        self._is_mobile = window_width < 800

        if self._is_mobile:
            # На мобильных скрываем sidebar и показываем hamburger
            if self.sidebar:
                self.sidebar.visible = False
            self.page.drawer = self.navigation.build_drawer()
        else:
            if self.sidebar:
                self.sidebar.visible = True
            self.page.drawer = None

        self.page.update()

    def _on_page_loaded(self, e):
        """Обработчик загрузки страницы - убираем скелетон после загрузки данных."""
        # Имитация загрузки данных (в реальности здесь будет вызов API)
        # TODO: интегрировать с моделью данных
        if self.content_area:
            self.content_area.set_loading(False)

    def build(self):
        """Строит главный экран dashboard."""
        from src.ui.navigation import ResponsiveNavigation

        # Создаем компоненты
        self.content_area = ContentArea()
        self.navigation = ResponsiveNavigation(on_nav_change=self._on_nav_change)
        self.sidebar = self.navigation.build()
        self.top_bar = TopAppBar(on_theme_toggle=self._on_theme_toggle)

        # Основной layout
        self.main_row = ft.Row(
            controls=[
                # Боковое меню
                ft.Container(
                    content=self.sidebar,
                    bgcolor=ft.colors.SURFACE,
                    # Анимация scale при сворачивании
                    animate_scale=200,
                ),
                # Основная область
                ft.VerticalDivider(width=1),
                ft.Column(
                    controls=[
                        self.top_bar.build(),
                        ft.Divider(height=1),
                        self.content_area.build(),
                    ],
                    spacing=0,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

        # Подписываемся на события
        self.page.on_resize = self._on_resize

        # Загружаем данные после отображения
        self.page.on_loaded = self._on_page_loaded

        return self.main_row


def create_dashboard(page: ft.Page) -> Dashboard:
    """Фабричная функция для создания dashboard.

    Args:
        page: Экземпляр страницы Flet.

    Returns:
        Настроенный экземпляр Dashboard.
    """
    return Dashboard(page=page)
