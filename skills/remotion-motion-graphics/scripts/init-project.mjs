// MIT; adapted skill copyright (c) 2025 haidrrrry. No network or install actions.
import {cpSync, existsSync, mkdirSync, readdirSync, lstatSync} from 'node:fs';
import {resolve, dirname, join, relative, isAbsolute, sep} from 'node:path';
import {fileURLToPath} from 'node:url';
const here = dirname(fileURLToPath(import.meta.url));
export function createProject(destination) {
  if (!destination) throw new Error('Usage: node init-project.mjs <new-project-directory>');
  const target = resolve(destination);
  if (existsSync(target)) {
    if (lstatSync(target).isSymbolicLink() || !lstatSync(target).isDirectory()) throw new Error('Destination must be a real directory');
    if (readdirSync(target).length) throw new Error('Refusing to overwrite a nonempty project: ' + target);
  }
  const template = resolve(here, '../assets/template');
  const withinSkill = relative(resolve(here, '..'), target);
  if (withinSkill === '' || (!withinSkill.startsWith('..' + sep) && withinSkill !== '..' && !isAbsolute(withinSkill))) throw new Error('Choose a project outside the skill');
  mkdirSync(target, {recursive: true});
  for (const name of readdirSync(template)) cpSync(join(template, name), join(target, name), {recursive: true, force: false, errorOnExist: true});
  cpSync(resolve(here, '../LICENSE'), join(target, 'LICENSE'), {force: false, errorOnExist: true});
  for (const sub of ['assets/originals', 'public', 'exports', 'proof', 'notes']) mkdirSync(join(target, sub), {recursive: true});
  return target;
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { console.log(createProject(process.argv[2])); }
  catch (error) { console.error(error.message); process.exitCode = 1; }
}
