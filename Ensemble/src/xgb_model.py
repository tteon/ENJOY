import glob
import numpy as np
import pandas as pd

from sklearn import metrics

from functools import partial
from scipy.optimize import fmin
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression

import xgboost as xgb

def run_training(pred_df, fold):
    train_df = pred_df[pred_df.kfold != fold].reset_index(drop=True)
    valid_df = pred_df[pred_df.kfold == fold].reset_index(drop=True)

    xtrain = train_df[['lr_pred', 'lr_cnt_pred', 'rf_svd_pred']].values
    xvalid = valid_df[['lr_pred', 'lr_cnt_pred', 'rf_svd_pred']].values
    
    scl = StandardScaler()
    xtrain = scl.fit_transform(xtrain)
    xvalid = scl.transform(xvalid)
    
    
    clf = xgb.XGBClassifier()
    clf.fit(xtrain, train_df.sentiment.values)
    preds = clf.predict_proba(xvalid)[:, 1]
    auc = metrics.roc_auc_score(valid_df.sentiment.values, preds)
    print(f'{fold}, {auc}')
    valid_df.loc[:, "xgb_pred"] = preds
    return valid_df


if __name__ == '__main__':
    files = glob.glob("../model_preds/*.csv")
    df = None
    for f in files:
        if df is None:
            df = pd.read_csv(f)
        else:
            temp_df = pd.read_csv(f)
            df = df.merge(temp_df, on="id", how="left")
    targets = df.sentiment.values
    pred_cols = ['lr_pred', 'lr_cnt_pred' ,'rf_svd_pred']
    
    dfs = []
    for j in range(5):
        temp_df = run_training(df, j)
        dfs.append(temp_df)
        
    fin_valid_df = pd.concat(dfs)
    print(
        metrics.roc_auc_score(
            fin_valid_df.sentiment.values, fin_valid_df.xgb_pred.values
        )
    )