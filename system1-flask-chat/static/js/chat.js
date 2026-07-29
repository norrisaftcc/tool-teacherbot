// chat.js — streaming message handler
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
            if (typeof marked !== 'undefined' && marked.parse) {
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
