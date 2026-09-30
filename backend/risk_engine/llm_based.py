from django.conf import settings
def analyze_with_llm(pr_data):
 """Provider adapter boundary; no score is invented when a provider is absent."""
 if not settings.LLM_API_KEY or not settings.LLM_PROVIDER: return {'available':False,'status':'not_configured','reason':'Set LLM_PROVIDER and LLM_API_KEY to enable LLM analysis.'}
 return {'available':False,'status':'not_implemented','reason':f'LLM provider adapter for {settings.LLM_PROVIDER} has not been configured.'}
