#!/usr/bin/env python3
"""BATCH01·02 원본 PDF를 SOURCES.csv의 download_url / answer_url에서 다시 내려받는다.

사용: python3 fetch_originals.py [--subject SCI|SOC] [--out 저장폴더] [--limit N] [--workers 4]
- 표준 라이브러리만 사용. 파일은 SOURCES.csv의 local_path / answer_local_path 위치(저장소 루트 기준)에 저장.
- 이미 있는 파일은 건너뛰고, %PDF 머리와 SHA-256(있을 때)을 확인한다. 실패 URL은 fetch_failed.txt에 남긴다.
- EBSi 서버는 요청을 빠르게 반복하면 연결을 끊으므로 workers는 4 이하를 권장한다.
"""
import argparse,csv,hashlib,os,sys,time,urllib.parse,urllib.request
from concurrent.futures import ThreadPoolExecutor
HERE=os.path.dirname(os.path.abspath(__file__));REPO=os.path.dirname(HERE)
def safe(u):
    p=urllib.parse.urlsplit(u)
    return urllib.parse.urlunsplit((p.scheme,p.netloc,urllib.parse.quote(urllib.parse.unquote(p.path),safe="/()[]+%"),p.query,p.fragment))
def get(url,dest,want_sha=''):
    if os.path.exists(dest) and os.path.getsize(dest)>0: return 'skip'
    os.makedirs(os.path.dirname(dest),exist_ok=True)
    for t in range(4):
        try:
            req=urllib.request.Request(safe(url),headers={'User-Agent':'Mozilla/5.0'})
            data=urllib.request.urlopen(req,timeout=120).read()
            if dest.endswith('.pdf') and not data.startswith(b'%PDF'): return 'notpdf'
            if want_sha and hashlib.sha256(data).hexdigest()!=want_sha: return 'shamismatch'
            open(dest,'wb').write(data);return 'ok'
        except Exception as e:
            err=str(e);time.sleep(2*(t+1))
    return 'fail:'+err[:60]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--subject',choices=['SCI','SOC']);ap.add_argument('--out',default=REPO);ap.add_argument('--limit',type=int,default=0);ap.add_argument('--workers',type=int,default=4)
    a=ap.parse_args();jobs=[]
    for s in ([a.subject] if a.subject else ['SCI','SOC']):
        for r in csv.DictReader(open(os.path.join(HERE,'BATCH02',s,'SOURCES.csv'),encoding='utf-8-sig')):
            if r['duplicate_of']: continue
            if r['download_url'] and r['local_path']: jobs.append((r['download_url'],os.path.join(a.out,r['local_path']),r['sha256']))
            if r['answer_url'] and r['answer_local_path']: jobs.append((r['answer_url'],os.path.join(a.out,r['answer_local_path']),''))
    if a.limit: jobs=jobs[:a.limit]
    print(len(jobs),'files');bad=[];n=0
    with ThreadPoolExecutor(a.workers) as ex:
        for (u,d,_),st in zip(jobs,ex.map(lambda j:get(*j),jobs)):
            n+=1
            if st not in('ok','skip'): bad.append(f'{st}\t{u}')
            if n%100==0: print(n,'done',len(bad),'failed',flush=True)
    open(os.path.join(HERE,'fetch_failed.txt'),'w').write('\n'.join(bad))
    print('done; failed',len(bad))
main()
