import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {database} from './local-db.mjs';
import worker from '../worker/index.js';
import {audit,blindExam,verificationMatches} from '../worker/domain.js';
const {binding:DB,db}=database(':memory:'),env={DB};
const request=(route,value,origin='https://arc.example')=>new Request('https://arc.example/api/'+route,{method:'POST',headers:{origin,'Content-Type':'application/json'},body:JSON.stringify(value)});
async function post(route,value,expected=200,origin){const r=await worker.fetch(request(route,value,origin),env,{});const d=await r.json();assert.equal(r.status,expected,JSON.stringify(d));return d;}
const source=await post('source',{title:'검증용 원문',subject:'과학',text:'산화는 전자를 잃는 반응이다. 환원은 전자를 얻는 반응이다. 반응 전후 전하량은 보존된다.',location:'테스트 원문'});
assert.match(source.sha256,/^[a-f0-9]{64}$/);
const q={stem:'산화에 대한 설명으로 옳은 것은?',options:['전자를 잃는다.','전자를 얻는다.','항상 양성자를 얻는다.','전하 보존이 성립하지 않는다.','항상 산소만 잃는다.'],answer:1,sourceIds:[source.id],evidence:Array.from({length:5},()=>({sourceId:source.id,quote:'산화는 전자를 잃는 반응이다.',reason:'검증용 근거 기록'})),part:'A',passage:''};
let exam=await post('exam',{title:'테스트용 시험지',subject:'과학',product:'N°',scope:'산화 환원',difficulty:'학교 상',sources:[source],questions:[q]});
assert.equal(exam.status,'DRAFT');
await post('exam',{...exam,revision:0},409);
await post('exam',{...exam,status:'APPROVED',aiVerification:{matches:true},review:{facts:true}});
exam=(await (await worker.fetch(new Request('https://arc.example/api/state'),env,{})).json()).exams[0];assert.equal(exam.status,'DRAFT');assert.equal(exam.aiVerification,null);
exam=await post('audit',{id:exam.id});assert.equal(exam.qa.structural,'PASS');assert.equal(exam.qa.independent,'NOT_RUN');
await post('approve',{id:exam.id,revision:exam.revision,review:{facts:true}},400);
const review={facts:true,unique:true,scope:true,difficulty:true,duplicates:true};
await post('approve',{id:exam.id,revision:exam.revision,review},400);
const originalFetch=globalThis.fetch;
const readExam=async()=> (await (await worker.fetch(new Request('https://arc.example/api/state'),env,{})).json()).exams[0];
try{
 // Synthetic responses exercise server gates; no external AI call or credential is used.
 env.OPENAI_API_KEY='synthetic-test-value';env.ARC_AI_MODEL='synthetic-test-model';
 globalThis.fetch=async (_url,options)=>{
  const input=JSON.parse(options.body).input;
  const data=JSON.parse(input.slice(input.indexOf('\n')+1));
  assert.ok(!('answer' in data.questions[0]));assert.ok(!('evidence' in data.questions[0]));
  return Response.json({status:'completed',output:[{content:[{type:'output_text',text:JSON.stringify({questions:[{answer:1,unique:true,inScope:true,difficultyMatches:true,optionReasons:['a','b','c','d','e']}]})}]}]});
 };
 exam=await post('verify',{id:exam.id});assert.equal(exam.aiVerification.status,'PASS');
 globalThis.fetch=async()=>{throw new Error('synthetic network failure');};
 await post('verify',{id:exam.id},502);exam=await readExam();
 assert.equal(exam.status,'QA_FAILED');assert.equal(exam.aiVerification.status,'ERROR');
 await post('approve',{id:exam.id,revision:exam.revision,review},400);
 globalThis.fetch=async()=>Response.json({status:'completed',output:[{content:[{type:'output_text',text:JSON.stringify({questions:[{answer:2,unique:true,inScope:true,difficultyMatches:true,optionReasons:['a','b','c','d','e']}]})}]}]});
 exam=await post('verify',{id:exam.id});assert.equal(exam.aiVerification.status,'FAIL');
 await post('approve',{id:exam.id,revision:exam.revision,review},400);
 globalThis.fetch=async()=>Response.json({status:'completed',output:[{content:[{type:'output_text',text:JSON.stringify({questions:[{answer:1,unique:true,inScope:true,difficultyMatches:true,optionReasons:['a','b','c','d','e']}]})}]}]});
 exam=await post('verify',{id:exam.id});assert.equal(exam.aiVerification.status,'PASS');
}finally{globalThis.fetch=originalFetch;delete env.OPENAI_API_KEY;delete env.ARC_AI_MODEL;}
exam=await post('approve',{id:exam.id,revision:exam.revision,review});assert.equal(exam.status,'APPROVED');assert.equal(exam.review.method,'AI_AND_HUMAN');
await post('exam',exam,409);
const duplicate=audit(exam,[exam]);assert.equal(duplicate.structural,'FAIL');
const bad=structuredClone(exam);bad.questions[0].evidence[0].quote='원문에 없는 내용';assert.equal(audit(bad).structural,'FAIL');
bad.questions[0].options[1]=bad.questions[0].options[0];assert.ok(audit(bad).issues.some(s=>s.includes('동일한 선지')));
const blind=blindExam(exam);assert.ok(!('answer' in blind.questions[0]));assert.ok(!('evidence' in blind.questions[0]));
assert.equal(verificationMatches(exam,{questions:[{answer:2,unique:true,inScope:true,difficultyMatches:true,optionReasons:['a','b','c','d','e']}]}),false);
await post('source',{title:'잘못된 요청',subject:'과학',text:'원문'},403,'https://other.example');
await post('research',{query:'테스트'},503);
const generation={title:'신규 생성',subject:'과학',product:'FINAL',scope:'산화 환원',difficulty:'학교 상',count:1,sourceIds:[source.id]};await post('generate',generation,503);
const noStorage=await worker.fetch(new Request('https://arc.example/api/state'),{},{});assert.equal((await noStorage.json()).capabilities.storage,false);
await post('brand',{core:'#77736b',n:'#182238',final:'#782d42'});
const inspected=await post('inspect',{});assert.ok(inspected.checks.some(c=>c.title.includes('회귀')&&c.status==='NOT_RUN'));
const state=await (await worker.fetch(new Request('https://arc.example/api/state'),env,{})).json();assert.equal(state.sources.length,1);assert.equal(state.exams.length,1);assert.equal(state.exams[0].status,'APPROVED');assert.equal(state.audits.length,1);
for(const p of ['/','/app.js','/app.css'])assert.equal((await worker.fetch(new Request('https://arc.example'+p),env,{})).status,200);
const syntax=spawnSync(process.execPath,['--check','ui/app.js'],{cwd:new URL('..',import.meta.url)});assert.equal(syntax.status,0,syntax.stderr?.toString());
db.close();console.log('PASS: persistence, revisions, evidence, duplicates, approval lock, blinded solver inputs, blocked AI, origin checks and assets.');
