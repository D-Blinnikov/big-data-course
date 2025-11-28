import sys
from collections import Counter
import re

test_data = ['1293336984	Экология без фанатизма	химик 10 способов приучить детей заботиться об экологии без фанатизма,',
             '1337112293	Страшная химия	ну что ж, телеграм-каналу быть! с вами пищевой технолог и химик оля,'] 

# только буквы (кириллица + латиница), минимум 2 символа
WORD_RE = re.compile(r'[а-яА-ЯёЁ]{4,}')

for line in sys.stdin:
# for line in test_data:
    line = line.strip()
    if not line:
        continue
    
    # channel_id \t name \t text
    parts = line.split('\t', 2)      
    if len(parts) < 3:
        continue

    channel_id, channel_name, text = parts
    
    words = WORD_RE.findall(text.lower())

    if not words:
        continue

    word_counts = Counter(words)
    total_words = sum(word_counts.values())

    for word, count in word_counts.items():
        if total_words == 0:
            tf = 0.0
        else:
            tf = count / total_words
        print(f"{word}\t{channel_id}\t{tf}\t1")