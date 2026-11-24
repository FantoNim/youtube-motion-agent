// Process-local safety wrapper for PINNED Remotion 4.0.538 only.
// Remotion's --host flag is not supported and default Studio listens on all interfaces.
// Override the shared internal port-config provider BEFORE loading Studio; no files/config are modified.
const {resolve} = require('node:path');
const {version} = require('@remotion/renderer/package.json');
if (version !== '4.0.538') throw new Error('Review loopback binding wrapper for this Remotion version before previewing');
const {RenderInternals} = require('@remotion/renderer');
if (typeof RenderInternals.getPortConfig !== 'function') throw new Error('Expected pinned getPortConfig API is unavailable');
RenderInternals.getPortConfig = () => ({host: '127.0.0.1', hostsToTry: ['127.0.0.1']});
if (process.argv.includes('--check-binding')) {
  const config = RenderInternals.getPortConfig(false);
  if (config.host !== '127.0.0.1' || config.hostsToTry.length !== 1) throw new Error('Loopback guard failed');
  console.log(JSON.stringify({version, ...config}));
} else {
  process.argv = [process.execPath, __filename, 'studio', resolve('src/index.ts'), '--port=3100', '--no-open', '--props=' + resolve('props.example.json')];
  console.log('Local-only Studio: forcing 127.0.0.1:3100 (Remotion ' + version + ')');
  require('@remotion/cli').cli().catch((error) => {console.error(error); process.exitCode = 1;});
}
