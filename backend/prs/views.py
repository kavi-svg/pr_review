from pathlib import Path
from django.utils import timezone
from rest_framework import status,viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Repository,PullRequest
from .serializers import PullRequestSerializer,FetchSerializer,AnalyzeSerializer,TrainSerializer
from .services.github_service import GitHubService,GitHubServiceError
from .services.feature_extractor import extract_from_pr
from risk_engine.scorer import analyze_pr
from ml.train import train_from_csv
from ml.predict import predict_risk
class PullRequestViewSet(viewsets.ReadOnlyModelViewSet):
 queryset=PullRequest.objects.select_related('repository').order_by('-updated_at'); serializer_class=PullRequestSerializer
 @action(detail=False,methods=['post'])
 def fetch(self,request):
  s=FetchSerializer(data=request.data); s.is_valid(raise_exception=True)
  try: repo,pr,files=GitHubService().get_pull_request(s.validated_data['repository'],s.validated_data['pr_number'])
  except GitHubServiceError as e: return Response({'detail':str(e)},status=status.HTTP_502_BAD_GATEWAY)
  obj,_=Repository.objects.update_or_create(full_name=repo.full_name,defaults={'name':repo.name,'owner':repo.owner.login,'url':repo.html_url})
  features=extract_from_pr(pr,files)
  pull,_=PullRequest.objects.update_or_create(repository=obj,github_pr_number=pr.number,defaults={'title':pr.title,'description':pr.body or '','author':getattr(pr.user,'login',''),'state':pr.state,'created_at':pr.created_at,'updated_at':pr.updated_at,'merged_at':pr.merged_at,'additions':pr.additions or 0,'deletions':pr.deletions or 0,'changed_files':pr.changed_files or 0,'commits':pr.commits or 0,'features':features})
  return Response(PullRequestSerializer(pull).data,status=status.HTTP_201_CREATED)
 @action(detail=False,methods=['post'])
 def analyze(self,request):
  s=AnalyzeSerializer(data=request.data); s.is_valid(raise_exception=True)
  try: pr=PullRequest.objects.select_related('repository').get(pk=s.validated_data['pr_id'])
  except PullRequest.DoesNotExist: return Response({'detail':'Pull request not found.'},status=404)
  analysis=analyze_pr(pr.features,{'title':pr.title,'description':pr.description,'features':pr.features},s.validated_data['model']); pr.analysis=analysis; pr.rule_risk_score=analysis['rule_based']['score']; pr.ml_risk_score=analysis['ml_based'].get('score'); pr.analyzed_at=timezone.now(); pr.save()
  return Response(PullRequestSerializer(pr).data)
 @action(detail=False,methods=['post'],url_path='ml/train')
 def train(self,request):
  s=TrainSerializer(data=request.data); s.is_valid(raise_exception=True); path=Path(s.validated_data['dataset_path'])
  if not path.is_file(): return Response({'detail':'Dataset path does not exist or is not a file.'},status=400)
  try: metrics,artifact=train_from_csv(path,s.validated_data['model'])
  except ValueError as e: return Response({'detail':str(e)},status=400)
  return Response({'metrics':metrics,'artifact':artifact},status=201)
 @action(detail=False,methods=['post'],url_path='ml/predict')
 def predict(self,request):
  features=request.data.get('features'); model=request.data.get('model','random_forest')
  if not isinstance(features,dict): return Response({'detail':'features must be an object.'},status=400)
  try: return Response(predict_risk(features,model))
  except (FileNotFoundError,ValueError) as e: return Response({'detail':str(e)},status=400)
