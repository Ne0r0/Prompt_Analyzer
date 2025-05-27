import logging
import re
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List

logging.basicConfig(
    level=logging.INFO,
    filename="logs/app.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# duomenu klase, ko man reikia, tikslas. Dataklase rezultatams saugoti.
@dataclass
class TextAnalyzerStorage:
    users_text: str
    fixed_text: str
    num_of_words: int
    num_of_sentences: int
    count_of_num: int
    most_com_word: str
# Teksto formatavimo funkcijos, jos dabar lengviau pasiekiamos
# tikrinu ar tai raide ar ne, jei raide padarau didziaja, jei skaicius arba didzioji praleidziu kaip yra.
def cap_sentence(sentence: str) -> str:
    for i, char in enumerate(sentence):
        if char.isalpha():
            return sentence[:i] + char.upper() + sentence[i+1:]
    return sentence

# formatavimas, pakeicia raides i didziasias, kurios eina po tasko.
def form_sentence(text: str) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    formatted = [cap_sentence(s.strip()) for s in sentences]
    return ''.join(formatted)

# abstrakti klase
class TextProcessor(ABC):
    def __init__(self, text: str) -> None:
        self.text: str = text
# sutvarko teksta pagal taisikles
    @abstractmethod
    def clean_text(self) -> str:
        pass
# atlieka pilna anlize ir grazina rezultatus
    @abstractmethod
    def analyze(self) -> TextAnalyzerStorage:
        pass

# Pagrindine teksto analizes klase, paveldi "TextProcessor"
class TextAnalyzerCore(TextProcessor):
    _instance_count: int = 0

    def __init__(self, text: str = "") -> None: # Inicilizuoja nauja "TextAnalyzerCore"
        super().__init__(text) 
        TextAnalyzerCore._instance_count += 1
        logging.info("TextAnalyzer instance created.")
        
# grazina trumpa objekto reprezentacija(rodomus tik pirmos 20 simboliu reiksmes)
    def __repr__(self) -> str:
        return f"TextAnalyzer(text='{self.text[:20]}...')"
# grazina teksto ilgi
    def __len__(self) -> int:
        return len(self.text)
# atnaujina teksta
    def update_text(self, new_text: str) -> None:
        self.text = new_text
        logging.info("Text update.")
# isvalo taksta pagal taisykles
    @property
    def fixed_text(self) -> str: 
        text_with_commas = re.sub(r',(?=\S)', ', ', self.text) # iterpia tarpus po kablelio
        return form_sentence(text_with_commas)
# grazina sukurtu 'TextAnaluzerCore' objektu skaiciu
    @staticmethod
    def get_instance_count() -> int:
        return TextAnalyzerCore._instance_count 
# Skaičiuoja žodžius tekste
    def count_words(self) -> int:
        words = re.findall(r'\b\w+\b', self.text)
        return len(words)
# Skaičiuoja sakinius tekste
    def count_sentences(self) -> int:
        sentences = re.split(r'[.!?]+', self.text)
        sentences = [s for s in sentences if s.strip()]
        return len(sentences)

    def count_numbers(self) -> int:
        numbers = re.findall(r'\d+', self.text)
        return len(numbers)
# Randa dažniausiai pasikartojantį žodį iš teksto 
    def most_common_word(self) -> str:
        words: List[str] = re.findall(r'\b\w+\b', self.text.lower())  # Pašalina skyrybos ženklus

        if not words:
            return ""  # Jei nėra žodžių, grąžiname tuščią eilutę

        word_counts: Dict[str, int] = {}  # Sukuriame žodyną žodžių dažnumui skaičiuoti
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1  # Didiname skaičiavimą

        return max(word_counts, key=lambda word: word_counts[word]) # Grąžiname žodį su didžiausiu pasikartojimų skaičiumi

    def analyze(self) -> TextAnalyzerStorage:
        """Atlieka pilną analizę ir grąžina rezultatus."""
        analysis = TextAnalyzerStorage(
            users_text=self.text,
            fixed_text=self.fixed_text,
            num_of_words=self.count_words(),
            num_of_sentences=self.count_sentences(),
            count_of_num=self.count_numbers(),
            most_com_word=self.most_common_word()
        )
        return analysis

# CLI meniu, work in progress
# def main() -> None:
#     app = TextAnalyzerApp()

#     while True:
#         print("\n===== Prompt Text Analyzer =====")
#         print("1. Enter new text (minimum 5 sentences)")
#         print("2. Get Report")
#         print("3. Show number of words")
#         print("4. Show number of sentences")
#         print("5. Show count of numbers")
#         print("6. Show most common word or words")
#         print("0. Exit")
        
#         choice = input("Enter your choice: ")

#         try:
#             if choice == "1":
#                 app.enter_text()
#             elif choice == "2":
#                 app.show_report
#             elif choice == "3":
#                 app.show_num_of_words()
#             elif choice == "4":
#                 app.show_num_of_sentences()
#             elif choice == "5":
#                 app.show_count_of_num()
#             elif choice == "6":
#                 app.show_most_common_words()
#             elif choice == "0":
#                 print("See you later 👋👋")
#                 break
#             else:
#                 print("Invalid input. Please try again.")
#         except Exception as e:
#             print(f"Error: {e}")

# def enter_text(self) -> None:
#     text_input = input("Enter your text (min 5 sentences): ").strip()
#     if len 

# def show_report(self) -> None:
#         if self.text        


# if __name__ == "__main__":
#     main()
