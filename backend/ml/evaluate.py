from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,confusion_matrix
def evaluate_model(model,X,y,model_name):
 pred=model.predict(X); prob=model.predict_proba(X)[:,1] if hasattr(model,'predict_proba') else None
 return {'model':model_name,'accuracy':round(float(accuracy_score(y,pred)),4),'precision':round(float(precision_score(y,pred,zero_division=0)),4),'recall':round(float(recall_score(y,pred,zero_division=0)),4),'f1':round(float(f1_score(y,pred,zero_division=0)),4),'roc_auc':round(float(roc_auc_score(y,prob)),4) if prob is not None and len(set(y))==2 else None,'confusion_matrix':confusion_matrix(y,pred).tolist()}
