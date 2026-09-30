from pathlib import Path
import joblib,pandas as pd
from .features import FEATURE_COLUMNS
from .train import ARTIFACT_DIR
def risk_level(score): return 'High' if score>=70 else 'Medium' if score>=35 else 'Low'
def predict_risk(features, model_name='random_forest'):
 path=ARTIFACT_DIR/f'{model_name}.joblib'
 if not path.exists(): raise FileNotFoundError(f'No trained {model_name} model found. Train one before requesting predictions.')
 missing=set(FEATURE_COLUMNS)-set(features)
 if missing: raise ValueError(f'Missing prediction features: {sorted(missing)}')
 model=joblib.load(path); probability=float(model.predict_proba(pd.DataFrame([{k:features[k] for k in FEATURE_COLUMNS}]))[0,1]); score=round(probability*100,2)
 result={'score':score,'risk_level':risk_level(score),'model':model_name,'probability':round(probability,4)}
 estimator=model.named_steps['model']
 if hasattr(estimator,'feature_importances_'): result['feature_importance_note']='Importance is an association within this fitted model, not a causal explanation.'
 return result
