from collections import Counter
from pathlib import PurePosixPath
SOURCE={'.py','.js','.ts','.tsx','.jsx','.java','.go','.rb','.php','.cs','.cpp','.c','.rs','.swift','.kt'}
DOC={'.md','.rst','.txt','.adoc'}; CONFIG={'.yml','.yaml','.json','.toml','.ini','.cfg','.xml','.env'}
def extract_features(additions, deletions, changed_files, commits, files):
    """Stable feature contract used by collection, training CSVs, and inference."""
    names=[getattr(f,'filename',f.get('filename','')) if not isinstance(f,str) else f for f in files]
    suffixes=[PurePosixPath(n).suffix.lower() for n in names if PurePosixPath(n).suffix]
    source=sum(s in SOURCE for s in suffixes); tests=sum(('test' in n.lower() or 'spec' in n.lower()) for n in names)
    docs=sum(s in DOC for s in suffixes); config=sum(s in CONFIG for s in suffixes)
    total=additions+deletions; file_count=changed_files or len(names)
    size='small' if total<100 else 'medium' if total<500 else 'large' if total<1000 else 'very_large'
    return {'lines_added':additions,'lines_deleted':deletions,'total_changes':total,'files_changed':file_count,'commits':commits,'average_changes_per_file':round(total/max(file_count,1),2),'source_files_changed':source,'test_files_changed':tests,'documentation_files_changed':docs,'configuration_files_changed':config,'number_of_file_types':len(set(suffixes)),'test_to_source_ratio':round(tests/max(source,1),3),'documentation_ratio':round(docs/max(file_count,1),3),'pr_size_category':size}
def extract_from_pr(pr, files):
    return extract_features(pr.additions or 0,pr.deletions or 0,pr.changed_files or len(files),pr.commits or 0,files)
