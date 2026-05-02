# Контекст проекта для Qwen Coder

## Стек
- Язык: Python 3.11+
- UI: Flet 0.25+ (Material Design 3)
- Анимации: `ft.animation(200-400ms, curve='easeOut/InCubic/Back')`, ft.Transition, ft.AnimatedSwitcher
- Стиль: Минимализм, скруглённые углы, тени, сияние, плавные переходы 200–400ms, поддержка тем и конструктор тем, дневная, ночная и автоматическая темы

## Правила генерации кода
1. Разделяй UI-логику, бизнес-логику и анимации по файлам
2. Используй `ft.Container` + `animate=ft.animation(duration, curve)`
3. Все цвета задавай через `ft.colors.PRIMARY`, `ft.colors.SURFACE` и т.д.
4. Не используй `time.sleep()` или блокирующие вызовы в UI-потоке
5. Для сложных переходов используй `ft.AnimatedSwitcher` или `ft.Page.open_snack_bar()`
6. Всегда добавляй `if __name__ == "__main__": ft.app(target=main, view=ft.AppView.FLET_APP)`
7. используй `page.update()` только при необходимости
8. Хранение: `ft.Page.client_storage` для настроек, JSON/SQLite для данных
9. AI: `async def` + `page.run_task` для потокового вывода
10. Структура: `src/ui/`, `src/utils/`, `assets/`

## Пример структуры вызова
async def on_click(e):
    await e.control.page.go("/next")
