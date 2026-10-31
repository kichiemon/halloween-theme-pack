#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');

const SKILL_NAME = 'halloween-theme-pack';
const HOME = os.homedir();

// Support multiple agent skill directories
const skillDirs = [
  path.join(HOME, '.claude', 'skills', SKILL_NAME),
  path.join(HOME, '.agents', 'skills', SKILL_NAME),
  path.join(HOME, '.cursor', 'skills', SKILL_NAME),
];

const srcSkill = path.join(__dirname, '..', 'SKILL.md');
const srcBin = path.join(__dirname, 'halloween-gen');

if (!fs.existsSync(srcSkill)) {
  console.error('SKILL.md not found in package. Installation failed.');
  process.exit(1);
}

let installed = 0;
for (const dir of skillDirs) {
  try {
    fs.mkdirSync(dir, { recursive: true });
    fs.copyFileSync(srcSkill, path.join(dir, 'SKILL.md'));
    // Also copy generate.py, validate.py, and bin for runtime use
    const scriptsDir = path.join(dir, 'scripts');
    fs.mkdirSync(scriptsDir, { recursive: true });
    const repoRoot = path.join(__dirname, '..');
    for (const f of ['generate.py', 'validate.py']) {
      const src = path.join(repoRoot, f);
      if (fs.existsSync(src)) fs.copyFileSync(src, path.join(dir, f));
    }
    console.log(`✓ Installed skill to ${dir}`);
    installed++;
  } catch (e) {
    // Directory may not be writable or parent doesn't exist; skip
  }
}

if (installed === 0) {
  // Fallback: install to ~/.claude/skills/ only
  const fallback = path.join(HOME, '.claude', 'skills', SKILL_NAME);
  fs.mkdirSync(fallback, { recursive: true });
  fs.copyFileSync(srcSkill, path.join(fallback, 'SKILL.md'));
  console.log(`✓ Installed skill to ${fallback}`);
  installed = 1;
}

console.log('');
console.log('🎃 Halloween Theme Pack skill installed!');
console.log('');
console.log('Your AI agent (Claude Code, Cursor, Codex, etc.) will now recognize');
console.log('the skill and can apply Halloween themes when you ask.');
console.log('');
console.log('Try: "Apply a Halloween theme to my terminal"');
console.log('');
console.log('Manual usage:');
console.log('  halloween-gen              # generate all theme files');
console.log('  halloween-gen apply        # auto-detect and apply');
console.log('  halloween-gen install      # interactive installer');
console.log('');

// Make binary executable if present
if (fs.existsSync(srcBin)) {
  try { fs.chmodSync(srcBin, 0o755); } catch (e) {}
}
