from segmentiq.cluster import create_pipe


def test_pipe_labels_every_customer(rfm_df):
    labels = create_pipe(n_clusters=2).fit_predict(rfm_df)
    assert len(labels) == len(rfm_df)
    assert set(labels) == {0, 1}


def test_pipe_separates_loyal_from_churned(rfm_df):
    labels = create_pipe(n_clusters=2).fit_predict(rfm_df)
    assert set(labels[:3]) != set(labels[3:])
    assert len(set(labels[:3])) == 1
    assert list(labels) == list(create_pipe(n_clusters=2).fit_predict(rfm_df))
