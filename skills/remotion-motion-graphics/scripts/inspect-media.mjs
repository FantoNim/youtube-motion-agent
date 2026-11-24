// Local metadata only; invokes ffprobe with an argument array, never a shell.
import {spawnSync} from 'node:child_process';
import {statSync} from 'node:fs';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const number = (v) => v !== undefined && Number.isFinite(Number(v)) ? Number(v) : null;
export function inspectMedia(input, ffprobe = process.env.FFPROBE_PATH || 'ffprobe') {
  if (!input) throw new Error('Usage: node inspect-media.mjs <local-media-file> [ffprobe-executable]');
  const path = resolve(input);
  if (!statSync(path).isFile()) throw new Error('Media input is not a file: ' + path);
  const p = spawnSync(ffprobe, ['-v', 'error', '-show_format', '-show_streams', '-of', 'json', path], {encoding: 'utf8', timeout: 60000, maxBuffer: 8 * 1024 * 1024, windowsHide: true});
  if (p.error) throw new Error('ffprobe could not run: ' + p.error.message);
  if (p.status !== 0) throw new Error('ffprobe failed: ' + p.stderr.trim());
  const raw = JSON.parse(p.stdout);
  const streams = (raw.streams || []).map((s) => ({index: s.index, type: s.codec_type, codec: s.codec_name, startSeconds: number(s.start_time), durationSeconds: number(s.duration), width: s.width, height: s.height, fps: s.avg_frame_rate || s.r_frame_rate, sampleRate: number(s.sample_rate), channels: s.channels, frames: number(s.nb_frames)}));
  if (!streams.length) throw new Error('No streams found');
  return {path, format: raw.format?.format_name, durationSeconds: number(raw.format?.duration), startSeconds: number(raw.format?.start_time), bytes: number(raw.format?.size), hasAudio: streams.some((s) => s.type === 'audio'), streams, note: 'Use actual selected stream duration/offset; null means unavailable, never an estimated value.'};
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { console.log(JSON.stringify(inspectMedia(process.argv[2], process.argv[3]), null, 2)); }
  catch (error) { console.error(error.message); process.exitCode = 1; }
}
