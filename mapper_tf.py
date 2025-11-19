#!/usr/bin/env python3
# mapper_tf.py — исправленная версия для русского текста + латиницы

import sys
from collections import Counter
import re

# Регулярка: только буквы (кириллица + латиница), минимум 2 символа
WORD_RE = re.compile(r'[а-яА-ЯёЁ]{4,}')

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    parts = line.split('\t', 2)      # channel_id \t name \t text
    if len(parts) < 3:
        continue

    channel_id, channel_name, text = parts

    # Ищем только настоящие слова
    words = WORD_RE.findall(text.lower())

    if not words:
        continue

    word_counts = Counter(words)
    total_words = sum(word_counts.values())   # уже только валидные слова

    for word, count in word_counts.items():
        if total_words == 0:
            tf = 0.0
        else:
            tf = count / total_words
        print(f"{word}\t{channel_id}\t{tf}\t1")