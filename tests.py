import pytest

import pandas as pd
from catboost import CatBoostClassifier

from sklearn.metrics import roc_auc_score, precision_score, recall_score

STATES =  ['AK','AL','AR','AZ','CA','CO',
          'CT','DC','DE','FL','GA','HI',
          'IA','ID','IL','IN','KS','KY',
          'LA','MA','MD','ME','MI','MN',
          'MO','MS','MT','NC','ND','NE',
          'NH','NJ','NM','NV','NY','OH',
          'OK','OR','PA','RI','SC','SD',
          'TN','TX','UT','VA','VT','WA',
          'WI','WV','WY']

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
    
    assert score > 0.75, 'Model precision is not good enough to push to production'
    
def test_recall(model, X, y):
    y_pred = model.predict(X)
    y = y.astype(str)
    
    score = recall_score(y, y_pred, pos_label='True')
    
    assert score > 0.75, 'Model recall is not good enough to push to production'
    
@pytest.mark.parametrize("state", STATES)
def test_precision_by_state(model, X, y, state):
    
    X_state = X.loc[lambda x: x['state']==state]
    y_state = y.loc[X_state.index]
    
    if y_state.sum() > 0:
    
        y_pred = model.predict(X_state)
        y_state = y_state.astype(str)

        score = precision_score(y_state, y_pred, pos_label='True')

        assert score > 0.3, f'Model precision is not good enough in {state} to push to production - tested on {len(X_state)} samples'    

    
@pytest.mark.parametrize("state", STATES)
def test_recall_by_state(model, X, y, state):
    
    X_state = X.loc[lambda x: x['state']==state]
    y_state = y.loc[X_state.index]
    
    churn_count = y_state.sum()
    if  churn_count> 0:

        y_pred = model.predict(X_state)
        y_state = y_state.astype(str)

        score = recall_score(y_state, y_pred, pos_label='True')

        assert score > 0.3, f'Model precision is not good enough in {state} to push to production - tested on {len(X_state)}'
