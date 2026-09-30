def calculate_rule_based_risk(f):
 score=0; factors=[]
 def add(name,points,value):
  nonlocal score; score+=points; factors.append({'name':name,'impact':f'+{points}','value':str(value)})
 if f['total_changes']>=1000: add('very_large_change_set',30,f['total_changes'])
 elif f['total_changes']>=500: add('large_change_set',20,f['total_changes'])
 elif f['total_changes']>=100: add('moderate_change_set',8,f['total_changes'])
 if f['files_changed']>=20: add('many_files_changed',15,f['files_changed'])
 elif f['files_changed']>=10: add('multiple_files_changed',8,f['files_changed'])
 if f['commits']>=10: add('many_commits',8,f['commits'])
 if f['source_files_changed']>=5 and f['test_to_source_ratio']<.3: add('low_test_change_ratio',18,f['test_to_source_ratio'])
 if f['configuration_files_changed']>0: add('configuration_change',12,f['configuration_files_changed'])
 if f['average_changes_per_file']>=300: add('concentrated_change',10,f['average_changes_per_file'])
 score=min(score,100); return {'score':score,'risk_level':'High' if score>=70 else 'Medium' if score>=35 else 'Low','factors':factors}
