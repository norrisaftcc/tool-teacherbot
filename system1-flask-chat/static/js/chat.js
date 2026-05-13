(function () {
  const form = document.getElementById('chat-form');
  const input = document.getElementById('message-input');
  const log = document.getElementById('chat-log');
  const status = document.getElementById('status-pill');
  const sendBtn = form.querySelector('.composer__send');

  const history = [];

  function appendMessage(role, content) {
    const wrap = document.createElement('div');
    wrap.className = 'msg msg--' + (role === 'assistant' ? 'bot' : role === 'error' ? 'instructor' : 'user');

    const body = document.createElement('div');
    body.className = 'msg__body';

    const meta = document.createElement('div');
    meta.className = 'msg__meta';
    const stamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    if (role === 'assistant') {
      meta.textContent = 'TEACHERBOT · ' + stamp;
    } else if (role === 'error') {
      meta.textContent = 'SYSTEM · ' + stamp;
    } else {
      meta.textContent = (window.TEACHERBOT_GROUP || 'OPERATIVE').toUpperCase() + ' · ' + stamp;
    }

    const bubble = document.createElement('div');
    bubble.className = 'msg__bubble';
    bubble.textContent = content;

    body.appendChild(meta);
    body.appendChild(bubble);
    wrap.appendChild(body);
    log.appendChild(wrap);
    log.scrollTop = log.scrollHeight;
  }

  function setStatus(state) {
    if (!status) return;
    status.className = 'pill pill--' + state;
    status.innerHTML = '<span class="pill__dot"></span>' +
      (state === 'streaming' ? 'STREAMING' : state === 'offline' ? 'ERROR' : 'READY');
  }

  function setRemaining(tokens) {
    const el = document.getElementById('tokens-remaining');
    if (el && tokens !== null && tokens !== undefined) {
      el.textContent = tokens.toLocaleString();
    }
  }

  async function send(message) {
    appendMessage('user', message);
    history.push({ role: 'user', content: message });
    input.value = '';
    input.style.height = 'auto';
    input.disabled = true;
    sendBtn.disabled = true;
    setStatus('streaming');

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message, history: history.slice(0, -1) }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        appendMessage('error', data.error || ('HTTP ' + res.status));
        setStatus('offline');
      } else {
        appendMessage('assistant', data.response);
        history.push({ role: 'assistant', content: data.response });
        setRemaining(data.tokens_remaining);
        setStatus('online');
      }
    } catch (err) {
      appendMessage('error', 'Network error: ' + err.message);
      setStatus('offline');
    } finally {
      input.disabled = false;
      sendBtn.disabled = false;
      input.focus();
    }
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const m = input.value.trim();
    if (m) send(m);
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      form.requestSubmit();
    }
  });

  input.addEventListener('input', (e) => {
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 140) + 'px';
  });
})();
