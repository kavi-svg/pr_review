from rest_framework import serializers
from .models import PullRequest
class PullRequestSerializer(serializers.ModelSerializer):
 repository=serializers.CharField(source='repository.full_name',read_only=True)
 pr_number=serializers.IntegerField(source='github_pr_number',read_only=True)
 class Meta: model=PullRequest; fields=['id','repository','pr_number','title','description','author','state','created_at','updated_at','merged_at','additions','deletions','changed_files','commits','features','analysis','analyzed_at']
class FetchSerializer(serializers.Serializer):
 repository=serializers.RegexField(r'^[^/\s]+/[^/\s]+$'); pr_number=serializers.IntegerField(min_value=1)
class AnalyzeSerializer(serializers.Serializer): pr_id=serializers.IntegerField(min_value=1); model=serializers.CharField(required=False,default='random_forest')
class TrainSerializer(serializers.Serializer): dataset_path=serializers.CharField(); model=serializers.ChoiceField(choices=['logistic_regression','random_forest','gradient_boosting','xgboost'],required=False,default='random_forest')
