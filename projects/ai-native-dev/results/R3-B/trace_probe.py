"""Synthetic mutation checks of a trace gate, seeded by historical queue acceptance facts.
Not actual OpenDesk release validation; no deployment or API calls."""
import json
from copy import deepcopy

# Predefined release-eligibility checks: each independently necessary, not a score.
# A minimal status-only baseline checks source implementation/build/candidate package.
# Candidate gate requires current passing suite + exact candidate installed and executed +
# required behavior in native context + no unresolved release blocker + matching provenance.
req={'trusted_shortcut','fifo_no_replay','draft_ime','route_owner'}
complete={'source':True,'build':True,'package':True,'suite_pass':True,'release_blocked':False,
          'candidate':'r16/hash-A','installed':'r16/hash-A','executed':'r16/hash-A',
          'native_behavior':{k:'r16/hash-A' for k in req}}
# historical document explicitly says 246/247, no native r16 install/execute, blocked.
historical={**complete,'suite_pass':False,'release_blocked':True,'installed':None,'executed':None,'native_behavior':{}}

def baseline(r): return all(r[k] for k in ['source','build','package'])
def linked(r):
    fail=[]
    for k in ['source','build','package','suite_pass']:
        if not r[k]: fail.append(k)
    if r['release_blocked']: fail.append('release_blocked')
    for k in ['installed','executed']:
        if r[k]!=r['candidate']: fail.append(k+'_identity')
    for k in sorted(req):
        if r['native_behavior'].get(k)!=r['candidate']: fail.append('native:'+k)
    return not fail,fail
scenarios=[('historical_report',historical,False),('hypothetical_complete',complete,True)]
for name,change in [('old_installed_version',{'installed':'r15/hash-B'}),('old_run_receipt',{'executed':'r15/hash-B'}),('full_suite_fail',{'suite_pass':False}),('unresolved_release_block',{'release_blocked':True}),('missing_native_IME',{'native_behavior':{k:'r16/hash-A' for k in req if k!='draft_ime'}}),('wrong_version_native_FIFO',{'native_behavior':{k:('r15/hash-B' if k=='fifo_no_replay' else 'r16/hash-A') for k in req}})]:
    scenarios.append((name,{**deepcopy(complete),**change},False))
rows=[]
for name,r,expected in scenarios:
    actual,fail=linked(r);assert actual==expected,(name,actual,expected)
    rows.append({'case':name,'expected_release':expected,'status_only':baseline(r),'linked_gate':actual,'failed_edges':fail})
print(json.dumps({'scope':'synthetic gate mutation checks with one historical case; labels are predefined, no independent evaluation','cases':rows},ensure_ascii=False,indent=2))
