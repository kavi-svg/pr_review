from django.test import TestCase
from rest_framework.test import APIClient
from prs.models import Repository,PullRequest
from prs.services.feature_extractor import extract_features
from risk_engine.rule_based import calculate_rule_based_risk
class CoreTests(TestCase):
 def setUp(self): self.client=APIClient()
 def test_features_and_rules(self):
  f=extract_features(800,300,3,12,['src/a.py','src/b.py','config/settings.yml'])
  self.assertEqual(f['total_changes'],1100); self.assertEqual(f['source_files_changed'],2); self.assertGreater(calculate_rule_based_risk(f)['score'],0)
 def test_list_and_analyze(self):
  repo=Repository.objects.create(name='repo',full_name='owner/repo',owner='owner',url='https://github.com/owner/repo')
  f=extract_features(5,2,1,1,['README.md']); p=PullRequest.objects.create(repository=repo,github_pr_number=1,title='Docs',state='open',features=f)
  self.assertEqual(self.client.get('/api/prs/').status_code,200)
  response=self.client.post('/api/prs/analyze/',{'pr_id':p.id},format='json'); self.assertEqual(response.status_code,200); self.assertEqual(response.data['analysis']['rule_based']['risk_level'],'Low')
 def test_validation(self): self.assertEqual(self.client.post('/api/prs/fetch/',{'repository':'bad','pr_number':0},format='json').status_code,400)
