"""
SaiKet Systems Internship Task 3
Basic File Handling
-------------------------------------------
Features:
  - Read data from a text file
  - Find and replace specific words/phrases
  - Save the modified content back to the file
  - Robust error handling for file-related exceptions
"""
import re
from pathlib import Path


def read_text_file(file_path):
    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied while reading '{file_path}'.")
    except IsADirectoryError:
        print(f"Error: '{file_path}' is a directory, not a text file.")
    except OSError as error:
        print(f"Error: Could not read '{file_path}'. Details: {error}")

    return None


def save_text_file(file_path, content):
    try:
        file_path.write_text(content, encoding="utf-8")
        return True
    except PermissionError:
        print(f"Error: Permission denied while writing to '{file_path}'.")
    except IsADirectoryError:
        print(f"Error: '{file_path}' is a directory, not a text file.")
    except OSError as error:
        print(f"Error: Could not save '{file_path}'. Details: {error}")

    return False


def replace_text(content, old_text, new_text):
    if old_text == "":
        raise ValueError("The text to replace cannot be empty.")

    pattern = re.compile(re.escape(old_text), re.IGNORECASE)
    return pattern.sub(new_text, content)


def count_text(content, text_to_find):
    pattern = re.compile(re.escape(text_to_find), re.IGNORECASE)
    return len(pattern.findall(content))


def show_menu():
    print("\nOptions:")
    print("  1. Find text")
    print("  2. Find and replace text")
    print("  3. Display current file")
    print("  4. Save and exit")
    print("  5. Exit without saving")


def find_text(content):
    text_to_find = input("Enter the word/phrase to find: ")

    if text_to_find == "":
        print("Error: Search text cannot be empty.")
        return

    count = count_text(content, text_to_find)
    if count == 0:
        print("Text not found.")
    else:
        print(f"Found {count} occurrence(s).")


def find_and_replace_text(content):
    old_text = input("Enter the word/phrase to find: ")
    new_text = input("Enter the replacement word/phrase: ")

    try:
        modified_content = replace_text(content, old_text, new_text)
    except ValueError as error:
        print(f"Error: {error}")
        return content

    replacements = count_text(content, old_text)
    if replacements == 0:
        print("No matching word/phrase was found.")
        return content

    print(f"Replaced {replacements} occurrence(s).")
    return modified_content


def display_current_file(content):
    print("\nCurrent file content:")
    print("---------------------")
    print(content)
    print("---------------------")


def main():
    print("Basic File Handling - Find and Replace")
    print("----------------------------------------")

    file_name = input("Enter the text file path: ").strip()
    file_path = Path(file_name)

    current_content = read_text_file(file_path)
    if current_content is None:
        return

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            find_text(current_content)
        elif choice == "2":
            current_content = find_and_replace_text(current_content)
        elif choice == "3":
            display_current_file(current_content)
        elif choice == "4":
            if save_text_file(file_path, current_content):
                print("File saved successfully.")
                print(f"Updated file: {file_path}")
                break
        elif choice == "5":
            print("Exited without saving changes.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
