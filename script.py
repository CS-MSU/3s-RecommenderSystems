import pickle
import surprise

import numpy as np
import pandas as pd

def main():
    print("READING DATA!")

    r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
    ratings = pd.read_csv('ml-100k/u.data', sep='\t', names=r_cols,encoding='latin-1')

    reader = surprise.Reader()
    dataset = surprise.Dataset.load_from_df(ratings[['user_id', 'movie_id', 'rating']], reader)
    train_dataset = dataset.build_full_trainset()
    valid_dataset = train_dataset.build_testset()
    test_dataset = train_dataset.build_anti_testset()

    print("LOADING MODELS")
    svd = pickle.load(open('models/svd.pkl', 'rb'))
    svdpp = pickle.load(open('models/svdpp.pkl', 'rb'))
    nmf = pickle.load(open('models/nmf.pkl', 'rb'))
    knn_ub = pickle.load(open('models/svd.pkl', 'rb'))
    knn_ib = pickle.load(open('models/svd.pkl', 'rb'))
    coclustering = pickle.load(open('models/svd.pkl', 'rb'))
    slopeOne = pickle.load(open('models/svd.pkl', 'rb'))

    print("ESTIMATORS")
    models = [svd, svdpp, nmf, knn_ub, knn_ib, coclustering, slopeOne]
    train = ratings[['user_id', 'movie_id', 'rating']]
    for i in range(7):
        predictions = models[i].test(valid_dataset)
        model_pred = pd.DataFrame([[i.uid, i.iid, i.est] for i in predictions], columns=['user_id', 'movie_id', str(i)])
        train = pd.merge(train, model_pred, how='left', left_on=['user_id', 'movie_id'], right_on=['user_id', 'movie_id'])
    train.columns = train.columns[:3].tolist() + ['svd', 'svdpp', 'nmf', 'knn_ub', 'knn_ib', 'coclustering', 'slopeOne']

    data = np.array(np.meshgrid(np.unique(ratings.user_id), np.unique(ratings.movie_id))).T.reshape(-1, 2)
    test = pd.DataFrame(data, columns=['user_id', 'movie_id'])
    test = pd.concat([test, ratings[['user_id', 'movie_id']]]).drop_duplicates(keep=False)

    models = [svd, svdpp, nmf, knn_ub, knn_ib, coclustering, slopeOne]
    for i in range(7):
        predictions = models[i].test(test_dataset)
        model_pred = pd.DataFrame([[i.uid, i.iid, i.est] for i in predictions], columns=['user_id', 'movie_id', str(i)])
        test = pd.merge(test, model_pred, how='left', left_on=['user_id', 'movie_id'], right_on=['user_id', 'movie_id'])
    test.columns = test.columns[:2].tolist() + ['svd', 'svdpp', 'nmf', 'knn_ub', 'knn_ib', 'coclustering', 'slopeOne']
    train.to_csv('train.csv', index=False)
    test.to_csv('test.csv', index=False)

    print("FINAL ESTIMATOR")
    eNet = pickle.load(open('models/elastic.pkl', 'rb'))
    test['raiting'] = eNet.predict(test.iloc[:, 2:])
    test.to_csv('test.csv', index=False)

    print("DONE!")


if __name__ == "__main__":
    main()