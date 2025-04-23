from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
from collections import Counter
import re
import math


router = APIRouter()

@router.post("/upload")
async def handle_upload(file: UploadFile = File(...)):
    content_bytes = await file.read()
    content = content_bytes.decode('utf-8')
    words = re.findall(r"\b\w+\b", content.lower())
    word_counts = Counter(words)
    total_words = sum(word_counts.values())

    tf_values = {}
    for word, count in word_counts.items():
        tf_values[word] = count / total_words
    doc_freq = {}
    for word in word_counts:
        doc_freq[word] = 1

    num_docs = 1
    idf_values = {}
    for word, df in doc_freq.items():
        idf_values[word] = math.log(num_docs / df) if df != 0 else 0

    result = []
    for word in tf_values:
        result.append({
            "word": word,
            "tf": round(tf_values[word], 4),
            "idf": round(idf_values[word], 4)
        })

    result_sorted = sorted(result, key=lambda x: x["idf"], reverse=True)[:50]

    return {"results": result_sorted}
