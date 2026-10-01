import {readFileSync,writeFileSync,mkdirSync,cpSync} from 'node:fs';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
const assets={html:readFileSync(path.join(root,'ui/index.html'),'utf8'),css:readFileSync(path.join(root,'ui/app.css'),'utf8'),js:readFileSync(path.join(root,'ui/app.js'),'utf8')};
writeFileSync(path.join(root,'worker/assets.js'),Object.entries(assets).map(([k,v])=>`export const ${k}=${JSON.stringify(v)};`).join('\n'));
mkdirSync(path.join(root,'dist/server'),{recursive:true});mkdirSync(path.join(root,'dist/.openai'),{recursive:true});cpSync(path.join(root,'worker'),path.join(root,'dist/server'),{recursive:true});cpSync(path.join(root,'.openai/hosting.json'),path.join(root,'dist/.openai/hosting.json'));
console.log('Worker built.');
