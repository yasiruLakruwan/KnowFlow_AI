import re
import unicodedata

class TextCleaner:

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return "  "
        # 1. Nomalize Unicode
        text = unicodedata.normalize("NFKC" ,text)
        # 2. Remove page numbers
        text = re.sub(r"^\s*\d+\s*$","",text,flags=re.MULTILINE)

        # 3. Remove common headers/footers
        text = re.sub(r"Page\s*\d+\s*(of\s*\d+)?", "", text, flags=re.IGNORECASE)
        text = re.sub(r"©.*", "", text)
        text = re.sub(r"Confidential", "", text, flags=re.IGNORECASE)
        text = re.sub(r"Draft", "", text, flags=re.IGNORECASE)

        # 4. Fix hypeneted line breaks: 'exam-\nple' -> example
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

        # 5. Merge broken lines (PDF common issue)
        text = re.sub(r""r"\n(?=[a-z])", " ", text) 

        # 6. Remove multiple newlines (>2)
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

        # 7. Remove leading/trailing spaces
        text = re.sub(r"[ \t]+", " ", text)

        text = text.strip()

        return text

if __name__=="__main__":
    text = TextCleaner.clean_text("""
        So this is recap where we’re talking about in the previous lecture, remember the notation
I defined was that I used this X superscript I, Y superscript I to denote the I training
example. And when we’re talking about linear regression or linear least squares, we use
this to denote the predicted value of “by my hypothesis H” on the input XI. And my
hypothesis was franchised by the vector of grams as theta and so we said that this was
equal to some from theta J, si J, and more theta transpose X. And we had the convention
that X subscript Z is equal to one so this accounts for the intercept term in our linear
regression model. And lowercase n here was the notation I was using for the number of
features in my training set. Okay? So in the example when trying to predict housing
prices, we had two features, the size of the house and the number of bedrooms. We had
two features and there was – little n was equal to two. So just to finish recapping the
previous lecture, we defined this quadratic cos function J of theta equals one-half,
something I equals one to m, theta of XI minus YI squared where this is the sum over our
m training examples and my training set. So lowercase m was the notation I’ve been
using to denote the number of training examples I have and the size of my training set.
And at the end of the last lecture, we derive the value of theta that minimizes this
enclosed form, which was X transpose X inverse X transpose Y. Okay? 
    """)
    print(text)