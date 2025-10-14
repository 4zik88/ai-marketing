#!/bin/bash
# Скрипт быстрой установки AI Marketing

echo "================================"
echo "AI Marketing - Установка"
echo "================================"
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден. Установите Python 3.8 или выше."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python версия: $PYTHON_VERSION"

# Создание виртуального окружения
echo ""
echo "Создание виртуального окружения..."
python3 -m venv venv

# Активация окружения
echo "Активация окружения..."
source venv/bin/activate

# Установка зависимостей
echo ""
echo "Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

# Создание .env если его нет
if [ ! -f .env ]; then
    echo ""
    echo "Создание файла конфигурации .env..."
    cp .env.example .env
    echo "✓ Файл .env создан"
    echo ""
    echo "⚠️  ВАЖНО: Отредактируйте файл .env и добавьте ваш API ключ!"
    echo "   Откройте файл: nano .env"
    echo "   Или: open .env"
else
    echo ""
    echo "✓ Файл .env уже существует"
fi

# Создание директории output
mkdir -p output

echo ""
echo "================================"
echo "✓ Установка завершена!"
echo "================================"
echo ""
echo "Следующие шаги:"
echo "1. Активируйте окружение: source venv/bin/activate"
echo "2. Добавьте API ключ в файл .env"
echo "3. Запустите: python main.py analyze https://example.com"
echo ""
echo "Документация: README.md"
echo "Быстрый старт: QUICKSTART.md"
echo ""

