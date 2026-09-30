"""Generate transparent instructional rows, not a research-quality dataset.
Labels are documented deterministic examples derived from the supplied scenario flags;
replace this file with real, independently labeled historical outcomes for evaluation.
"""
import csv
from pathlib import Path
from prs.services.feature_extractor import extract_features
def generate_demo_dataset(destination):
 scenarios=[(20,5,1,1,['docs/readme.md'],0),(900,300,20,12,['src/a.py','src/b.py','config/app.yml'],1),(130,50,4,2,['src/a.py','tests/test_a.py'],0),(700,600,15,8,['src/a.py','src/b.py'],1)]
 rows=[]
 for additions,deletions,files,commits,names,label in scenarios:
  row=extract_features(additions,deletions,files,commits,names); row['is_risky']=label; rows.append(row)
 # Duplicate documented scenarios with measured-size variants only to meet split mechanics; never use for claims.
 rows=[{**r, 'lines_added':r['lines_added']+i, 'total_changes':r['total_changes']+i} for i in range(8) for r in rows]
 with Path(destination).open('w',newline='') as f: csv.DictWriter(f,fieldnames=rows[0].keys()).writeheader(); csv.DictWriter(f,fieldnames=rows[0].keys()).writerows(rows)
 return len(rows)
