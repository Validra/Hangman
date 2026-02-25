import math
import random
from collections import deque

def log_call(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

class Renderer:
    def render(self, wrong, max_attempts):
        raise NotImplementedError

class AsciiRenderer(Renderer):
    STAGES = (
        " +---+\n     |\n     |\n     |\n    ===",
        " +---+\n O   |\n     |\n     |\n    ===",
        " +---+\n O   |\n |   |\n     |\n    ===",
        " +---+\n O   |\n/|   |\n     |\n    ===",
        " +---+\n O   |\n/|\\  |\n     |\n    ===",
        " +---+\n O   |\n/|\\  |\n/    |\n    ===",
        " +---+\n O   |\n/|\\  |\n/ \\  |\n    ===",
    )

    def render(self, wrong, max_attempts):
        if max_attempts <= 0:
            idx = 0
        else:
            ratio = wrong / max_attempts
            idx = int(math.floor(ratio * (len(self.STAGES) - 1)))
            idx = max(0, min(idx, len(self.STAGES) - 1))
        return self.STAGES[idx]


class TextRenderer(Renderer):
    def render(self, wrong, max_attempts):
        return f"Wrong tries: {wrong}/{max_attempts}"

class HangmanState:
    def __init__(self, word, max_attempts):
        self.word = word
        self.max_attempts = max_attempts
        self.guessed = set()
        self.wrong = []
        self.last_inputs = deque(maxlen=10)

    def masked_word(self):
        return " ".join(ch if ch in self.guessed else "_" for ch in self.word)

    def wrong_count(self):
        return len(self.wrong)

    def remaining(self):
        return self.max_attempts - self.wrong_count()

    def is_won(self):
        return set(self.word) <= self.guessed

    def is_lost(self):
        return self.wrong_count() >= self.max_attempts

    def hint_letter(self):
        candidates = [c for c in set(self.word) if c not in self.guessed]
        if not candidates:
            return None
        return random.choice(candidates)

    @log_call
    def guess(self, user_input):
        text = user_input.strip().lower()

        if len(text) != 1 or not text.isalpha():
            return {"ok": False, "message": "Type ONE letter."}

        if text in self.guessed or text in self.wrong:
            return {"ok": False, "message": "You already used this letter."}

        self.last_inputs.append(text)

        if text in self.word:
            self.guessed.add(text)
            return {"ok": True, "hit": True, "message": "Good!"}
        else:
            self.wrong.append(text)
            return {"ok": True, "hit": False, "message": "Wrong!"}

class WordProvider:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_words(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f"Missing file: {self.file_path}")

        words = []
        with self.file_path.open("r", encoding="utf-8") as f:
            for line in f:
                w = line.strip().lower()
                if not w:
                    continue
                w = "".join(ch for ch in w if ch.isalpha())
                if w:
                    words.append(w)

        if not words:
            raise ValueError("No valid words in words.txt")

        return words

    def random_word(self):
        return random.choice(self.load_words())

class ScoreBoard:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_result(self, record):
        line = (
            f"word={record['word']}; "
            f"won={record['won']}; "
            f"wrong={record['wrong']}; "
            f"max={record['max_attempts']}; "
            f"score={record['score']}\n"
        )
        with self.file_path.open("a", encoding="utf-8") as f:
            f.write(line)

def compute_score(state):
    base = 100
    penalty = state.wrong_count() * 10
    bonus = int(math.ceil(math.sqrt(max(0, state.remaining())) * 10))
    return max(0, base - penalty + bonus)

class HangmanGame:
    def __init__(self, words_file, scoreboard_file, max_attempts, renderer):
        self.provider = WordProvider(words_file)
        self.board = ScoreBoard(scoreboard_file)
        self.max_attempts = max_attempts
        self.renderer = renderer

    def new_state(self):
        return HangmanState(self.provider.random_word(), self.max_attempts)

    def save(self, state):
        record = {
            "word": state.word,
            "won": state.is_won(),
            "wrong": state.wrong_count(),
            "max_attempts": state.max_attempts,
            "score": compute_score(state) if state.is_won() else 0,
        }
        self.board.save_result(record)
