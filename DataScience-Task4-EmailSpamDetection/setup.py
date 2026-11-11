from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parent
REQ=ROOT/'requirements.txt'; NOTEBOOK=ROOT/'Email_Spam_Detection.ipynb'
def run(args): subprocess.check_call(list(map(str,args)),cwd=ROOT)
def check():
    missing=[]
    for m in ['numpy','pandas','matplotlib','seaborn','sklearn','jupyter','joblib']:
        try: __import__(m); print('[OK]',m)
        except Exception as e: print('[MISSING]',m,e); missing.append(m)
    for p in [NOTEBOOK,ROOT/'data'/'sample_spam.csv']: print('[OK]' if p.exists() else '[MISSING]',p.name)
    if missing: print('Run: python setup.py install'); return 1
    print('Environment check passed.'); return 0
if __name__=='__main__':
    cmd=sys.argv[1].lower() if len(sys.argv)>1 else 'help'
    if cmd=='install': run([sys.executable,'-m','pip','install','--upgrade','pip']); run([sys.executable,'-m','pip','install','-r',REQ])
    elif cmd=='check': sys.exit(check())
    elif cmd=='notebook': run([sys.executable,'-m','jupyter','notebook',NOTEBOOK])
    else: print('Commands: python setup.py install | check | notebook')
