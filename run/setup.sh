#!/bin/bash
# Создаём структуру проекта для Python UI с анимациями

PROJECT_DIR="my-python-ui-app"
mkdir -p $PROJECT_DIR/{src/ui,src/utils,assets,tests}

# 📄 pyproject.toml — современный стандарт управления зависимостями
cat > $PROJECT_DIR/pyproject.toml << 'EOF'
[project]
name = "my-python-ui-app"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["flet>=0.25.0"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.black]
line-length = 100
EOF

# 📄 requirements.txt — для совместимости с pip
cat > $PROJECT_DIR/requirements.txt << 'EOF'
flet>=0.25.0
ruff>=0.4.0
black>=24.0
EOF

# 📄 .gitignore (дополнения для Flet/Python)
cat > $PROJECT_DIR/.gitignore << 'EOF'
__pycache__/
*.pyc
.venv/
.env
*.log
.flet/
dist/
build/
EOF

# 📄 src/main.py — точка входа с базовой настройкой
cat > $PROJECT_DIR/src/main.py << 'EOF'
import flet as ft

def main(page: ft.Page):
    page.title = "My Python UI App"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # Анимированный заголовок
    title = ft.Text(
        "Добро пожаловать!",
        size=32,
        weight=ft.FontWeight.BOLD,
        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT)
    )
    
    # Кнопка с эффектом нажатия
    btn = ft.ElevatedButton(
        "Нажми меня",
        on_click=lambda e: animate_click(e, title),
        style=ft.ButtonStyle(
            animation_duration=200,
            shape=ft.RoundedRectangleBorder(radius=12)
        )
    )
    
    page.add(title, btn)

def animate_click(e, target: ft.Control):
    """Простая анимация при клике"""
    target.scale = 1.1
    target.update()
    ft.animation.wait(100)
    target.scale = 1.0
    target.update()

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)
EOF

# 📄 README.md — инструкция для разработчика
cat > $PROJECT_DIR/README.md << 'EOF'
# 🎨 My Python UI App

Современное приложение на Python с анимациями (Flet).

## 🚀 Быстрый старт
```bash
# Клонируйте репо
git clone https://github.com/ваш-ник/my-python-ui-app.git
cd my-python-ui-app

# Создайте окружение
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Установите зависимости
pip install -r requirements.txt

# Запустите
python -m src.main
