from ml.predict import predict_risk
def calculate_ml_risk(features, model_name='random_forest'):
 try: return predict_risk(features,model_name)
 except (FileNotFoundError,ValueError) as exc: return {'available':False,'reason':str(exc)}
