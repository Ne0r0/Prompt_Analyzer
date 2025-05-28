import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List

logging.basicConfig(
    level=logging.INFO,
    filename="logs/app.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Duomenų klasė tekstui saugoti.
@dataclass
class TextAnalyzerStorage:
    users_text: str
    fixed_text: str
    num_of_words: int
    num_of_sentences: int
    count_of_num: int
    most_com_word: str

# Pakeičia pirmą sakinį didžiąja raide, bet nekeičia žodžių po skaičiaus.
def cap_sentence(sentence: str) -> str:
    words =sentence.split()
    if words:
        words[0] = words[0].capitalize()
    return ' '.join(words)

# Formatuoja sakinius: kiekvieno sakinio pradžia didžiąja raide.
def form_sentence(text: str) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    formatted = [cap_sentence(s.strip()) for s in sentences]
    return ' '.join(formatted)

# Abstrakti bazinė klasė teksto apdorojimui.
class TextProcessor(ABC):
    def __init__(self, text: str) -> None:
        self.text: str = text

# Sutvarko teksta pagal taisikles.
    @abstractmethod
    def clean_text(self) -> str:
        pass

# Atlieka pilna anlize ir grazina rezultatus.
    @abstractmethod
    def analyze(self) -> TextAnalyzerStorage:
        pass

# Pagrindine teksto analizes klase, paveldi "TextProcessor".
class TextAnalyzerCore(TextProcessor):
    _instance_count: int = 0

# Inicilizuoja nauja "TextAnalyzerCore"
    def __init__(self, text: str = "") -> None:
        super().__init__(text) 
        TextAnalyzerCore._instance_count += 1
        logging.info("TextAnalyzer instance created.")

# Įgivendina privalomą 'clean_text() metodą.'
    def clean_text(self) -> str:
        return self.fixed_text
# Atnaujina tekstą.

    def update_text(self, new_text: str) -> None:
        self.text = new_text
        logging.info("Text update.")

# Išvalo tekstą pagal taisykles.
    @property
    def fixed_text(self) -> str: 
        text_with_commas = re.sub(r',(\S)', r', \1', self.text)
        return form_sentence(text_with_commas)
    
# Grąžina sukurtų 'TextAnaluzerCore' objektų skaičių.
    @staticmethod
    def get_instance_count() -> int:
        return TextAnalyzerCore._instance_count 
    
# Skaičiuoja žodžius tekste.
    def count_words(self) -> int:
        words = re.findall(r'\b[a-zA-Z]+\b', self.text)
        return len(words)
    
# Skaičiuoja sakinius tekste.
    def count_sentences(self) -> int:
        sentences = re.split(r'[.!?]+', self.text)
        sentences = [s for s in sentences if s.strip()]
        return len(sentences)
    
# Skaičiuoja skaičius tekste.
    def count_numbers(self) -> int:
        numbers = re.findall(r'\d+', self.text)
        return len(numbers)
    
# Randa dažniausiai pasikartojantį žodį iš teksto.
    def most_common_word(self) -> str:
        words: List[str] = re.findall(r'\b\w+\b', self.text.lower())  # Pašalina skyrybos ženklus
        if not words:
            return ""  # Jei nėra žodžių, grąžiname tuščią eilutę
        
        word_counts: Dict[str, int] = {}  # Sukuriame žodyną žodžių dažnumui skaičiuoti
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1  # Didiname skaičiavimą

        return max(word_counts, key=lambda word: word_counts[word]) # Grąžiname žodį su didžiausiu pasikartojimų skaičiumi

# Atlieka pilną analizę ir grąžina rezultatus.
    def analyze(self) -> TextAnalyzerStorage:
        analysis = TextAnalyzerStorage(
            users_text=self.text,
            fixed_text=self.fixed_text,
            num_of_words=self.count_words(),
            num_of_sentences=self.count_sentences(),
            count_of_num=self.count_numbers(),
            most_com_word=self.most_common_word()
        )
        return analysis
