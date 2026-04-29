import os
import sys
import warnings
from pathlib import Path

import spiner

spiner_obj = spiner.Spinner("script is running")


import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

import spiner

spiner_obj = spiner.Spinner("script is running")
spiner_obj.start()

# Скрыть все warnings
warnings.filterwarnings("ignore")

# Подавить stdout/stderr для загрузки модели
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Подавить логи
import logging

logging.disable(logging.CRITICAL)


def aggregate_subtokens_xlm(ner_results):
    aggregated = []
    current_word = ""
    current_entity = None
    current_score = 0.0
    current_start = 0
    current_end = 0

    for item in ner_results:
        word = item["word"]
        score = item["score"]

        if not word.startswith("▁") and current_word:
            current_word += word
            current_score = min(current_score, score)
            current_end = item["end"]
        else:
            if current_word:
                aggregated.append(
                    {"entity": current_entity.replace("U-", ""), "score": current_score, "word": current_word, "start": current_start, "end": current_end}
                )

            current_word = word[1:] if word.startswith("▁") else word
            current_entity = item["entity"]
            current_score = score
            current_start = item["start"]
            current_end = item["end"]

    if current_word:
        aggregated.append(
            {"entity": current_entity.replace("U-", ""), "score": current_score, "word": current_word, "start": current_start, "end": current_end}
        )

    return aggregated


images = sorted([Path("docs_data") / name for name in os.listdir("docs_data")], key=lambda img: img.stem.split("_")[1])
gray_images = [np.array(Image.open(img).convert("L")) for img in images]

thresh_images = []
for idx, image in enumerate(gray_images):
    _, thresh = cv2.threshold(image, 90, 255, cv2.THRESH_BINARY)
    thresh_images.append(thresh)

reader = easyocr.Reader(["ru"])
reader_params = {
    "decoder": "beamsearch",
    "beamWidth": 5,
    "allowlist": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
    # 'blocklist': "!@#$%^&*()_+",
    "min_size": 10,  # убираем мусор
    # rotation_info
}

result = [reader.readtext(img, **reader_params) for img in thresh_images]

# Собираем из вывода, для каждой картинки все значения с уверенностью выше 0.8 и длины >=3 (обычно фамилии больше трех символов)

image_texts_with_high_conf = []
for img in result:
    img_list = []
    for i in img:
        if i[2] > 0.8 and len(i[1]) >= 3:
            img_list.append(i[1])
    image_texts_with_high_conf.append(" ".join(img_list))


model_id = "FacebookAI/xlm-roberta-large-finetuned-conll03-english"

model = AutoModelForTokenClassification.from_pretrained(model_id).cuda()
tokenizer = AutoTokenizer.from_pretrained(model_id)

ner_pipe = pipeline("ner", model=model.eval(), tokenizer=tokenizer)


full_names_list = []

for s in image_texts_with_high_conf:
    raw_outputs = ner_pipe(s, aggregation_strategy=None)
    aggregated = aggregate_subtokens_xlm(raw_outputs)

    name = ""
    for ent in aggregated:
        if ent["entity"] == "I-PER":
            name += ent["word"] + " "
    full_names_list.append(name)

spiner_obj.stop()
print("Result:", full_names_list)
print("✓ Done!")
