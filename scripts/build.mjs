import {readFile,mkdir,writeFile,copyFile} from 'node:fs/promises';
await mkdir('dist/server',{recursive:true});await mkdir('dist/.openai',{recursive:true});
const source=await readFile('server/index.js','utf8');
const tools=JSON.parse(await readFile('server/tools.json','utf8'));
await writeFile('dist/server/index.js',source.replace("import coreTools from './tools.json' with {type:'json'};",'const coreTools='+JSON.stringify(tools)+';'));
await copyFile('.openai/hosting.json','dist/.openai/hosting.json');
console.log('Built standalone Worker ESM.');
