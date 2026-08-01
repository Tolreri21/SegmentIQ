import numpy as np
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler


def create_pipe(n_clusters):
    pipe_log = FunctionTransformer(func=np.log1p, inverse_func=np.expm1)
    pipe = Pipeline(
        [
            ("Logarithm", pipe_log),
            ("Standard_scaler", StandardScaler()),
            ("KMeans", KMeans(n_clusters=n_clusters, random_state=42)),
        ]
    )
    return pipe
