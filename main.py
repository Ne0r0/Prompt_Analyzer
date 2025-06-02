import logging
import json
from prompt_analyzer import TextAnalyzerCore

logging.basicConfig(
    level=logging.INFO,
    filename="logs/app.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)
class TextAnalyzerApp:
    def __init__(self) -> None:
        self.analyzer = None

# Enter new text and create an analysis object.
    def enter_text(self)  -> None:
        try:
            text_input: str = input("Enter your text (At least 5 sentences): ").strip()
            if len(text_input) < 15:
                raise ValueError("Text is to short. Please provide at least 5 sentences.")
            self.analyzer = TextAnalyzerCore(text_input)
            print("Text entered successfully!")
        except ValueError as e:
            logging.error(f"Text input error: {e}")
            print(f"Error: {e}")

# Returns the analysis report in JSON.
    def show_report(self) -> None:
        if self.analyzer is None:
            logging.warning("Attempted to generate report with no text entered.")
            print("No text available. Please enter text first")
            return
        
        report_data: dict[str, str | int] = {
            "fixed_text": self.analyzer.fixed_text,
            "number_of_words": self.analyzer.count_words(),
            "number_of_sentences": self.analyzer.count_sentences(),
            "count_of_numbers": self.analyzer.count_numbers(),
            "most_common_word/words": self.analyzer.most_common_word()
        }
        print(json.dumps(report_data, indent=4))
        logging.info("Report generated successfully.")

# Shows the number of words.
    def show_num_of_words(self) -> None:
        try:
            if self.analyzer is None:
                raise RuntimeError("No text available. Please enter text first.")
            print(f"Total words: {self.analyzer.count_words()}")
        except RuntimeError as e:
            logging.error(f"Word count error: {e}")
            print(f"Error: {e}")

# Shows the number of sentences in the text.
    def show_num_of_sentences(self) -> None:
        try:
            if self.analyzer is None:
                raise RuntimeError("No text available. Please enter text first.")
            print(f"Total sentences: {self.analyzer.count_sentences()}")
        except RuntimeError as e:
            logging.error(f"Sentence count error: {e}")
            print(f"Error: {e}")

# Shows the count of numbers in the text.
    def show_count_of_num(self) -> None:
        try:
            if self.analyzer is None:
                raise RuntimeError("No text available. Please enter text first.")
            print(f"Count of numbers: {self.analyzer.count_numbers()}")
        except RuntimeError as e:
            logging.error(f"Number count error: {e}")
            print(f"Error: {e}")

# Shows the most common word(s).   
    def show_most_common_words(self) -> None:
        try:
            if self.analyzer is None:
                raise RuntimeError("No text available. Please enter text first.")
            print(f"Most common word(s): {self.analyzer.most_common_word()}")
        except RuntimeError as e:
            logging.error(f"Most common word error: {e}")
            print(f"Error: {e}")

# CLI application.
def main() -> None:
    app: TextAnalyzerApp = TextAnalyzerApp()

    while True:
        print("\n===== Prompt Text Analyzer =====")
        print("1. Enter new text (minimum 5 sentences)")
        print("2. Get Report")
        print("3. Show number of words")
        print("4. Show number of sentences")
        print("5. Show count of numbers")
        print("6. Show most common word or words")
        print("0. Exit")
        
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                app.enter_text()
            elif choice == "2":
                app.show_report()
            elif choice == "3":
                app.show_num_of_words()
            elif choice == "4":
                app.show_num_of_sentences()
            elif choice == "5":
                app.show_count_of_num()
            elif choice == "6":
                app.show_most_common_words()
            elif choice == "0":
                logging.info("User exited the application.")
                print("See you later 👋👋")
                break
            else:
                raise ValueError("Invalid input. Please try again.")
        except ValueError as e:
            logging.error(f"Invalid menu choise: {e}")
            print(f"Invalid menu choise: {e}")
        except Exception as e:
            logging.critical(f"Error: {e}")
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
