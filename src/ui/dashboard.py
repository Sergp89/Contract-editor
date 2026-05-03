"""Dashboard UI components."""

import flet as ft
from typing import Optional, Callable, Any


class SkeletonLoader(ft.Container):
    """Skeleton loader for loading state with animated opacity."""

    def __init__(self, height: float = 100, width: Optional[float] = None):
        # TODO: интегрировать с моделью данных для определения количества скелетонов
        super().__init__(
            height=height,
            width=width,
            bgcolor=ft.colors.ELEVATION_2,
            border_radius=ft.border_radius.all(8),
            animate_opacity=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            opacity=0.7,
        )


class ContentArea(ft.Column):
    """Main content area with animated transitions."""

    def __init__(self):
        super().__init__(spacing=16)
        self._current_index = 0
        self._loading = True
        self._content_map = {
            0: self._build_clients_content(),
            1: self._build_contracts_content(),
            2: self._build_templates_content(),
            3: self._build_ai_content(),
            4: self._build_settings_content(),
        }
        
        # AnimatedSwitcher with fadeThrough + slideLeft animation
        self._animated_switcher = ft.AnimatedSwitcher(
            content=self._get_loading_skeletons(),
            duration=300,
            reverse_duration=300,
            switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
            switch_out_curve=ft.AnimationCurve.EASE_IN_OUT,
            transition=ft.AnimatedSwitcherTransition.FADE,
        )
        self.controls = [self._animated_switcher]

    def _build_clients_content(self):
        """Build clients section content."""
        # TODO: интегрировать с моделью данных для отображения клиентов
        return ft.Column(
            controls=[
                ft.Text("Клиенты", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Список клиентов будет загружен здесь..."),
            ],
            spacing=16,
        )

    def _build_contracts_content(self):
        """Build contracts section content."""
        # TODO: интегрировать с моделью данных для отображения договоров
        return ft.Column(
            controls=[
                ft.Text("Договоры", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Список договоров будет загружен здесь..."),
            ],
            spacing=16,
        )

    def _build_templates_content(self):
        """Build templates section content."""
        # TODO: интегрировать с моделью данных для отображения шаблонов
        return ft.Column(
            controls=[
                ft.Text("Шаблоны", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Библиотека шаблонов будет загружена здесь..."),
            ],
            spacing=16,
        )

    def _build_ai_content(self):
        """Build AI assistant section content."""
        # TODO: интегрировать с моделью данных для AI-помощника
        return ft.Column(
            controls=[
                ft.Text("AI-помощник", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("AI-ассистент готов помочь с документами..."),
            ],
            spacing=16,
        )

    def _build_settings_content(self):
        """Build settings section content."""
        # TODO: интегрировать с моделью данных для настроек
        return ft.Column(
            controls=[
                ft.Text("Настройки", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Параметры приложения будут здесь..."),
            ],
            spacing=16,
        )

    def _get_loading_skeletons(self):
        """Get skeleton loaders for loading state."""
        return ft.Column(
            controls=[
                SkeletonLoader(height=40, width=200),
                SkeletonLoader(height=10),
                SkeletonLoader(height=100),
                SkeletonLoader(height=100),
                SkeletonLoader(height=100),
            ],
            spacing=16,
        )

    def switch_content(self, index: int):
        """Switch to content at given index with animation."""
        self._current_index = index
        self._animated_switcher.content = self._content_map.get(
            index, self._build_clients_content()
        )
        self.update()

    def set_loading(self, loading: bool, page: Optional[ft.Page] = None):
        """Set loading state."""
        self._loading = loading
        if loading:
            self._animated_switcher.content = self._get_loading_skeletons()
        else:
            self._animated_switcher.content = self._content_map.get(
                self._current_index, self._build_clients_content()
            )
        self.update()


class TopAppBar(ft.Row):
    """Top app bar with search and theme toggle."""

    def __init__(self, on_theme_toggle: Optional[Callable] = None, on_search: Optional[Callable] = None):
        super().__init__(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            padding=ft.padding.symmetric(horizontal=16, vertical=8),
        )
        self._on_theme_toggle = on_theme_toggle
        self._on_search = on_search
        self._is_dark = False
        
        # TODO: интегрировать с моделью данных для поиска
        
        self._search_field = ft.TextField(
            hint_text="Поиск...",
            prefix_icon=ft.icons.Icons.SEARCH,
            border=ft.InputBorder.NONE,
            filled=True,
            fill_color=ft.colors.ELEVATION_2,
            expand=True,
            on_change=self._handle_search_change,
        )

        self._theme_button = ft.IconButton(
            icon=ft.icons.Icons.LIGHT_MODE,
            tooltip="Переключить тему",
            on_click=self._handle_theme_toggle,
        )
        
        self.controls = [
            self._search_field,
            ft.VerticalDivider(width=1),
            self._theme_button,
            ft.IconButton(
                icon=ft.icons.Icons.ACCOUNT_CIRCLE_OUTLINED,
                tooltip="Профиль",
            ),
        ]

    def _handle_theme_toggle(self, e):
        """Handle theme toggle button click."""
        self._is_dark = not self._is_dark
        self._theme_button.icon = (
            ft.icons.Icons.DARK_MODE if self._is_dark else ft.icons.Icons.LIGHT_MODE
        )
        if self._on_theme_toggle:
            self._on_theme_toggle(self._is_dark)
        self.update()

    def _handle_search_change(self, e):
        """Handle search field change."""
        if self._on_search:
            self._on_search(e.control.value)


class Dashboard(ft.Column):
    """Main dashboard screen with navigation and content area."""

    def __init__(self):
        super().__init__(expand=True, spacing=0)
        self._nav_menu = None
        self._content_area = None
        self._top_app_bar = None
        self._is_mobile = False
        self._menu_visible = False
        self._page = None

    def _handle_nav_change(self, e):
        """Handle navigation change."""
        if self._content_area:
            self._content_area.switch_content(e.control.selected_index)
            # Simulate loading state when switching sections
            self._content_area.set_loading(True)
            # Use call_later to avoid blocking UI thread
            if self._page:
                self._page.call_later(lambda: self._content_area.set_loading(False))

    def _handle_theme_toggle(self, is_dark: bool):
        """Handle theme toggle."""
        if self._page:
            self._page.theme_mode = (
                ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
            )
            self._page.update()

    def _handle_search(self, query: str):
        """Handle search query."""
        # TODO: интегрировать с моделью данных для поиска
        print(f"Search query: {query}")

    def _toggle_mobile_menu(self, e):
        """Toggle mobile menu visibility."""
        if self._page and hasattr(self, "_drawer"):
            self._page.open(self._drawer)

    def _build_drawer(self):
        """Build drawer for mobile navigation."""
        # TODO: интегрировать с моделью данных для мобильного меню
        
        return ft.NavigationDrawer(
            controls=[
                ft.NavigationDrawerDestination(
                    icon=ft.icons.Icons.PEOPLE_OUTLINE,
                    selected_icon=ft.icons.Icons.PEOPLE,
                    label="Клиенты",
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.icons.Icons.DESCRIPTION_OUTLINED,
                    selected_icon=ft.icons.Icons.DESCRIPTION,
                    label="Договоры",
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.icons.Icons.ART_TRACK_OUTLINED,
                    selected_icon=ft.icons.Icons.ART_TRACK,
                    label="Шаблоны",
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.icons.Icons.PSYCHOLOGY_OUTLINED,
                    selected_icon=ft.icons.Icons.PSYCHOLOGY,
                    label="AI-помощник",
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.icons.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.icons.Icons.SETTINGS,
                    label="Настройки",
                ),
            ],
            on_destination_change=self._handle_drawer_change,
        )

    def _handle_drawer_change(self, e):
        """Handle drawer destination change."""
        if self._content_area:
            self._content_area.switch_content(e.control.selected_index)
            self._content_area.set_loading(True)
            if self._page:
                self._page.call_later(lambda: self._content_area.set_loading(False))
        if hasattr(self, "_drawer") and self._page:
            self._page.close(self._drawer)

    def _check_responsive(self, e=None):
        """Check screen size and adjust layout."""
        if self._page:
            width = self._page.width
            self._is_mobile = width < 800
            if hasattr(self, "_nav_container"):
                self._nav_container.visible = not self._is_mobile
            if hasattr(self, "_hamburger_button"):
                self._hamburger_button.visible = self._is_mobile
            self.update()

    def did_mount(self):
        """Called when control is mounted."""
        if self._page:
            self._page.on_resize = self._check_responsive
            self._check_responsive()
            # Simulate initial data loading
            if self._content_area:
                self._content_area.set_loading(True)
                self._page.call_later(lambda: self._content_area.set_loading(False))

    def will_unmount(self):
        """Called when control is about to be unmounted."""
        if self._page:
            self._page.on_resize = None

    def _build(self):
        """Build the dashboard layout."""
        # Create navigation menu
        self._nav_menu = NavigationMenu(on_nav_change=self._handle_nav_change)
        
        # Create content area
        self._content_area = ContentArea()
        
        # Create top app bar
        self._top_app_bar = TopAppBar(
            on_theme_toggle=self._handle_theme_toggle,
            on_search=self._handle_search,
        )

        # Hamburger button for mobile
        self._hamburger_button = ft.IconButton(
            icon=ft.icons.Icons.MENU,
            tooltip="Меню",
            visible=False,
            on_click=self._toggle_mobile_menu,
        )

        # Navigation container (for desktop)
        self._nav_container = ft.Container(
            content=self._nav_menu,
            bgcolor=ft.colors.SURFACE,
            width=200,
        )

        # Build drawer for mobile
        self._drawer = self._build_drawer()

        # Main layout with Row for desktop
        main_row = ft.Row(
            controls=[
                # Left navigation (desktop)
                self._nav_container,
                # Main content area
                ft.Column(
                    controls=[
                        ft.Container(
                            content=self._top_app_bar,
                            bgcolor=ft.colors.SURFACE,
                        ),
                        ft.Container(
                            content=self._content_area,
                            expand=True,
                            padding=24,
                        ),
                    ],
                    expand=True,
                    spacing=0,
                ),
            ],
            expand=True,
            spacing=0,
        )

        self.controls = [
            ft.Stack(
                controls=[
                    main_row,
                    # Hamburger button overlay for mobile
                    ft.Positioned(
                        left=0,
                        top=0,
                        content=self._hamburger_button,
                    ),
                ],
                expand=True,
            )
        ]
        
        return self.controls


def create_dashboard():
    """Factory function to create dashboard instance."""
    return Dashboard()
