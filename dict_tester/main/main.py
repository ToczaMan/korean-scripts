import random


# TODO: English --> Korean translation
def main():
    # Load the dictionary file. A CSV with two columns, one with English words, another with Korean.
    # Not all English words have to be translated to Korean.
    known_dictionary = {}
    words_to_guess = {}
    mistakes = 0
    with open("../res/all_words.txt", encoding="utf-8") as all_words, \
            open("../res/known_words.txt", encoding="utf-8", mode="w") as known_words_reference:
        for line in all_words:
            words_in_line = line.split(";")
            if len(words_in_line) > 1:
                english_word = words_in_line[0].strip()
                korean_word = words_in_line[1].strip()
                known_dictionary[english_word.lower()] = words_to_guess[english_word.lower()] = korean_word
                known_words_reference.write("{english_word} - {korean_word}\r\n"
                                            .format(english_word=english_word, korean_word=korean_word))
    while words_to_guess:
        # Pick a random Korean word from the list.
        drawn_english_word, drawn_korean_word = random.choice(list(words_to_guess.items()))
        # Print the word and ask the user for input - need to answer in English.
        translation = input("{korean_word}(은/는) 영어로 무엇입니까? (type \"@end\" to end) "
                            .format(korean_word=drawn_korean_word))
        if translation == "@end":
            break
        # TODO: Synonyms in one line
        elif known_dictionary.get(translation.lower()) == drawn_korean_word:
            print("CORRECT. 잘했습니다!")
            words_to_guess.pop(drawn_english_word)
        else:
            print("INCORRECT...")
            print("{korean_word}: {english_word}".format(korean_word=drawn_korean_word, english_word=drawn_english_word))
            mistakes += 1
        print("Words left: {}".format(len(words_to_guess)))
    print("GAME OVER... MISTAKES: {mistakes}".format(mistakes=mistakes))


if __name__ == "__main__":
    main()
