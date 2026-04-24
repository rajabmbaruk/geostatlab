import numpy as np

def sample_data(df, method, size):

    size = min(size, len(df))

    if method == "Simple Random":
        return df.sample(n=size)

    if method == "Cluster":
        clusters = np.random.choice(df["County"].unique(), 3)
        return df[df["County"].isin(clusters)]

    if method == "Systematic":
        k = max(1, len(df)//size)
        return df.iloc[::k].head(size)

    if method == "Stratified":
        return df.groupby("County", group_keys=False).apply(
            lambda x: x.sample(min(len(x), max(1, size // df["County"].nunique())))
        )