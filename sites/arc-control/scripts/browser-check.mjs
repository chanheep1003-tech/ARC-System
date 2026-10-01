import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import path from 'node:path';
import {database} from './local-db.mjs';
import worker from '../worker/index.js';
const require=createRequire(import.meta.url);
const runtimeModules=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES||'C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium}=require(path.join(runtimeModules,'playwright'));
const {binding:DB,db}=database(':memory:'),env={DB};
const browser=await chromium.launch({headless:true,executablePath:process.env.ARC_CHROME||'C:/Program Files/Google/Chrome/Application/chrome.exe'});
const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.route('http://127.0.0.1:4173/**',async route=>{const r=route.request(),headers=await r.allHeaders();const request=new Request(r.url(),{method:r.method(),headers,...(['GET','HEAD'].includes(r.method())?{}:{body:r.postDataBuffer(),duplex:'half'})});const response=await worker.fetch(request,env,{});await route.fulfill({status:response.status,headers:Object.fromEntries(response.headers),body:Buffer.from(await response.arrayBuffer())});});
try{
 await page.goto('http://127.0.0.1:4173');await page.getByRole('heading',{name:'학습 운영 현황'}).waitFor();
 await page.getByRole('link',{name:'학습 자료실',exact:true}).click();
 await page.locator('#source-form [name=title]').fill('브라우저 검증 원문');await page.locator('#source-form [name=subject]').selectOption('과학');await page.locator('#source-form [name=text]').fill('산화는 전자를 잃는 반응이다. 환원은 전자를 얻는 반응이다. 반응 전후 전하량은 보존된다.');await page.getByRole('button',{name:'자료 저장',exact:true}).click();await page.getByText('브라우저 검증 원문 · 과학',{exact:true}).waitFor();
 await page.getByRole('link',{name:'문제 출제',exact:true}).click();await page.locator('#generate-form [name=subject]').selectOption('과학');await page.locator('#generate-form [name=title]').fill('브라우저 검증 시험지');await page.locator('#generate-form [name=scope]').fill('산화 환원');await page.locator('#generate-form [name=sourceId]').check();await page.getByRole('button',{name:'직접 문항 편집'}).click();
 await page.locator('[data-question] [name=stem]').fill('산화에 대한 설명으로 옳은 것은?');const choices=['전자를 잃는다.','전자를 얻는다.','항상 양성자를 얻는다.','전하 보존이 성립하지 않는다.','항상 산소만 잃는다.'];for(let i=0;i<5;i++)await page.locator(`[name=option${i}]`).fill(choices[i]);
 await page.getByText('선지별 근거',{exact:true}).click();for(let i=0;i<5;i++){await page.locator(`[name=quote${i}]`).fill('산화는 전자를 잃는 반응이다.');await page.locator(`[name=reason${i}]`).fill('검증용 판정 이유');}
 await page.getByRole('button',{name:'원고 저장',exact:true}).click();await page.getByRole('button',{name:'형식·근거 검사'}).waitFor();
 await page.locator('[name=stem]').fill('수정된 발문');await page.getByRole('button',{name:'형식·근거 검사'}).click();await page.getByText('문항을 수정했습니다. 먼저 원고 저장을 눌러 주세요.',{exact:true}).waitFor();await page.locator('[name=stem]').fill('산화에 대한 설명으로 옳은 것은?');await page.getByRole('button',{name:'형식·근거 검사'}).click();await page.getByText('통과',{exact:true}).waitFor();
 for(const k of ['facts','unique','scope','difficulty','duplicates'])await page.locator(`#approve-form [name=${k}]`).check();await page.getByRole('button',{name:'검토 완료·승인',exact:true}).click();await page.getByText('승인·잠금',{exact:true}).waitFor();
 await page.getByRole('button',{name:'시험지 출력',exact:true}).click();await page.locator('.paper').waitFor();assert.equal(await page.locator('.student-q').count(),1);assert.equal(await page.locator('.draft-watermark').count(),0);assert.equal(await page.locator('.student-source').count(),1);assert.equal(await page.locator('.student-options li').count(),5);
 await page.emulateMedia({media:'print'});await page.pdf({path:path.resolve(import.meta.dirname,'../../outputs/ARC_PRINT_QA.pdf'),preferCSSPageSize:true,printBackground:true});await page.emulateMedia({media:'screen'});
 await page.getByRole('button',{name:'정답지',exact:true}).click();assert.equal(await page.locator('.student-q').count(),0);await page.emulateMedia({media:'print'});await page.pdf({path:path.resolve(import.meta.dirname,'../../outputs/ARC_ANSWER_QA.pdf'),preferCSSPageSize:true});await page.emulateMedia({media:'screen'});
 await page.goto('http://127.0.0.1:4173/#brand');await page.getByRole('heading',{name:'브랜드 관리'}).waitFor();await page.locator('[name=n]').fill('#1b2c45');await page.getByRole('button',{name:'설정 저장'}).click();await page.waitForFunction(()=>getComputedStyle(document.documentElement).getPropertyValue('--n')==='#1b2c45');
 await page.goto('http://127.0.0.1:4173/#checks');await page.getByRole('button',{name:'점검 실행'}).click();await page.getByText('ARC 엔진 전체 회귀 검사',{exact:true}).waitFor();assert.equal(await page.getByText('미실행',{exact:true}).count(),1);
 await page.setViewportSize({width:390,height:844});await page.goto('http://127.0.0.1:4173/#dashboard');await page.getByRole('heading',{name:'학습 운영 현황'}).waitFor();assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.screenshot({path:path.resolve(import.meta.dirname,'../../outputs/ARC_MOBILE_QA.png'),fullPage:true});
 await page.setViewportSize({width:1440,height:1000});await page.screenshot({path:path.resolve(import.meta.dirname,'../../outputs/ARC_CONTROL_QA.png'),fullPage:true});assert.deepEqual(errors,[]);console.log('PASS: browser source registration, editor, unsaved-change guard, QA, approval, printing, brand persistence, inspections and mobile width.');
}catch(e){console.error('UI diagnostics',await page.evaluate(()=>({invalid:[...document.querySelectorAll(':invalid')].map(x=>({name:x.name,message:x.validationMessage})),toast:document.querySelector('#toast')?.textContent,errors:document.querySelector('#notice')?.textContent})));console.error('Browser errors',errors);throw e;}finally{await browser.close();db.close();}
