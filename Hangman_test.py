from hangman import HangmanState, compute_score

def test_masked_word_start():
    state = HangmanState("python", 6)
    assert state.masked_word() == "_ _ _ _ _ _"

def test_guess_good_letter():
    state = HangmanState("python", 6)
    result = state.guess("p")
    assert result["ok"] is True
    assert result["hit"] is True
    assert state.masked_word().startswith("p")

def test_guess_wrong_letter():
    state = HangmanState("python", 6)
    result = state.guess("z")
    assert result["ok"] is True
    assert result["hit"] is False
    assert state.wrong_count() == 1

def test_guess_validation_not_one_letter():
    state = HangmanState("python", 6)
    result = state.guess("ab")
    assert result["ok"] is False

def test_guess_validation_not_letter():
    state = HangmanState("python", 6)
    result = state.guess("1")
    assert result["ok"] is False

def test_repeated_letter():
    state = HangmanState("python", 6)
    state.guess("p")
    result = state.guess("p")
    assert result["ok"] is False

def test_win_condition():
    state = HangmanState("aa", 6)
    state.guess("a")
    assert state.is_won() is True

def test_lose_condition():
    state = HangmanState("a", 2)
    state.guess("x")
    state.guess("y")
    assert state.is_lost() is True

def test_score_non_negative():
    state = HangmanState("aa", 6)  #
    state.guess("a")
    score = compute_score(state)
    assert score >= 0
