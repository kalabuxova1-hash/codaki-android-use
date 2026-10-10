import test from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import worker from '../server/index.js';

function environment() {
  const sql = new DatabaseSync(':memory:');
  function prepare(query, args=[]) {
    const stmt=()=>sql.prepare(query);
    return { bind(...values){return prepare(query,values);},
      async run(){const result=stmt().run(...args);return {meta:{changes:Number(result.changes)}};},
      async first(){return stmt().get(...args)??null;},
      async all(){return {results:stmt().all(...args)};} };
  }
  return {DB:{prepare,async batch(statements){sql.exec('BEGIN');try{const r=[];for(const s of statements)r.push(await s.run());sql.exec('COMMIT');return r;}catch(e){sql.exec('ROLLBACK');throw e;}}},AGENT_TOKEN:'a'.repeat(64),MCP_WAIT_MS:'0',AGENT_WAIT_MS:'0'};
}
function request(path,body,headers={}) { return new Request('https://example.test'+path,{method:body===undefined?'GET':'POST',headers:{'Content-Type':'application/json',...headers},...(body===undefined?{}:{body:JSON.stringify(body)})}); }
async function call(env,name,args={},user='owner',id=crypto.randomUUID()) {
  if(name!=='android_job_result')args={request_id:crypto.randomUUID(),...args};
  const response=await worker.fetch(request('/mcp',{jsonrpc:'2.0',id,method:'tools/call',params:{name,arguments:args}},user?{'oai-authenticated-user-id':user}:{}),env);
  return {status:response.status,body:await response.json()};
}
const agentHeaders={Authorization:'Bearer '+'a'.repeat(64)};
async function heartbeat(env){return worker.fetch(request('/agent/jobs/next',undefined,agentHeaders),env);}
function value(response){return JSON.parse(response.body.result.content[0].text);}

test('anonymous and service-only callers cannot execute phone commands',async()=>{
  const env=environment(); const result=await call(env,'android_start',{},null);
  assert.equal(result.status,403);
});
test('discovery lists core GUI tools without shell execution',async()=>{
  const env=environment();
  const r=await worker.fetch(request('/mcp',{jsonrpc:'2.0',id:1,method:'tools/list'}),env);
  const body=await r.json();
  assert.ok(body.result.tools.some(x=>x.name==='android_set_text'));
  assert.ok(body.result.tools.some(x=>x.name==='android_job_result'));
  assert.ok(!body.result.tools.some(x=>x.name==='root_shell'));
});
test('offline phone never queues an action',async()=>{
  const env=environment();const r=await call(env,'android_start');
  assert.equal(r.body.result.isError,true);
  assert.match(r.body.result.content[0].text,/offline/i);
});
test('owner binding rejects a second user and foreign job reads',async()=>{
  const env=environment();await call(env,'android_privileges');
  const r=await call(env,'android_start',{},'other');assert.equal(r.status,403);
});
test('service endpoints reject invalid credentials',async()=>{
  const env=environment(); const r=await worker.fetch(request('/agent/jobs/next'),env);assert.equal(r.status,401);
});
test('invalid keys, extra arguments and oversized batches are rejected before queueing',async()=>{
  const env=environment();await heartbeat(env);
  for(const [name,args] of [['android_key',{key:'HOME'}],['android_tap',{x:2,y:3,display:0}],['android_batch',{steps:Array(19).fill({op:'status'})}],['android_set_text',{text:'x'.repeat(1001)}],['root_shell',{command:'id'}]]){
    const r=await call(env,name,args);assert.ok(r.body.error||r.body.result?.isError,JSON.stringify(r));
  }
  assert.equal((await heartbeat(env)).status,204);
});
test('queue claims once and returns Unicode and PNG results intact',async()=>{
  const env=environment();await heartbeat(env);
  const r=await call(env,'android_set_text',{text:'Привет мир'});const queued=value(r);assert.equal(queued.status,'queued');
  const claim=await (await heartbeat(env)).json();assert.equal(claim.job.arguments.text,'Привет мир');
  assert.equal((await heartbeat(env)).status,204);
  const result={content:[{type:'image',mimeType:'image/png',data:'iVBORw0KGgo='},{type:'text',text:'Готово'}],isError:false};
  const saved=await worker.fetch(request('/agent/jobs/'+claim.job.id+'/result',{status:'completed',result},agentHeaders),env);assert.equal(saved.status,200);
  const read=await call(env,'android_job_result',{job_id:queued.job_id});assert.deepEqual(read.body.result,result);
});
test('queue full refuses further work and a request ID from another session is not a replay key',async()=>{
  const env=environment();await heartbeat(env);
  const a=value(await call(env,'android_privileges',{},'owner',1));
  const b=value(await call(env,'android_privileges',{},'owner',1));assert.notEqual(a.job_id,b.job_id);
  for(let i=0;i<6;i++)await call(env,'android_privileges');
  const r=await call(env,'android_start');assert.equal(r.body.result.isError,true);assert.match(r.body.result.content[0].text,/full/i);
});
test('lost MCP response can be retried with request_id without duplicating an action',async()=>{
 const env=environment();await heartbeat(env);
 const args={request_id:'stable-action-id',x:1,y:2};
 const a=value(await call(env,'android_tap',args));const b=value(await call(env,'android_tap',args));assert.equal(a.job_id,b.job_id);
 const claim=await (await heartbeat(env)).json();assert.deepEqual(claim.job.arguments,{x:1,y:2});
 assert.equal((await heartbeat(env)).status,204);
 const mismatch=await call(env,'android_tap',{...args,x:3});assert.ok(mismatch.body.error||mismatch.body.result?.isError);
});
test('failed result storage returns retryable HTTP error and keeps job retrievable',async()=>{
 const env=environment();await heartbeat(env);
 const queued=value(await call(env,'android_privileges'));
 await heartbeat(env);
 const original=env.DB.batch;env.DB.batch=async()=>{throw Error('database temporarily unavailable');};
 const result={content:[{type:'text',text:'done'}],isError:false};
 const failed=await worker.fetch(request('/agent/jobs/'+queued.job_id+'/result',{status:'completed',result},agentHeaders),env);
 assert.equal(failed.status,503);
 env.DB.batch=original;
 const retried=await worker.fetch(request('/agent/jobs/'+queued.job_id+'/result',{status:'completed',result},agentHeaders),env);assert.equal(retried.status,200);
 assert.deepEqual((await call(env,'android_job_result',{job_id:queued.job_id})).body.result,result);
});

const pause=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function claimSoon(env){
 for(let i=0;i<30;i++){const r=await heartbeat(env);if(r.status===200)return (await r.json()).job;await pause(10);}
 throw Error('Job was not offered');
}
async function saveResult(env,job,result,status='completed'){
 const r=await worker.fetch(request('/agent/jobs/'+job.id+'/result',{status,result},agentHeaders),env);
 assert.equal(r.status,200);
}
test('fast phone execution returns its result in the original MCP call',async()=>{
 const env=environment();await heartbeat(env);env.MCP_WAIT_MS='1500';
 const response=call(env,'android_privileges',{request_id:'sync-result-1'});
 const job=await claimSoon(env);
 const result={content:[{type:'text',text:'completed once'}],isError:false};
 await saveResult(env,job,result);
 assert.deepEqual((await response).body.result,result);
 assert.deepEqual((await call(env,'android_privileges',{request_id:'sync-result-1'})).body.result,result);
 assert.equal((await heartbeat(env)).status,204);
});
test('retrieving an in-flight job waits briefly and returns its PNG intact',async()=>{
 const env=environment();await heartbeat(env);
 const queued=value(await call(env,'android_capture'));
 const job=await claimSoon(env);env.MCP_WAIT_MS='1500';
 const response=call(env,'android_job_result',{job_id:queued.job_id});
 await pause(40);
 const result={content:[{type:'image',mimeType:'image/png',data:'iVBORw0KGgo='}],isError:false};
 await saveResult(env,job,result);
 assert.deepEqual((await response).body.result,result);
});
test('agent long poll receives work queued after its request began',async()=>{
 const env=environment();await heartbeat(env);env.AGENT_WAIT_MS='1500';
 const waiting=heartbeat(env);await pause(40);
 const queued=value(await call(env,'android_privileges'));
 const response=await waiting;assert.equal(response.status,200);
 assert.equal((await response.json()).job.id,queued.job_id);
 env.AGENT_WAIT_MS='0';assert.equal((await heartbeat(env)).status,204);
});
test('cancelled agent wait does not claim work queued after disconnect',async()=>{
 const env=environment();await heartbeat(env);env.AGENT_WAIT_MS='1500';
 const abort=new AbortController();
 const waiting=worker.fetch(new Request(request('/agent/jobs/next',undefined,agentHeaders),{signal:abort.signal}),env);
 await pause(40);abort.abort();
 const queued=value(await call(env,'android_privileges'));
 assert.equal((await waiting).status,204);
 env.AGENT_WAIT_MS='0';assert.equal((await claimSoon(env)).id,queued.job_id);
});
test('wait budget expires with the same pending job, without replay',async()=>{
 const env=environment();await heartbeat(env);env.MCP_WAIT_MS='40';
 const a=value(await call(env,'android_tap',{request_id:'bounded-wait-1',x:1,y:1}));
 const b=value(await call(env,'android_tap',{request_id:'bounded-wait-1',x:1,y:1}));
 assert.equal(a.job_id,b.job_id);assert.equal(a.status,'queued');
 const job=await claimSoon(env);assert.equal(job.id,a.job_id);
 assert.equal((await heartbeat(env)).status,204);
});
test('batch can prepare and release an isolated session in one request',async()=>{
 const env=environment();await heartbeat(env);
 const queued=await call(env,'android_batch',{steps:[{op:'privileges'},{op:'start'},{op:'stop'}]});
 assert.equal(queued.body.result.isError,false);
 const job=await claimSoon(env);assert.deepEqual(job.arguments.steps,[{op:'privileges'},{op:'start'},{op:'stop'}]);
});
