import json
from prompt_analyzer import TextAnalyzerCore
from logger import logger


class TextAnalyzerApp:
    def __init__(self) -> None:
        self.analyzer = None

# Enter new text and create an analysis object.
    def enter_text(self, text: str)  -> None:
            if len(text) < 15:
                raise ValueError("Text is too short. Please provide at least 5 sentences.")
            self.analyzer = TextAnalyzerCore(text)
            logger.info("Text entered successfully.")
            

# Returns the analysis report in JSON.
    def get_report(self) -> dict[str, str | int]:
        if self.analyzer is None:
            logger.warning("Attempted to generate report with no text entered.")
            return {"error": "No text available. Please enter text first."}
        
        return {
            "fixed_text": self.analyzer.fixed_text,
            "number_of_words": self.analyzer.count_words(),
            "number_of_sentences": self.analyzer.count_sentences(),
            "count_of_numbers": self.analyzer.count_numbers(),
            "most_common_word/words": self.analyzer.most_common_word()
        }

# Shows the number of words.
    def show_num_of_words(self) -> int | str:
            if self.analyzer is None:
                logger.warning("Attempted to get word count with no text entered.")
                return "No text available. Please enter text first."
            return self.analyzer.count_words()

# Shows the number of sentences in the text.
    def show_num_of_sentences(self) -> int | str:
            if self.analyzer is None:
                logger.warning("Attempted to get sentence count with no text entered.")
                return "No text available. Please enter text first."
            return self.analyzer.count_sentences()

# Shows the count of numbers in the text.
    def show_count_of_num(self) -> int | str:
        if self.analyzer is None:
            logger.warning("Attempted to get sentence count with no text entered.")
            return "No text available. Please enter text first."
        return self.analyzer.count_numbers()
         
# Shows the most common word(s).   
    def show_most_common_words(self) -> str | list[str]:
            if self.analyzer is None:
                logger.warning("Attempted to get most common word(s) with no text entered.")
                return "No text available. Please enter text first."
            return self.analyzer.most_common_word()
