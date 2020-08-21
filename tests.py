import pytest

import pandas as pd
from catboost import CatBoostClassifier

from sklearn.metrics import roc_auc_score, precision_score, recall_score

@pytest.fixture
def model():
    return CatBoostClassifier().load_model(fname='catboost_model.cbm')

@pytest.fixture
def df_holdout():
    return pd.read_pickle('data/df_holdout.p')

@pytest.fixture
def X(df_holdout):
    return df_holdout.drop(columns=['churn'])

@pytest.fixture
def y(df_holdout):
    return df_holdout['churn']

def test_roc_auc(model, X, y):
    y_pred_proba = model.predict_proba(X)
    score = roc_auc_score(y, y_pred_proba[:,1])
    
    assert score > 0.85, 'Model is not good enough to push to production'
    
def test_precision(model, X, y):
    y_pred = model.predict(X)
    y = y.astype(str)
    
    score = precision_score(y, y_pred, pos_label='True')
    
    assert score > 0.75, 'Model is not good enough to push to production'
    
def test_recall(model, X, y):
    y_pred = model.predict(X)
    y = y.astype(str)
    
    score = recall_score(y, y_pred, pos_label='True')
    
    assert score > 0.75, 'Model is not good enough to push to production'
    