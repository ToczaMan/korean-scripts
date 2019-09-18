import random
from gtts import gTTS, gTTSError
from os import remove, close
from pygame import mixer


def set_console():
    import ctypes

    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD),
                    ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint),
                    ("FaceName", ctypes.c_wchar * LF_FACESIZE)]

    font = CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font.nFont = 16
    font.dwFontSize.X = 11
    font.dwFontSize.Y = 18
    font.FontFamily = 54
    font.FontWeight = 400
    font.FaceName = "NSimSun"

    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(
        handle, ctypes.c_long(False), ctypes.pointer(font))


# TODO: English --> Korean translation
def main():
    set_console()
    # Load the dictionary file. A CSV with two columns, one with English words, another with Korean.
    # Not all English words have to be translated to Korean.
    known_dictionary = {}
    words_to_guess = {}
    mistakes = 0
    with open("../res/known_words.txt", encoding="utf-8") as known_words:
        for line in known_words:
            words_in_line = line.split(";")
            if len(words_in_line) > 1:
                english_word = words_in_line[0].strip()
                korean_word = words_in_line[1].strip()
                known_dictionary[english_word.lower()] = words_to_guess[english_word.lower()] = korean_word
    saved_voice_num = 1
    mixer.init()
    while words_to_guess:
        saved_voice_num ^= 1
        saved_voice_name = "voice{}.mp3".format(saved_voice_num)
        # Pick a random Korean word from the list.
        drawn_english_word, drawn_korean_word = random.choice(list(words_to_guess.items()))
        # Print the word and ask the user for input - need to answer in English.
        tts = gTTS(text=drawn_korean_word, lang="ko")
        try:
            tts.save(saved_voice_name)
        except gTTSError:
            print("Error loading voice from Google TTS.")
            saved_voice_num ^= 1
        except PermissionError:
            pass
        else:
            mixer.music.load(saved_voice_name)
            mixer.music.play()
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
