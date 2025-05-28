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

# Data class for storing text.
@dataclass
class TextAnalyzerStorage:
    users_text: str
    fixed_text: str
    num_of_words: int
    num_of_sentences: int
    count_of_num: int
    most_com_word: str

# Capitalizes the first sentence but does not change words after a number.
def cap_sentence(sentence: str) -> str:
    words =sentence.split()
    if words:
        words[0] = words[0].capitalize()
    return ' '.join(words)

# Formats sentences: each sentence starts with a capital letter.
def form_sentence(text: str) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    formatted = [cap_sentence(s.strip()) for s in sentences]
    return ' '.join(formatted)

# Abstract base class for text processing.
class TextProcessor(ABC):
    def __init__(self, text: str) -> None:
        self.text: str = text

# Cleans text according to rules.
    @abstractmethod
    def clean_text(self) -> str:
        pass

# Performs full analysis and returns results.
    @abstractmethod
    def analyze(self) -> TextAnalyzerStorage:
        pass

# Main text analysis class, inherits from "TextProcessor".
class TextAnalyzerCore(TextProcessor):
    _instance_count: int = 0

# Initializes a new "TextAnalyzerCore".
    def __init__(self, text: str = "") -> None:
        super().__init__(text) 
        TextAnalyzerCore._instance_count += 1
        logging.info("TextAnalyzer instance created.")

# Returns the textual representation of the object.
    def __repr__(self) -> str:
        return f"TextAnalyzerCore(text='{self.text[:30]}...', words={self.count_words()}, sentences={self.count_sentences()})"
    
# Returns the total word count in the text.
    def __len__(self) -> int:
        return self.count_words()
    
# Implements the required 'clean_text()' method.
    def clean_text(self) -> str:
        return self.fixed_text
    
# Updates the text.
    def update_text(self, new_text: str) -> None:
        self.text = new_text
        logging.info("Text update.")

# Cleans the text according to rules.
    @property
    def fixed_text(self) -> str: 
        text_with_commas = re.sub(r',(\S)', r', \1', self.text) 
        return form_sentence(text_with_commas)
    
# Returns the number of 'TextAnalyzerCore' instances created.
    @staticmethod
    def get_instance_count() -> int:
        return TextAnalyzerCore._instance_count 
    
# Counts words in the text.
    def count_words(self) -> int:
        words = re.findall(r'\b[a-zA-Z]+\b', self.text)
        return len(words)
    
# Counts sentences in the text.
    def count_sentences(self) -> int:
        sentences = re.split(r'[.!?]+', self.text)
        sentences = [s for s in sentences if s.strip()]
        return len(sentences)
    
# Counts numbers in the text.
    def count_numbers(self) -> int:
        numbers = re.findall(r'\d+', self.text)
        return len(numbers)
    
# Finds the most common word(s) in the text.
    def most_common_word(self) -> str:
        words: List[str] = re.findall(r'\b\w+\b', self.text.lower())  # Removes punctuation
        word_counts: Dict[str, int] = {}  # Create a dictionary to count word frequencies
        
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1  # Increase the count

        max_count = max(word_counts.values()) # Find the maximum number of occurrences
        most_common_words = [word for word, count in word_counts.items() if count == max_count] # Select all equivalent
        
        return ", ".join(most_common_words) # Return all words with the same count

# Performs a full analysis and returns results.
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
