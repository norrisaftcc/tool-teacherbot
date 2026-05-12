// chat.js — handles message send/receive without page reload
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
  if (typingEl) typingEl.style.display = 'flex';

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, history: history.slice(0, -1) }),
    });
    const data = await res.json();

    if (!res.ok) {
      appendMessage('error', data.error || 'Something went wrong.');
    } else {
      appendMessage('assistant', data.response);
      history.push({ role: 'assistant', content: data.response });
      if (tokenEl && data.tokens_remaining !== null) {
        tokenEl.textContent = Number(data.tokens_remaining).toLocaleString();
      }
    }
  } catch (err) {
    appendMessage('error', 'Network error. Please try again.');
  } finally {
    input.disabled = false;
    input.focus();
    if (typingEl) typingEl.style.display = 'none';
  }
});

function appendMessage(role, content) {
  const wrapper = document.createElement('div');
  wrapper.className = `msg msg--${role === 'user' ? 'user' : role === 'error' ? 'error' : 'bot'}`;

  if (role !== 'user') {
    const avatar = document.createElement('div');
    avatar.className = 'msg__avatar';
    // SVG brand mark for bot
    if (role === 'assistant') {
      avatar.innerHTML = document.getElementById('bot-avatar-svg').innerHTML;
    } else {
      avatar.textContent = '!';
    }
    wrapper.appendChild(avatar);
  }

  const body = document.createElement('div');
  body.className = 'msg__body';

  if (role !== 'user') {
    const meta = document.createElement('div');
    meta.className = 'msg__meta';
    meta.textContent = role === 'assistant' ? 'TEACHERBOT' : 'ERROR';
    body.appendChild(meta);
  }

  const bubble = document.createElement('div');
  bubble.className = 'msg__bubble';
  bubble.textContent = content;  // textContent prevents XSS
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
