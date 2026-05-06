import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
    "has", "have", "he", "her", "his", "i", "in", "is", "it", "its", "of",
    "on", "or", "our", "she", "that", "the", "their", "them", "they", "this",
    "to", "was", "we", "were", "with", "you", "your",
}

WORD_PATTERN = re.compile(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)?")
SENTENCE_PATTERN = re.compile(r"[^.!?]+[.!?]+|[^.!?]+$")
VOWEL_GROUP_PATTERN = re.compile(r"[aeiouy]+", re.IGNORECASE)


def read_input(file_path):
    if file_path:
        try:
            return Path(file_path).read_text(encoding="utf-8"), str(file_path)
        except FileNotFoundError:
            raise SystemExit(f"Error: File not found: {file_path}")
        except PermissionError:
            raise SystemExit(f"Error: Permission denied: {file_path}")
        except IsADirectoryError:
            raise SystemExit(f"Error: Expected a text file, got a directory: {file_path}")
        except UnicodeDecodeError:
            raise SystemExit(f"Error: File is not valid UTF-8: {file_path}")
        except OSError as error:
            raise SystemExit(f"Error: Could not read file. Details: {error}")

    if sys.stdin.isatty():
        entered_path = input("Enter UTF-8 text file path: ").strip().strip('"')
        if not entered_path:
            raise SystemExit("Error: No file path provided.")
        return read_input(entered_path)

    return sys.stdin.read(), "stdin"


def get_words(text):
    return WORD_PATTERN.findall(text)


def count_sentences(text):
    sentences = [item.strip() for item in SENTENCE_PATTERN.findall(text)]
    return len([sentence for sentence in sentences if sentence])


def count_paragraphs(text):
    paragraphs = re.split(r"\n\s*\n", text.strip())
    return len([paragraph for paragraph in paragraphs if paragraph.strip()])


def estimate_syllables(word):
    cleaned = re.sub(r"[^a-z]", "", word.lower())
    if not cleaned:
        return 0

    groups = VOWEL_GROUP_PATTERN.findall(cleaned)
    count = len(groups)

    if cleaned.endswith("e") and count > 1:
        count -= 1

    return max(count, 1)


def flesch_reading_ease(words, sentence_count):
    word_count = len(words)
    if word_count == 0 or sentence_count == 0:
        return None

    syllable_count = sum(estimate_syllables(word) for word in words)
    return 206.835 - (1.015 * (word_count / sentence_count)) - (
        84.6 * (syllable_count / word_count)
    )


def flesch_kincaid_grade(words, sentence_count):
    word_count = len(words)
    if word_count == 0 or sentence_count == 0:
        return None

    syllable_count = sum(estimate_syllables(word) for word in words)
    return (0.39 * (word_count / sentence_count)) + (
        11.8 * (syllable_count / word_count)
    ) - 15.59


def frequency_analysis(words, include_stop_words, limit):
    normalized_words = [word.lower() for word in words]
    if not include_stop_words:
        normalized_words = [
            word for word in normalized_words if word not in STOP_WORDS
        ]

    return Counter(normalized_words).most_common(limit)


def analyze_text(text, source, include_stop_words, limit):
    words = get_words(text)
    lines = text.splitlines()
    sentence_count = count_sentences(text)

    return {
        "source": source,
        "words": len(words),
        "lines": len(lines),
        "characters": len(text),
        "characters_no_spaces": len(re.sub(r"\s", "", text)),
        "sentences": sentence_count,
        "paragraphs": count_paragraphs(text),
        "readability": {
            "flesch_reading_ease": flesch_reading_ease(words, sentence_count),
            "flesch_kincaid_grade": flesch_kincaid_grade(words, sentence_count),
        },
        "top_words": frequency_analysis(words, include_stop_words, limit),
        "stop_words_filtered": not include_stop_words,
    }


def format_score(score):
    if score is None:
        return "N/A"
    return f"{score:.2f}"


def print_report(analysis):
    print("\nWord Count Tool Report")
    print("=" * 44)
    print(f"Source: {analysis['source']}")
    print(f"Words: {analysis['words']}")
    print(f"Lines: {analysis['lines']}")
    print(f"Characters: {analysis['characters']}")
    print(f"Characters without spaces: {analysis['characters_no_spaces']}")
    print(f"Sentences: {analysis['sentences']}")
    print(f"Paragraphs: {analysis['paragraphs']}")
    print("-" * 44)
    print("Readability")
    print(
        "Flesch Reading Ease: "
        f"{format_score(analysis['readability']['flesch_reading_ease'])}"
    )
    print(
        "Flesch-Kincaid Grade: "
        f"{format_score(analysis['readability']['flesch_kincaid_grade'])}"
    )
    print("-" * 44)
    print("Top Words")

    if not analysis["top_words"]:
        print("No words found.")
        return

    for word, count in analysis["top_words"]:
        print(f"{word:<20} {count}")


def export_json(analysis, output_path):
    try:
        Path(output_path).write_text(
            json.dumps(analysis, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except OSError as error:
        raise SystemExit(f"Error: Could not write JSON export. Details: {error}")


def export_csv(analysis, output_path):
    try:
        with Path(output_path).open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["metric", "value"])
            writer.writerow(["source", analysis["source"]])
            writer.writerow(["words", analysis["words"]])
            writer.writerow(["lines", analysis["lines"]])
            writer.writerow(["characters", analysis["characters"]])
            writer.writerow(["characters_no_spaces", analysis["characters_no_spaces"]])
            writer.writerow(["sentences", analysis["sentences"]])
            writer.writerow(["paragraphs", analysis["paragraphs"]])
            writer.writerow([
                "flesch_reading_ease",
                format_score(analysis["readability"]["flesch_reading_ease"]),
            ])
            writer.writerow([
                "flesch_kincaid_grade",
                format_score(analysis["readability"]["flesch_kincaid_grade"]),
            ])
            writer.writerow([])
            writer.writerow(["word", "frequency"])
            writer.writerows(analysis["top_words"])
    except OSError as error:
        raise SystemExit(f"Error: Could not write CSV export. Details: {error}")


def build_parser():
    parser = argparse.ArgumentParser(
        description="Expert-level word count and text analysis tool."
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="UTF-8 text file to analyze. Omit when piping stdin.",
    )
    parser.add_argument(
        "--include-stop-words",
        action="store_true",
        help="Include common stop words in frequency analysis.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of frequent words to show. Default: 10.",
    )
    parser.add_argument("--json", help="Export analysis to a JSON file.")
    parser.add_argument("--csv", help="Export analysis to a CSV file.")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.top <= 0:
        raise SystemExit("Error: --top must be greater than zero.")

    text, source = read_input(args.file)
    analysis = analyze_text(text, source, args.include_stop_words, args.top)

    print_report(analysis)

    if args.json:
        export_json(analysis, args.json)
        print(f"\nJSON export saved to: {args.json}")

    if args.csv:
        export_csv(analysis, args.csv)
        print(f"CSV export saved to: {args.csv}")


if __name__ == "__main__":
    main()
