import {DatabaseSync} from 'node:sqlite';
import {readFileSync} from 'node:fs';
export function database(filename){const db=new DatabaseSync(filename);db.exec(readFileSync(new URL('../db/local-schema.sql',import.meta.url),'utf8'));return {db,binding:{prepare(sql){return {bind(...args){return {async all(){return {results:db.prepare(sql).all(...args)};},async first(){return db.prepare(sql).get(...args)||null;},async run(){const r=db.prepare(sql).run(...args);return {meta:{changes:r.changes}};}};}};}}};}
