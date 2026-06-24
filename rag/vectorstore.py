import faiss
import numpy as np
import pickle
import os

# all-MiniLM-L6-v2 embedding dimension
DIM = 384


class FAISSStore:

    def __init__(self, path="faiss.index"):

        self.path = path

        self.index = faiss.IndexFlatL2(DIM)

        self.texts = []
        self.metadata = []

        if (
            os.path.exists(path)
            and
            os.path.exists(path + ".pkl")
        ):
            self.load()

    def add(
        self,
        embedding,
        text,
        meta=None
    ):

        embedding = np.array(
            [embedding],
            dtype=np.float32
        )

        self.index.add(
            embedding
        )

        self.texts.append(
            text
        )

        self.metadata.append(
            meta or {}
        )

    def search(
        self,
        query_embedding,
        k=5
    ):

        if self.index.ntotal == 0:
            return []

        query_embedding = np.array(
            [query_embedding],
            dtype=np.float32
        )

        distances, indices = self.index.search(
            query_embedding,
            min(k, self.index.ntotal)
        )

        results = []

        for idx in indices[0]:

            if idx < len(self.texts):

                results.append(
                    {
                        "id": idx,
                        "text": self.texts[idx],
                        "meta": self.metadata[idx]
                    }
                )

        return results

    def save(self):

        faiss.write_index(
            self.index,
            self.path
        )

        with open(
            self.path + ".pkl",
            "wb"
        ) as f:

            pickle.dump(
                (
                    self.texts,
                    self.metadata
                ),
                f
            )

    def load(self):

        self.index = faiss.read_index(
            self.path
        )

        with open(
            self.path + ".pkl",
            "rb"
        ) as f:

            self.texts, self.metadata = pickle.load(
                f
            )


# ---------------------------------
# Global store instance
# ---------------------------------

store = FAISSStore()


# ---------------------------------
# Functions used by app.py
# ---------------------------------

def add_document(
    text,
    embedding
):

    store.add(
        embedding,
        text
    )

    store.save()


def search(
    embedding,
    k=5
):

    return store.search(
        embedding,
        k
    )