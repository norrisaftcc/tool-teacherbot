// Exercises the real static/js/chat.js rendering path against marked.
//
// This exists because the obvious fix was wrong. Escaping the text before
// handing it to marked neutralises XSS and also double-escapes: marked
// escapes the ampersands the pre-escape introduced, so `cout << "hi"`
// reaches the student as `cout &lt;&lt; "hi"`. In a C++ course that corrupts
// the stream operator in every code sample, and it eats blockquotes too,
// because a leading `>` is markdown syntax. Both were measured, not
// reasoned about, which is the whole point of this file.
//
// It loads the VENDORED bundle, not the npm package. Those are different
// builds of the same version: `import { marked } from 'marked'` resolves the
// ESM entrypoint, while the browser executes static/js/marked.umd.js. Testing
// the one students do not run is a guarantee about the wrong artifact, so the
// UMD file is evaluated here exactly as a <script> tag would evaluate it.
// npm is still needed — `npm ci` is what makes the vendored file reproducible
// on upgrade — but it is no longer what this check exercises.
//
// Run: node system1-flask-chat/tests/js/render_check.mjs
// (see tests/test_chat_js_rendering.py, which skips when node is absent).

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';
import vm from 'vm';

const here = dirname(fileURLToPath(import.meta.url));
const STATIC_JS = resolve(here, '..', '..', 'static', 'js');
const CHAT_JS = resolve(STATIC_JS, 'chat.js');
const MARKED_UMD = resolve(STATIC_JS, 'marked.umd.js');

// chat.js talks to the DOM at import time. Give it just enough to run.
const stub = () => ({
  addEventListener() {}, appendChild() {}, focus() {},
  classList: { add() {}, remove() {}, contains: () => false },
  closest: () => stub(), style: {}, textContent: '', value: '',
  scrollTop: 0, scrollHeight: 0, innerHTML: '',
});

const ctx = {
  document: { getElementById: () => stub(), createElement: () => stub() },
  window: {}, console, fetch: async () => ({}), TextDecoder: class {},
};
vm.createContext(ctx);

// Evaluate the vendored UMD bundle first, the way the browser does. It has no
// module system to attach to in here, so it takes its global branch and
// defines `marked` on the sandbox — the same object chat.js will find.
vm.runInContext(readFileSync(MARKED_UMD, 'utf8'), ctx);
if (typeof ctx.marked === 'undefined') {
  console.error('FAIL static/js/marked.umd.js did not define a global `marked`');
  process.exit(1);
}
// `markedReady` is a `let`, so it never becomes a property of the sandbox
// global — hoist it deliberately rather than reading undefined and calling
// that a pass.
vm.runInContext(readFileSync(CHAT_JS, 'utf8') + '\n;globalThis.__ready = markedReady;', ctx);

const fail = (msg) => { console.error(`FAIL ${msg}`); process.exitCode = 1; };

if (ctx.__ready !== true) {
  fail('markedReady is not true — chat.js would silently fall back to plain text');
  process.exit(1);
}

const render = (s) => ctx.marked.parse(s);

// ---- raw HTML must never survive into the output -------------------------

const PAYLOADS = [
  '<img src=x onerror="alert(1)">',
  '<script>alert(1)</script>',
  'inline <img src=x onerror=alert(1)> mid-sentence',
  '<iframe src="evil"></iframe>',
  '<svg/onload=alert(1)>',
  '<div onclick="alert(1)">hi</div>',
  '<a href="javascript:alert(1)">click</a>',
  '<style>body{display:none}</style>',
];

for (const payload of PAYLOADS) {
  const out = render(payload);
  // marked legitimately emits <p>, <code>, <pre> etc. Only these tags could
  // have come from the payload itself.
  if (/<(img|script|iframe|svg|div|style|a|object|embed|form)\b/i.test(out)) {
    fail(`live HTML survived: ${payload}\n     -> ${out.trim()}`);
  }
}

// ---- and the course's own content must still render ----------------------

const cpp = render('```cpp\ncout << "Hello" << endl;\nif (a < b && b > c) {}\n```');
if (!cpp.includes('&lt;&lt;')) {
  fail(`C++ stream operator lost:\n     ${cpp.trim()}`);
}
if (cpp.includes('&amp;lt;')) {
  fail(`C++ code double-escaped — students would see literal &lt;&lt;:\n     ${cpp.trim()}`);
}

const EXPECTED = [
  ['blockquote', '> paste the error message', '<blockquote>'],
  ['heading', '## Opening your Codespace', '<h2>'],
  ['bold', 'You need **cout** here', '<strong>'],
  ['inline code', 'use `cin >> x;`', '<code>'],
  ['list', '- step one\n- step two', '<li>'],
  ['link', '[walkthrough](https://example.com)', 'href="https://example.com"'],
  ['table', '| a | b |\n|---|---|\n| 1 | 2 |', '<table>'],
];

for (const [name, src, needle] of EXPECTED) {
  const out = render(src);
  if (!out.includes(needle)) {
    fail(`${name} stopped rendering (expected ${needle}):\n     ${out.trim()}`);
  }
}

if (!process.exitCode) {
  console.log(`ok — ${PAYLOADS.length} payloads neutralised, ` +
              `${EXPECTED.length + 1} content cases render`);
}
