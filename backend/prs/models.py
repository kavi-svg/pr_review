from django.db import models
class Repository(models.Model):
    name=models.CharField(max_length=255); full_name=models.CharField(max_length=512,unique=True,db_index=True); owner=models.CharField(max_length=255); url=models.URLField()
    def __str__(self): return self.full_name
class PullRequest(models.Model):
    repository=models.ForeignKey(Repository,on_delete=models.CASCADE,related_name='pull_requests')
    github_pr_number=models.PositiveIntegerField(); title=models.CharField(max_length=500); description=models.TextField(blank=True); author=models.CharField(max_length=255,blank=True); state=models.CharField(max_length=30)
    created_at=models.DateTimeField(null=True); updated_at=models.DateTimeField(null=True); merged_at=models.DateTimeField(null=True,blank=True)
    additions=models.PositiveIntegerField(default=0); deletions=models.PositiveIntegerField(default=0); changed_files=models.PositiveIntegerField(default=0); commits=models.PositiveIntegerField(default=0)
    features=models.JSONField(default=dict,blank=True); analysis=models.JSONField(default=dict,blank=True); rule_risk_score=models.FloatField(null=True,blank=True); ml_risk_score=models.FloatField(null=True,blank=True); analyzed_at=models.DateTimeField(null=True,blank=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['repository','github_pr_number'],name='unique_repo_pr')]
        indexes=[models.Index(fields=['state','updated_at'])]
    def __str__(self): return f'{self.repository.full_name}#{self.github_pr_number}'
