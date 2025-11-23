import json
import re
import os
import glob
import subprocess

def run(cmd):
    print(f"==> {cmd}")
    subprocess.run(cmd, shell=True, check=True)


NAME_NODE = "hadoop-namenode-1"
HDFS_PATH = "/user/root/tg_channels/docs.txt"

def clean_text(text_parts):
    if isinstance(text_parts, str):
        return re.sub(r'\s+', ' ', text_parts.strip()).lower()
    if isinstance(text_parts, list):
        parts = []
        for part in text_parts:
            if isinstance(part, dict):
                if part.get('type') in ['plain', 'bold', 'italic', 'link', 'mention', 'text_link']:
                    parts.append(part.get('text', ''))
            elif isinstance(part, str):
                parts.append(part)
        return re.sub(r'\s+', ' ', ''.join(parts).strip()).lower()
    return ""

def process_single_json(json_path: str) -> str:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    channel_id = str(data['id'])
    channel_name = data.get('name', 'Unknown').replace('\t', ' ').replace('\n', ' ')

    full_text = []
    for msg in data.get('messages', []):
        if msg.get('type') != 'message':
            continue
        text = msg.get('text')
        if not text:
            continue
        cleaned = clean_text(text)
        if cleaned:
            full_text.append(cleaned)

    doc_text = ' '.join(full_text)
    return f"{channel_id}\t{channel_name}\t{doc_text}\n"

def main():
    json_files = glob.glob("*.json")
    if not json_files:
        print("Ошибка: в текущей папке нет файлов *.json")
        return

    print(f"Найдено {len(json_files)} каналов. Обработка...\n")

    output_file = "all_channels.txt"
    with open(output_file, 'w', encoding='utf-8') as out:
        for i, json_file in enumerate(json_files, 1):
            print(f"  [{i:3}/{len(json_files)}] {json_file}", end="")
            try:
                line = process_single_json(json_file)
                out.write(line)
                print(" ✓")
            except Exception as e:
                print(f" ✗ (ошибка: {e})")

    size_mb = os.path.getsize(output_file) / 1024 / 1024
    print(f"\nСоздан файл all_channels.txt ({size_mb:.1f} МБ)")


    if not os.path.exists(output_file):
        print("Файл не создан — заливка отменена")
        return

    print(f"\nЗагрузка в HDFS → hdfs://{HDFS_PATH}")

    run(f"docker cp \"{os.path.abspath(output_file)}\" {NAME_NODE}:/tmp/all_channels.txt")

    # 2. Создаём папку в HDFS (если нет) и заливаем с перезаписью
    run(f"docker exec {NAME_NODE} hdfs dfs -mkdir -p /user/root/tg_channels")
    run(f"docker exec {NAME_NODE} hdfs dfs -put -f /tmp/all_channels.txt {HDFS_PATH}")

    print(f"\nУспешно загружено в HDFS!")
    print(f"Путь: hdfs://{HDFS_PATH}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nОстановлено руками")
    finally:
         print("\n\Каналы загружены в HDFS!")