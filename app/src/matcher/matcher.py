from sklearn.metrics.pairwise import cosine_similarity


class Matcher:
    def __init__(self) -> None:
        pass

    def compute_similarity(self, jd_vector: list, resume_vector: list) -> float:
        similarity = cosine_similarity(jd_vector, resume_vector)
        return similarity[0][0]
