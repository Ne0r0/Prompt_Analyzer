from flask import Flask, request
import json

app = Flask(__name__)

FILE_NAME = "saved_text.json"

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

if __name__ == "__main__":
    app.run(debug=True)