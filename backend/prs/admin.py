from django.contrib import admin
from .models import Repository, PullRequest
admin.site.register(Repository); admin.site.register(PullRequest)
