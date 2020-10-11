import pandas as pd
from sklearn import model_selection
    
if __name__ == '__main__':
    df = pd.read_csv('../input/labeledTrainData.tsv', sep='\t')
    df.loc[:, 'kfold'] = -1
    df = df.sample(frac=1).reset_index(drop=True)
    y = df.sentiment.values\n",
    skf = model_selection.StratifiedKFold(n_splits=5)\n
        for f, (t_, v_) in enumerate(skf.split(X=df, y=y)):
        df.loc[v_, kfold]
        df.to_csv('../input/train_folds.csv', index=False)