from flask import Flask, request, jsonify
import json
from main import TextAnalyzerApp
from logger import logger # DEBUG logger


app = Flask(__name__)
analyzer_app = TextAnalyzerApp()

FILE_NAME = "data/saved_text.json"

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
@app.route("/save_text", methods=["POST"])
def save_text_api() -> tuple[dict[str, str], int]:
    data: dict[str, str] = request.json or {}
    text: str | None = data.get("text")

    if not text:
        return {"error": "No text provided"}, 400
    
    save_text(text)
    return {"message": "Text saved successfully"}, 200

# API to retrieve endpoint text
@app.route("/get_text", methods=["GET"])
def get_text_api() -> tuple[dict[str, str], int]:
    text: str | None = get_text()

    if text:
        return {"text": text}, 200
    
    return {"error": "No text found"}, 404

# Endpoint for entering new text
@app.route("/enter_text", methods=["POST"])
def enter_text():
    data = request.json or {}
    text = data.get("text")

    if not text or len(text) < 15:
        return jsonify({"error": "Text is too short. Please provide at least 5 sentences."}), 400

    analyzer_app.enter_text(text)
    return jsonify({"message": "Text entered successfully."}), 200

# Endpoint to get analysis report
@app.route("/get_report", methods=["GET"])
def get_report():
    report = analyzer_app.get_report()
    return jsonify(report), 200

# Endpoint to get the number of words
@app.route("/get_word_count", methods=["GET"])
def get_word_count():
    return jsonify({"words_count": analyzer_app.show_num_of_words()}), 200

# Endpoint to get the number of sentences
@app.route("/get_sentence_count", methods=["GET"])
def get_sentence_count():
    return jsonify({"sentence_count": analyzer_app.show_num_of_sentences()}), 200

# Endpoint to get the amount of numbers in text
@app.route("/get_number_count", methods=["GET"])
def get_number_count():
    return jsonify({"number_count": analyzer_app.show_count_of_num()}), 200

# Endpoint to retrieve the most frequent word or words
@app.route("/get_common_words", methods=["GET"])
def get_common_words():
    return jsonify({"common_words": analyzer_app.show_most_common_words()}), 200

logger.info("Logger test: this message should appear in the file logs/app.log") # DEBUG logger

if __name__ == "__main__":
    app.run(debug=True)