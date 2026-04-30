# Russian NER for Personal Names (ФИО)

Извлечение фамилий, имён и отчеств из русского текста с использованием предобученной модели `XLM-RoBERTa`.

## 📋 Описание проекта

Проект решает задачу извлечения персон (ФИО) из текста с помощью NER. 
Выбрал модель `FacebookAI/xlm-roberta-large-finetuned-conll03-english` обрабатывает русскоязычные тексты и возвращает структурированные данные.

### Файлы:
* Основной ресерч и работа: [research.ipynb](research.ipynb)
* Готовый скрипт для запуска: [main.py](main.py)

### Результаты:
| Текст (gt) | Результат (pred) |
|-------|-----------|
| КОБАЛАВА МАКСИМ ЮРЬЕВИЧ | КОБАЛАВА МАКСИМ ЮРЕВИЧ |
| ДАУЭ СВЕТЛАНА АЛЕКСАНДРОВНА | ДАУЭ СВЕТЛАНА АЛЕКСАНДРОВНА |
| СОЛДАТОВА НАДЕЖДА ВАСИЛЬЕВНА | СОЛДАТОВА НАДЕЖДА ВАС |

## 🚀 Установка и запуск

### 1. Установка Poetry

```bash
# Установка Poetry (если ещё не установлен)
curl -sSL https://install.python-poetry.org | python3 -

# Или через pip
pip install poetry
```
**Документация:** [`https://python-poetry.org/docs/`](https://python-poetry.org/docs/)


### 2. Клонирование репозитория
``` bash
git clone https://github.com/your-username/ner-russian-names.git
cd ner-russian-names
```
### 3.Установка всех зависимостей через Poetry
```bash
poetry install
```

### 4. Активация виртуального окружения
```bash
eval $(poetry env activate)

python main.py
```

