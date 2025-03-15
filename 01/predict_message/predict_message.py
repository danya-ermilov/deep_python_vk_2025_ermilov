class SomeModel:
    def predict(self, message: str) -> float:
        letter_count = 0

        letter_count = sum(1 for char in message if char.isalpha())

        return letter_count / len(message)


def predict_message_mood(
    message: str,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    model = SomeModel()

    result = model.predict(message)

    if result >= good_thresholds:
        return "отл"
    elif good_thresholds > result >= bad_thresholds:
        return "норм"
    else:
        return "неуд"

if __name__ == "__main__":
    assert predict_message_mood("Чапаев и пустота") == "отл"
    assert predict_message_mood("ф ф", 0.5, 0.9) == "норм"
    assert predict_message_mood("Вулкан______________________") == "неуд"