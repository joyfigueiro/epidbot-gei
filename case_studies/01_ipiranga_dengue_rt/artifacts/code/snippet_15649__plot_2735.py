# Auto-generated Python code from EpiDBot sandbox
# This code was executed in the sandbox and produced figure(s).


import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import gamma as gammadist

df = pd.read_parquet('/data/mosqlimate/infodengue_dengue_4110508_2023-12-01_2025-12-28/data.parquet')
df['data_iniSE']=pd.to_datetime(df['data_iniSE'])
df=df.sort_values('data_iniSE').drop_duplicates('data_iniSE').reset_index(drop=True)

def disc(mean,sd,max_len=40):
    shape=(mean/sd)**2; rate=mean/sd**2
    p=np.array([gammadist.cdf(k+.5,shape,scale=1/rate)-gammadist.cdf(k-.5,shape,scale=1/rate) for k in range(max_len+1)])
    p[0]=0.; return p/p.sum()

def cori(I,si,window=7,a=1.,b=.2):
    n=len(I); lam=np.zeros(n)
    for s in range(1,n): lam[s]=sum(I[s-u]*si[u] for u in range(1,min(s,len(si)-1)+1))
    rows=[]
    for t in range(window-1,n):
        SI_=I[t-window+1:t+1].sum(); SL=lam[t-window+1:t+1].sum(); sh=a+SI_; r=b+SL
        rows.append({'idx':t,'win_cases':SI_,'Rt':sh/r,'lo':gammadist.ppf(.025,sh,scale=1/r),
                     'hi':gammadist.ppf(.975,sh,scale=1/r),'p_gt1':1-gammadist.cdf(1,sh,scale=1/r)})
    return pd.DataFrame(rows)

r=cori(df.casos.to_numpy().astype(float),disc(2.0,1.0),7)
r['week']=df.data_iniSE.iloc[r.idx].values; r['SE']=df.SE.iloc[r.idx].values
r['casos']=df.casos.iloc[r.idx].values; r['inc100k']=df.p_inc100k.iloc[r.idx].values
r25=r[pd.to_datetime(r.week).dt.year==2025].reset_index(drop=True)

def runs(mask, minlen):
    out=[];st=None
    for i,v in enumerate(mask):
        if v and st is None: st=i
        if not v and st is not None: out.append((st,i-1)); st=None
    if st is not None: out.append((st,len(mask)-1))
    return [(a,b) for a,b in out if b-a+1>=minlen]

print("=== runs with Rt > 1 (>=3 weeks) ===")
for a,b in runs(list(r25.Rt>1),3):
    print(f"  SE{int(r25.SE[a])}-{int(r25.SE[b])}: {b-a+1} wks | Rt {r25.Rt[a:b+1].min():.2f}-{r25.Rt[a:b+1].max():.2f} | cases {int(r25.casos[a:b+1].sum())}")
print("=== runs with lower 95% CI > 1 (>=2 weeks) ===")
for a,b in runs(list(r25.lo>1),2):
    print(f"  SE{int(r25.SE[a])}-{int(r25.SE[b])}: {b-a+1} wks | Rt {r25.Rt[a:b+1].min():.2f}-{r25.Rt[a:b+1].max():.2f} | cases {int(r25.casos[a:b+1].sum())} | first week {r25.week[a].date()}")

peak=r25.loc[r25.casos.idxmax()]
print(f"\npeak week: SE{int(peak.SE)} ({peak.week.date()}) {int(peak.casos)} cases, {peak.inc100k:.1f}/100k")
print(f"2025 total: {int(r25.casos.sum())} cases; annual incidence {r25.casos.sum()/14230*100000:.1f}/100k")
print(f"weeks with zero reported cases: {int((r25.casos==0).sum())}; long zero run SE{int(r25.SE[(r25.casos==0)&(r25.index>28)].min())}-{int(r25.SE[(r25.casos==0)&(r25.index>28)].max())}")
print(f"Aug artefact weeks (0 cases in window, Rt drifting to prior mean 5.0): SE{int(r25.SE[(r25.win_cases==0)].min())}-{int(r25.SE[(r25.win_cases==0)].max())}")

# ---- figure ----
fig,ax=plt.subplots(figsize=(13,6))
x=np.arange(len(r25))
ax.bar(x,r25.casos,color='#9ecae1',edgecolor='#6baed6',label='weekly notified cases')
ax2=ax.twinx()
ax2.fill_between(x,r25.lo,r25.hi,color='#e6550d',alpha=.22,label='Rt 95% CI')
ax2.plot(x,r25.Rt,color='#e6550d',lw=2,label='Rt (posterior mean)')
ax2.axhline(1,color='k',ls='--',lw=1)
for a,b in runs(list(r25.lo>1),2):
    ax2.axvspan(a-.5,b+.5,color='#fdae6b',alpha=.28,zorder=0)
ax2.set_ylim(0,12); ax.set_ylim(0,17)
ax.set_ylabel('notified cases / week'); ax2.set_ylabel('Rt')
ax.set_xticks(x[::4]); ax.set_xticklabels([f"SE{int(v)}" for v in r25.SE[::4]],rotation=45,ha='right',fontsize=8)
ax.set_title('Ipiranga (PR) — dengue Rt, 2025\nCori et al. (2013), 7-week window, gamma SI mean 14 d (sd 7 d); shaded = 95% CI > 1',fontsize=11)
h1,l1=ax.get_legend_handles_labels(); h2,l2=ax2.get_legend_handles_labels()
ax.legend(h1+h2,l1+l2,loc='upper left',fontsize=9)
ax.set_xlabel('epidemiological week (InfoDengue)')
plt.tight_layout(); plt.savefig('/data/plots/ipiranga_rt_2025.png',dpi=150)
print("\nsaved figure")
