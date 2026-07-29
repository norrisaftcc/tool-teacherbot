// chat.js — streaming message handler

// marked stopped sanitizing at v5, and its output goes to innerHTML below,
// so raw HTML in a model response would execute — an <img onerror=…> quoted
// out of the corpus, or reflected back from something a student pasted in.
//
// The fix is a renderer override, not pre-escaping the input. Pre-escaping
// looks simpler and is wrong: marked then escapes the ampersands we just
// introduced, so `cout << "hi"` reaches the student as `cout &lt;&lt; "hi"`.
// That corrupts the stream operator in every C++ example this course
// serves, and it also eats blockquotes, because a leading `>` is markdown
// syntax. Measured against marked 18, not assumed.
//
// Overriding renderer.html leaves the parser alone — headings, emphasis,
// lists, links, tables, blockquotes and fenced code all render normally —
// and turns raw HTML into visible text, which is the honest outcome for a
// bot whose job is quoting course material.
//
// No DOMPurify: that would be another unpinned CDN script, which is the
// problem in #25, not the solution to it.
//
// Today the blast radius is mostly a student's own session. #29 (an admin
// transcript view) is what turns this into stored XSS against the
// instructor, so this lands before that does.
function escapeHtml(text) {
  return String(text)
    .replace(/&/g, '&amp;')   // first, or it double-escapes the others
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

// Set up once. `markedReady` stays false if the CDN script is missing or too
// old to accept the override — in which case we render plain text rather
// than piping unsanitized HTML into innerHTML. Degrading to unformatted
// output is a cosmetic loss; degrading to unsanitized output is not.
let markedReady = false;
try {
  if (typeof marked !== 'undefined' && typeof marked.use === 'function') {
    marked.use({
      renderer: {
        // Signature differs across marked majors — a string in v4 and
        // earlier, a token object from v5. The CDN tag is unpinned (#25),
        // so handle both rather than betting on which one loads.
        html(token) {
          return escapeHtml(typeof token === 'string' ? token : token.text);
        },
      },
    });
    markedReady = true;
  }
} catch (e) {
  markedReady = false;
}

const form = document.getElementById('chat-form');
const input = document.getElementById('message-input');
const log = document.getElementById('chat-log');
const typingEl = document.getElementById('typing-indicator');
const tokenEl = document.getElementById('tokens-remaining');
let history = [];

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  appendMessage('user', message);
  history.push({ role: 'user', content: message });
  input.value = '';
  input.disabled = true;

  // Create the bot bubble immediately so text streams into it
  const bubble = appendStreamingMessage();

  try {
    const res = await fetch(`/${window.SKIN_SLUG}/api/chat/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, history: history.slice(0, -1) }),
    });

    if (!res.ok) {
      const data = await res.json();
      bubble.textContent = data.error || 'Something went wrong.';
      bubble.closest('.msg').classList.add('msg--error');
    } else {
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let fullText = '';
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // keep incomplete line for next chunk

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          let event;
          try { event = JSON.parse(line.slice(6)); } catch { continue; }

          if (event.chunk) {
            fullText += event.chunk;
            bubble.textContent = fullText;  // plain text while streaming
            log.scrollTop = log.scrollHeight;
          } else if (event.error) {
            bubble.textContent = event.error;
            bubble.closest('.msg').classList.add('msg--error');
          } else if (event.done) {
            // Snap to rendered Markdown on completion.
            //
            // marked comes from a third-party CDN (chat.html). If that
            // request fails, `marked` is undefined and this line throws
            // inside the read loop — which the outer catch turns into
            // "Network error. Please try again." over an answer that
            // arrived intact, and skips the token-remaining update. Losing
            // Markdown formatting is a cosmetic degradation; losing the
            // answer to a misleading error is not.
            bubble.classList.remove('cursor');
            if (markedReady) {
              bubble.innerHTML = marked.parse(fullText);
            } else {
              bubble.textContent = fullText;
            }
            log.scrollTop = log.scrollHeight;
            history.push({ role: 'assistant', content: fullText });
            if (tokenEl && event.tokens_remaining !== null) {
              tokenEl.textContent = Number(event.tokens_remaining).toLocaleString();
            }
          }
        }
      }
    }
  } catch (err) {
    bubble.textContent = 'Network error. Please try again.';
    bubble.closest('.msg').classList.add('msg--error');
  } finally {
    input.disabled = false;
    input.focus();
    log.scrollTop = log.scrollHeight;
  }
});

function appendStreamingMessage() {
  const wrapper = document.createElement('div');
  wrapper.className = 'msg msg--bot';

  const avatar = document.createElement('div');
  avatar.className = 'msg__avatar';
  const svgTemplate = document.getElementById('bot-avatar-svg');
  if (svgTemplate) avatar.innerHTML = svgTemplate.innerHTML;
  wrapper.appendChild(avatar);

  const body = document.createElement('div');
  body.className = 'msg__body';

  const meta = document.createElement('div');
  meta.className = 'msg__meta';
  meta.textContent = 'TEACHERBOT';
  body.appendChild(meta);

  const bubble = document.createElement('div');
  bubble.className = 'msg__bubble cursor';  // .cursor adds blinking caret via kit.css
  body.appendChild(bubble);
  wrapper.appendChild(body);

  log.appendChild(wrapper);
  log.scrollTop = log.scrollHeight;
  return bubble;
}

function appendMessage(role, content) {
  const wrapper = document.createElement('div');
  wrapper.className = `msg msg--${role === 'user' ? 'user' : 'bot'}`;

  if (role !== 'user') {
    const avatar = document.createElement('div');
    avatar.className = 'msg__avatar';
    const svgTemplate = document.getElementById('bot-avatar-svg');
    if (svgTemplate) avatar.innerHTML = svgTemplate.innerHTML;
    wrapper.appendChild(avatar);
  }

  const body = document.createElement('div');
  body.className = 'msg__body';

  if (role !== 'user') {
    const meta = document.createElement('div');
    meta.className = 'msg__meta';
    meta.textContent = 'TEACHERBOT';
    body.appendChild(meta);
  }

  const bubble = document.createElement('div');
  bubble.className = 'msg__bubble';
  bubble.textContent = content;
  body.appendChild(bubble);

  if (role === 'user') {
    const avatar = document.createElement('div');
    avatar.className = 'msg__avatar';
    avatar.textContent = 'YOU';
    wrapper.appendChild(body);
    wrapper.appendChild(avatar);
  } else {
    wrapper.appendChild(body);
  }

  log.appendChild(wrapper);
  log.scrollTop = log.scrollHeight;
}
