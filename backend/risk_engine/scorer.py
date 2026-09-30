from .rule_based import calculate_rule_based_risk
from .ml_based import calculate_ml_risk
from .llm_based import analyze_with_llm
def analyze_pr(features, pr_data=None, model_name='random_forest'):
 return {'rule_based':calculate_rule_based_risk(features),'ml_based':calculate_ml_risk(features,model_name),'llm_based':analyze_with_llm(pr_data or {'features':features})}
