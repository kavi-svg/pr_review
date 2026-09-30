import argparse,json
from pathlib import Path
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from .dataset import load_dataset
from .features import NUMERIC_FEATURES,CATEGORICAL_FEATURES,TARGET_COLUMN
from .evaluate import evaluate_model
ARTIFACT_DIR=Path(__file__).parent/'artifacts'
def make_model(name):
 models={'logistic_regression':LogisticRegression(max_iter=1000,random_state=42),'random_forest':RandomForestClassifier(n_estimators=200,random_state=42,class_weight='balanced'),'gradient_boosting':GradientBoostingClassifier(random_state=42)}
 if name=='xgboost':
  try:
   from xgboost import XGBClassifier; return XGBClassifier(random_state=42,eval_metric='logloss')
  except ImportError as e: raise ValueError('XGBoost is optional; install xgboost to select it.') from e
 if name not in models: raise ValueError(f'Unsupported model: {name}')
 return models[name]
def train_from_csv(dataset_path, model_name='random_forest', target=TARGET_COLUMN):
 df=load_dataset(dataset_path,target); X=df.drop(columns=[target]); y=df[target].astype(int)
 if y.nunique()<2: raise ValueError('Training data must contain both risk classes.')
 Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
 prep=ColumnTransformer([('numeric',Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())]),NUMERIC_FEATURES),('category',Pipeline([('impute',SimpleImputer(strategy='most_frequent')),('encode',OneHotEncoder(handle_unknown='ignore'))]),CATEGORICAL_FEATURES)])
 pipe=Pipeline([('preprocessor',prep),('model',make_model(model_name))]); pipe.fit(Xtr,ytr); metrics=evaluate_model(pipe,Xte,yte,model_name)
 ARTIFACT_DIR.mkdir(exist_ok=True); path=ARTIFACT_DIR/f'{model_name}.joblib'; joblib.dump(pipe,path); (ARTIFACT_DIR/f'{model_name}.metrics.json').write_text(json.dumps(metrics,indent=2))
 return metrics,str(path)
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('dataset'); p.add_argument('--model',default='random_forest'); a=p.parse_args(); print(json.dumps({'metrics':train_from_csv(a.dataset,a.model)[0]},indent=2))
