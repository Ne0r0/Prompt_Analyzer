from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import TextAnalyzerApp
from logger import logger # DEBUG logger
import json

app = FastAPI()
analyzer_app = TextAnalyzerApp()

FILE_NAME = "data/saved_text.json"

# Data model for incoming text
class TextInput(BaseModel):
    text: str

# Stores text in a JSON file
def save_text(text: str) -> None:
    data: dict[str, str] = {"text": text}
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)

# Gets text from a JSON file
def get_text() -> str | None:
    try:
        with open(FILE_NAME, "r") as file:
            data: dict[str, str] = json.load(file)
            return data.get("text")
    except FileNotFoundError:
        return None
    
# API to store endpoint text
@app.post("/save_text")
def save_text_api(input_text: TextInput) -> dict[str, str]:
    if not input_text.text:
        raise HTTPException(status_code=400, detail="No text provided")
    save_text(input_text.text)
    return {"message": "Text saved successfully"}

# API to retrieve endpoint text
@app.get("/get_text")
def get_text_api() -> dict[str, str]:
    text: str | None = get_text()
    if not text:
        raise HTTPException(status_code=400, detail="No text found")
    return {"text": text}

# Endpoint for entering new text
@app.post("/enter_text")
def enter_text(input_text: TextInput) -> dict[str, str]:
    if not input_text.text or len(input_text.text) < 15:
        raise HTTPException(status_code=400, detail="Text is too short. Please provide at least 5 sentences.")
    analyzer_app.enter_text(input_text.text)
    return {"message": "Text entered successfully."}

# Endpoint to get analysis report
@app.get("/get_report")
def get_report() -> dict[str, str | int]:
    return analyzer_app.get_report()

# Endpoint to get the number of words
@app.get("/get_word_count")
def get_word_count() -> dict[str, int | str]:
    return {"words_count": analyzer_app.show_num_of_words()}

# Endpoint to get the number of sentences
@app.get("/get_sentence_count")
def get_sentence_count() -> dict[str, int | str]:
    return {"sentence_count": analyzer_app.show_num_of_sentences()}

# Endpoint to get the amount of numbers in text
@app.get("/get_number_count")
def get_number_count() -> dict[str, int | str]:
    return {"number_count": analyzer_app.show_count_of_num()}

# Endpoint to retrieve the most frequent word or words
@app.get("/get_common_words")
def get_common_words() -> dict[str, str | list[str]]:
    return {"common_words": analyzer_app.show_most_common_words()}

logger.info("Logger test: this message should appear in the file logs/app.log") # DEBUG logger
