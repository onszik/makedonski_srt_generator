from spellchecker import SpellChecker # type: ignore

def correct_text(text):
    spell = SpellChecker(language=None)

    with open("mk_full.txt", "r", encoding="utf-8") as f:
        macedonian_words = {line.strip().lower() for line in f}

    spell.word_frequency.load_words(macedonian_words)

    words = text.split()
    corrected_words = []
    for word in words:
        if word.lower() not in spell:
            corrected_word = spell.correction(word.lower())
            corrected_words.append(corrected_word if corrected_word else word)
        else:
            corrected_words.append(word)
    return " ".join(corrected_words)

# Example usage
# with open("text.txt", 'r', encoding='utf-8') as file:
#         lines = file.readlines()

# for line in lines:
#     corrected_text = correct_text(line)
#     print(corrected_text)

