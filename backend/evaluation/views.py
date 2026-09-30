import json
from pathlib import Path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ml.train import ARTIFACT_DIR
@api_view(['GET'])
def evaluation(request):
 results=[]
 for p in ARTIFACT_DIR.glob('*.metrics.json'):
  results.append(json.loads(p.read_text()))
 return Response({'evaluations':results,'note':'Metrics are saved only after an actual held-out evaluation during training.'})
