from django.conf import settings
class GitHubServiceError(Exception): pass
class GitHubService:
 def __init__(self):
  if not settings.GITHUB_TOKEN: raise GitHubServiceError('GitHub integration is not configured: set GITHUB_TOKEN.')
  try:
   from github import Github
   self.client=Github(settings.GITHUB_TOKEN)
  except ImportError as exc: raise GitHubServiceError('PyGithub is not installed.') from exc
 def get_pull_request(self, full_name, number):
  if '/' not in full_name or number < 1: raise GitHubServiceError('Repository must be owner/repository and PR number must be positive.')
  try:
   repo=self.client.get_repo(full_name); pr=repo.get_pull(number); return repo,pr,list(pr.get_files())
  except Exception as exc:
   status=getattr(exc,'status',None)
   if status==403: raise GitHubServiceError('GitHub request was denied or rate limited.') from exc
   if status==404: raise GitHubServiceError('Repository or pull request was not found.') from exc
   raise GitHubServiceError(f'GitHub API request failed: {exc}') from exc
