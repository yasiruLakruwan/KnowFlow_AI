import re
import unicodedata

class TextCleaner:

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return "  "
        