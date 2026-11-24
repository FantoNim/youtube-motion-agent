// A deterministic LOCAL 4s low-level test tone; NOT speech/music/TTS.
// Writes ONLY the dedicated public/audio-fixture.wav. No media uploads or dependencies.
import {writeFileSync, mkdirSync} from 'node:fs';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const sampleRate = 48000, seconds = 4, count = sampleRate * seconds;
const out = Buffer.alloc(44 + count * 2);
out.write('RIFF', 0); out.writeUInt32LE(36 + count * 2, 4); out.write('WAVE', 8); out.write('fmt ', 12); out.writeUInt32LE(16, 16); out.writeUInt16LE(1, 20); out.writeUInt16LE(1, 22); out.writeUInt32LE(sampleRate, 24); out.writeUInt32LE(sampleRate * 2, 28); out.writeUInt16LE(2, 32); out.writeUInt16LE(16, 34); out.write('data', 36); out.writeUInt32LE(count * 2, 40);
for (let i = 0; i < count; i++) {
  const t = i / sampleRate;
  const envelope = Math.min(1, t / 0.05, (seconds - t) / 0.08);
  const pulse = 0.78 + 0.22 * Math.cos(2 * Math.PI * 2 * t);
  const s = (Math.sin(2 * Math.PI * 220 * t) + 0.35 * Math.sin(2 * Math.PI * 330 * t)) * 0.12 * envelope * pulse;
  out.writeInt16LE(Math.round(s * 32767), 44 + i * 2);
}
mkdirSync(resolve(root, 'public'), {recursive: true});
const path = resolve(root, 'public/audio-fixture.wav');
writeFileSync(path, out);
console.log(path + ' (4s, 48kHz mono PCM, synthetic test fixture only)');
