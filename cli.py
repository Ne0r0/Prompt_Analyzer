import json
from main import TextAnalyzerApp
from logger import logger


def cli_menu() -> None:
    app: TextAnalyzerApp = TextAnalyzerApp()
    logger.info("CLI application started")
    
    while True:
        print("\n===== Prompt Text Analyzer =====")
        print("1. Enter new text")
        print("2. Get Report")
        print("3. Show number of words")
        print("4. Show number of sentences")
        print("5. Show count of numbers")
        print("6. Show most common word or words")
        print("0. Exit")
        
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                text = input("Enter your text (At least 5 sentences): ").strip()
                app.enter_text(text)
                logger.info("User entered text successfully.")
                print("Text entered successfully!")

            elif choice == "2":
                report = app.get_report()
                logger.info("Report generated succesfully.")
                print(json.dumps(report, indent=4))

            elif choice == "3":
                if app.analyzer:
                    logger.info("Word count displayed.")
                    print(f"Total words: {app.analyzer.count_words()}")
                else:
                    logger.warning("Attempted to get word count without text.")
                    print("No text available. Please enter text first.")

            elif choice == "4":
                if app.analyzer:
                    logger.info("Sentence count displayed.")
                    print(f"Total sentences: {app.analyzer.count_sentences()}")
                else:
                    logger.warning("Attempted to get sentence count without text.")
                    print("No text available. Please enter text first.")

            elif choice == "5":
                if app.analyzer:
                    logger.info("Number count displayed.")
                    print(f"Count of numbers: {app.analyzer.count_numbers()}")
                else:
                    logger.warning("Attempted to get number count without text.")
                    print("No text available. Please enter text first.")

            elif choice == "6":
                if app.analyzer:
                    logger.info("Most common word displayed.")
                    print(f"Most common word(s): {app.analyzer.most_common_word()}")
                else:
                    logger.warning("Attempted to get most common word without text.")
                    print("No text available. Please enter text first.")

            elif choice == "0":
                logger.info("User exited the application.")
                print("See you later 👋👋")
                break

            else:
                logger.error(f"Invalid menu choice: {choice}")
                print("Invalid input. Please try again.")
            
        except Exception as e:
            logger.critical(f"Error: {e}")
            print(f"Error: {e}")

if __name__ == "__main__":
    cli_menu()