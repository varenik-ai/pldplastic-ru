#!/bin/bash
# Двойной клик на этом файле запустит скачивание всех фотографий

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
echo "📂 Папка: $DIR"
echo ""
bash download-media.sh
echo ""
echo "Нажмите Enter для закрытия..."
read
