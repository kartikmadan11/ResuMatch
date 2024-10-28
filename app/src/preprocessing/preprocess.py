import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import spmatrix

# Ensure stopwords are downloaded
nltk.download("stopwords")


class Preprocess:
    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.vectorizer = TfidfVectorizer(stop_words="english")

    def fit_vectorizer(self, corpus: list):
        """Fit the TF-IDF vectorizer on a combined corpus of texts."""
        self.vectorizer.fit(corpus)
        print(
            "Vectorizer fitted with vocabulary size:", len(self.vectorizer.vocabulary_)
        )

    def preprocess(self, text: str) -> spmatrix:
        """Preprocess the extracted text (cleaning, tokenization, etc.)."""
        # Convert text to lowercase
        text = text.lower()

        # Remove stop words
        words = text.split()
        filtered_words = [word for word in words if word not in self.stop_words]
        filtered_text = " ".join(filtered_words)

        # Apply TF-IDF transformation
        tfidf_matrix = self.vectorizer.transform([filtered_text])

        return tfidf_matrix
