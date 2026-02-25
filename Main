from pathlib import Path
from hangman import AsciiRenderer, TextRenderer, HangmanGame

def choose_renderer():
    print("Choose display mode:")
    print("1) Pictorial hangman")
    print("2) Text hangman")

    choice = input("You can choose 1 or 2: ").strip()

    if choice == "2":
        return TextRenderer()
    else:
        return AsciiRenderer()

def main():
    renderer = choose_renderer()

    game = HangmanGame(
        words_file=Path("words.txt"),
        scoreboard_file=Path("scoreboard.txt"),
        max_attempts=6,
        renderer=renderer,
    )

    state = game.new_state()

    print("\n=== Hangman Game ===")
    print("Commands: hint, quit\n")

    while True:
        print(game.renderer.render(state.wrong_count(), state.max_attempts))
        print("Word:", state.masked_word())
        print("Wrong letters:", ", ".join(state.wrong) if state.wrong else "(none)")
        print("Remaining tries:", state.remaining())
        print()

        if state.is_won():
            print("You win! B)")
            break

        if state.is_lost():
            print("You lose :( , Word was:", state.word)
            break

        user_input = input("Type a letter or command: ").strip().lower()

        if user_input == "quit":
            print("Bye!")
            break

        if user_input == "hint":
            h = state.hint_letter()
            if h:
                print("Hint letter:", h)
            else:
                print("No hint available.")
            continue

        result = state.guess(user_input)

        if not result["ok"]:
            print(result["message"])
            continue

        print(result["message"])

    game.save(state)
    print("Result saved to scoreboard.txt")

if __name__ == "__main__":
    main()
