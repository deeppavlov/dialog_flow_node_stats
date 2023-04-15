# %%
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import typing
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

class DialogModel:
    def __init__(self, n_clusters = 10, text_embedder: typing.Optional[TfidfVectorizer] = None):
        self.n_clusters = n_clusters
        self.text_embedder = text_embedder
        self.replica_df = None
        
    def fit(self, replicas: list[str]):
        self.replica_df = pd.DataFrame(replicas, columns=['replica'])

        if self.text_embedder is None:
            self.text_embedder = TfidfVectorizer()
            self.text_embedder.fit(self.replica_df['replica'])

        # Cluster user and bot replicas separately
        replica_X = self.text_embedder.transform(self.replica_df['replica'])
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        kmeans.fit(replica_X)
        self.replica_df["cluster_label"] = kmeans.labels_
        self.cluster_centers = kmeans.cluster_centers_

        # Build Markov model
        self.markov_model = np.zeros((self.n_clusters, self.n_clusters))
        for start, end in zip(kmeans.labels_[1:],kmeans.labels_):
            self.markov_model[start, end] += 1
        

    def replica2cluster(self, replica):
        # Embed the input replica using the specified embedder
        replica_embedding = self.text_embedder.transform([replica]).toarray()
        
        # Calculate the distance between the replica embedding and each cluster center
        distances = np.linalg.norm(replica_embedding - self.cluster_centers, axis=1)
        
        # Find the index of the closest cluster
        closest_cluster = np.argmin(distances)
        
        # Retrieve the corresponding cluster label and response options
        # cluster = self.cluster_labels[closest_cluster]
        
        return closest_cluster

    def predict_next_cluster(self, replica):
        cluster = self.replica2cluster(replica)
        next_cluster = np.argmax(self.markov_model[cluster])
        return next_cluster

    def predict_responses(self, replica):
        next_cluster = self.predict_next_cluster(replica)
        predicted_responses = self.replica_df[self.replica_df["cluster_label"] == next_cluster]
        return predicted_responses
