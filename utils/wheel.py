
import random

class WheelLogic:
    suggestions = []

    @classmethod
    def add_suggestion(cls, text):
        cls.suggestions.append(text)

    @classmethod
    def set_suggestions(cls, data):
        cls.suggestions = data

    @classmethod
    def get_suggestions(cls):
        return cls.suggestions

    @classmethod
    def clear(cls):
        cls.suggestions = []

    @classmethod
    def pick(cls):
        if not cls.suggestions:
            return None, None
        index = random.randint(0, len(cls.suggestions) - 1)
        return cls.suggestions[index], index
