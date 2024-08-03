import json
from difflib import get_close_matches


def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data
# Function to load the knowledge base from a JSON file


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
# Function to save the knowledge base to a JSON file


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(
        user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None
# Function to find the best match for a user's question using fuzzy matching


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
# Function to get the answer for a matched question from the knowledge base


def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    # Load the knowledge base from a JSON file

    user_name = input("Hello there! Please input username or 'quit' to exit: ")
    print(
        f"Thank you, {user_name}, my name is Chathy! How may I assist?")
    # Prompt user for their name & greet them

    while True:
        user_input: str = input('User: ')
        # Get user input

        if user_input.lower() == 'quit':
            break
        # Exit the loop if the user types 'quit'

        best_match: str | None = find_best_match(
            user_input,
            [q["question"] for q in knowledge_base["questions"]])
        # Find the best matching question from the knowledge base

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            answer = answer.replace('your name', user_name)
            print(f'Bot: {answer}')
            # Provide the answer for the matched question
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')
            # Inform user that bot doesn’t know answer & ask for help

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append(
                    {"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')
                # Add new question-answer pair to knowledge base & save it


# Entry point of the program
if __name__ == '__main__':
    chat_bot()
