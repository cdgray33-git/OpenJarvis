import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const configPath = path.resolve(__dirname, '../src-tauri/tauri.conf.json');
const cachebuster = Date.now();

let config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

// 1. Clean frontendDist
if (config.build?.frontendDist?.includes('?')) {
  config.build.frontendDist = config.build.frontendDist.split('?')[0];
}

// 2. Set window url with cachebuster (first window)
// FIX: Set path relative to frontendDist directory rather than physical source paths
if (config.app?.windows?.[0]) {
  config.app.windows[0].url = `index.html?cachebuster=${cachebuster}`;
}

// 3. Remove timestampUrl if present
if (config.bundle?.windows?.timestampUrl) {
  delete config.bundle.windows.timestampUrl;
}

fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
console.log(`Cachebuster injected into window.url: ${cachebuster}`);
console.log(`frontendDist cleaned`);
