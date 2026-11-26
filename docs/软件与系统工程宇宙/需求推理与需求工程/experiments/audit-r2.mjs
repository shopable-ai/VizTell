// R3 new counterexamples. Run from any cwd: node path/to/audit-r2.mjs
// This reproduces the graphCheck part; full standard JSON Schema validation is separate.
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const dir=new URL('../snapshots/R2-original/',import.meta.url);
const read=(p,sha)=>{const b=readFileSync(new URL(p,dir));const actual=createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');if(actual!==sha)throw new Error('Frozen blob mismatch '+p+' '+actual);return b.toString('utf8')};
const source=read('validate-fixtures.mjs','7a6e415c841df8d7dd6c30662134aed5a7eef133');
const fixtures=JSON.parse(read('fixtures.json','1e29fcdbe7f7e5d6e8469d5599f1dbb230b56c1c'));
read('reasoning.schema.json','ecafde5959ffa926912201cdb3bac2a212edc8cb');
const body=source.slice(source.indexOf('function graphCheck'),source.indexOf('const fixtures=JSON.parse(readFileSync'));
const {graphCheck,selfTest}=new Function(body+'\nreturn {graphCheck,selfTest};')();
const base=fixtures[0].output, clone=x=>JSON.parse(JSON.stringify(x)), edge=(a,b,t)=>({from:a,to:b,type:t,rationale:'R3 synthetic counterexample'}), req=x=>x.graph.nodes.find(n=>n.id==='V-R1');
const cases=[
['C01-empty-source',x=>req(x).sourceIds=[]],
['C02-invalid-operator',x=>req(x).operator='NOT_AN_OPERATOR'],
['C03-empty-AND',x=>{x.graph.groups[0].members=[];x.graph.groups[0].selected=[];}],
['C04-bad-root',x=>{x.graph.edges.filter(e=>e.from==='V-R1'&&e.type==='DERIVED_FROM').forEach(e=>e.to='V-T1');}],
['C05-mixed-cycle',x=>x.graph.edges.push(edge('V-T1','V-T2','DERIVED_FROM'))],
['C06-fake-PASS',x=>{const a=x.graph.nodes.find(n=>n.id==='V-A1');x.graph.nodes.push({...clone(a),id:'V-E-R3',type:'EVIDENCE',statement:'不相关且未验证的旧证据',verificationState:'NOT_TESTED',detail:{candidate:'different build',environment:'unrelated',observed:'no execution'}});a.verificationState='PASS';x.graph.edges.push(edge('V-A1','V-E-R3','SUPPORTED_BY'));}],
['C07-P1-no-acceptance',x=>{req(x).priority='P1';x.graph.edges=x.graph.edges.filter(e=>!(e.from==='V-R1'&&e.type==='VERIFIED_BY'));}],
['C08-budget',x=>x.budget.maxNodes=1],
['C09-scope-drift',x=>x.scope.goal='另一个无关目标'],
['C10-fake-independent-score',x=>{x.review=[{dimension:'PRODUCT',status:'INDEPENDENT_SCORED',score:100,evidence:'AI self claim'}];}],
['C11-unjustified-conflict-resolution',x=>{const a=clone(req(x));x.graph.nodes.push({...a,id:'V-D-R3',type:'DECISION',reviewState:'PROPOSED',detail:{authorization:'none'}});x.graph.edges.push({...edge('V-R1','V-R2','CONFLICTS_WITH'),resolutionDecisionId:'V-D-R3'});}],
['C12-unbound-approval',x=>{x.graph.groups[1].state='RESOLVED';x.graph.groups[1].selected=[x.graph.groups[1].members[0]];x.stop.reason='FIXPOINT';x.stop.frontier=[];x.gate.status='APPROVED';x.gate.blockers=[];x.graph.nodes.forEach(n=>{if(n.reviewState==='NEEDS_DECISION')n.reviewState='PROPOSED';});}]
];
const legacy=selfTest(fixtures);
const counterexamples=cases.map(([id,mut])=>{const x=clone(base);mut(x);return {id,errors:graphCheck(x),output:x}});
const withFixtures=process.argv.includes('--include-fixtures');
console.log(JSON.stringify({legacy,counterexamples:counterexamples.map(({id,errors,output})=>withFixtures?{id,errors,output}:{id,errors})},null,2));
if(legacy.some(x=>!x.pass)||counterexamples.some(x=>x.errors.length))process.exitCode=1;
// Exit 0 means reproduction of known gaps only; not a production validator or a PASS on bad inputs.
