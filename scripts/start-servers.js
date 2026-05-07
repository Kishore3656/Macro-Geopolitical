/**
 * Startup script to start both FastAPI backend and Next.js frontend
 * for Playwright testing
 */
const { spawn } = require('child_process');
const path = require('path');

const projectRoot = __dirname;

console.log('Starting servers for Playwright testing...');

// Start FastAPI backend
console.log('Starting FastAPI backend on port 8000...');
const backend = spawn('python', ['-m', 'uvicorn', 'api.main:app', '--reload', '--host', '0.0.0.0', '--port', '8000'], {
  cwd: projectRoot,
  stdio: 'inherit',
});

// Start Next.js frontend
console.log('Starting Next.js frontend on port 3000...');
const frontend = spawn('npm', ['run', 'dev'], {
  cwd: path.join(projectRoot, 'frontend'),
  stdio: 'inherit',
});

// Handle process termination
process.on('exit', () => {
  backend.kill();
  frontend.kill();
});

backend.on('error', (err) => {
  console.error('Backend error:', err);
});

frontend.on('error', (err) => {
  console.error('Frontend error:', err);
});
