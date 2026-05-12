/* system1/doc-panel.jsx — bottom (or side) split with tabs, code highlight, markdown, presence */

// ---------- Simple syntax highlighter ---------------------------------------
const PY_KW = new Set(['def','return','from','import','as','if','elif','else','for','while','in','not','and','or','True','False','None','class','pass','try','except','finally','with','lambda','yield','raise','break','continue','global','nonlocal','is']);
const JS_KW = new Set(['const','let','var','function','return','if','else','for','while','do','switch','case','break','continue','class','extends','new','import','export','from','default','async','await','try','catch','finally','throw','typeof','instanceof','of','in','this','null','undefined','true','false']);

function highlight(src, lang) {
  const kw = lang === 'py' ? PY_KW : lang === 'js' || lang === 'jsx' ? JS_KW : null;
  if (!kw) return escapeHtml(src);

  const lines = src.split('\n');
  return lines.map(line => {
    // comments first — split at # or //
    const cmtPattern = lang === 'py' ? /(#.*)$/ : /(\/\/.*)$/;
    const cmtMatch = line.match(cmtPattern);
    let codePart = line, cmtPart = '';
    if (cmtMatch) {
      codePart = line.slice(0, cmtMatch.index);
      cmtPart = '<span class="tok-cmt">' + escapeHtml(cmtMatch[0]) + '</span>';
    }

    // tokenize codePart: strings, numbers, keywords, decorators, function calls
    let out = '';
    let i = 0;
    while (i < codePart.length) {
      const ch = codePart[i];
      // string
      if (ch === '"' || ch === "'") {
        let j = i + 1;
        while (j < codePart.length && codePart[j] !== ch) {
          if (codePart[j] === '\\') j++;
          j++;
        }
        const s = codePart.slice(i, Math.min(j + 1, codePart.length));
        out += '<span class="tok-str">' + escapeHtml(s) + '</span>';
        i = j + 1;
        continue;
      }
      // decorator (python)
      if (ch === '@' && lang === 'py' && (i === 0 || /\s/.test(codePart[i-1]))) {
        let j = i + 1;
        while (j < codePart.length && /[\w.]/.test(codePart[j])) j++;
        out += '<span class="tok-deco">' + escapeHtml(codePart.slice(i, j)) + '</span>';
        i = j;
        continue;
      }
      // number
      if (/[0-9]/.test(ch) && (i === 0 || !/[A-Za-z_]/.test(codePart[i-1]))) {
        let j = i;
        while (j < codePart.length && /[0-9.]/.test(codePart[j])) j++;
        out += '<span class="tok-num">' + escapeHtml(codePart.slice(i, j)) + '</span>';
        i = j;
        continue;
      }
      // identifier
      if (/[A-Za-z_]/.test(ch)) {
        let j = i;
        while (j < codePart.length && /[A-Za-z0-9_]/.test(codePart[j])) j++;
        const word = codePart.slice(i, j);
        const nextCh = codePart[j];
        if (kw.has(word)) {
          out += '<span class="tok-kw">' + escapeHtml(word) + '</span>';
        } else if (nextCh === '(') {
          out += '<span class="tok-fn">' + escapeHtml(word) + '</span>';
        } else {
          out += escapeHtml(word);
        }
        i = j;
        continue;
      }
      out += escapeHtml(ch);
      i++;
    }
    return out + cmtPart;
  }).join('\n');
}

function escapeHtml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// ---------- markdown renderer (tiny) ---------------------------------------
function renderMd(src) {
  const esc = (s) => escapeHtml(s).replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/\*([^*]+)\*/g, '<em>$1</em>');
  const lines = src.split('\n');
  let html = '';
  let inList = null;
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    const h = l.match(/^(#{1,3})\s+(.*)$/);
    const ul = l.match(/^[-*]\s+(.*)$/);
    const ol = l.match(/^(\d+)\.\s+(.*)$/);
    if (h) {
      if (inList) { html += `</${inList}>`; inList = null; }
      const lvl = h[1].length;
      html += `<h${lvl}>${esc(h[2])}</h${lvl}>`;
    } else if (ul) {
      if (inList !== 'ul') { if (inList) html += `</${inList}>`; html += '<ul>'; inList = 'ul'; }
      html += `<li>${esc(ul[1])}</li>`;
    } else if (ol) {
      if (inList !== 'ol') { if (inList) html += `</${inList}>`; html += '<ol>'; inList = 'ol'; }
      html += `<li>${esc(ol[2])}</li>`;
    } else if (l.trim() === '---') {
      if (inList) { html += `</${inList}>`; inList = null; }
      html += '<hr>';
    } else if (l.trim() === '') {
      if (inList) { html += `</${inList}>`; inList = null; }
    } else {
      if (inList) { html += `</${inList}>`; inList = null; }
      html += `<p>${esc(l)}</p>`;
    }
  }
  if (inList) html += `</${inList}>`;
  return html;
}

// ---------- doc viewer body ------------------------------------------------
const CodeView = ({ doc, editingLine, caretCol }) => {
  const lang = (doc.name.match(/\.([a-z]+)$/) || [])[1] || 'txt';
  const langKey = (lang === 'py' ? 'py' : (lang === 'js' || lang === 'jsx' || lang === 'ts' || lang === 'tsx') ? 'js' : null);
  const lines = doc.content.split('\n');
  const highlighted = highlight(doc.content, langKey);
  const hlLines = highlighted.split('\n');

  return (
    <div className="doc-code">
      <div className="doc-code__gutter">
        {lines.map((_, i) => <span key={i}>{i + 1}</span>)}
      </div>
      <div className="doc-code__src">
        {hlLines.map((html, i) => {
          const isEditing = editingLine === i + 1;
          return (
            <div
              key={i}
              className={isEditing ? 'editing-line' : ''}
              style={{ minHeight: '1.55em', position: 'relative' }}
            >
              <span dangerouslySetInnerHTML={{ __html: html || '&nbsp;' }} />
              {isEditing && caretCol != null && <span className="fake-caret" />}
            </div>
          );
        })}
      </div>
    </div>
  );
};

const MdView = ({ doc }) => (
  <div className="doc-md" dangerouslySetInnerHTML={{ __html: renderMd(doc.content) }} />
);

// ---------- panel chrome ---------------------------------------------------
const DocTab = ({ doc, active, dirty, onSelect, onClose }) => (
  <div
    className={'doc-tab' + (active ? ' doc-tab--active' : '') + (dirty ? ' doc-tab--dirty' : '')}
    onClick={onSelect}
  >
    <span className="doc-tab__icon">{doc.type === 'md' ? '▤' : '▣'}</span>
    <span className="doc-tab__name">{doc.name}</span>
    <button
      className="doc-tab__close"
      onClick={(e) => { e.stopPropagation(); onClose(); }}
      title="Close"
    >×</button>
  </div>
);

const DocPanel = ({
  docs, activeId, onSelectDoc, onCloseDoc,
  collapsed, onToggleCollapsed,
  presence, layout, onToggleLayout, height, onResize,
}) => {
  const active = docs.find(d => d.id === activeId);
  const resizeRef = React.useRef();

  // drag-to-resize (only when bottom-stacked)
  React.useEffect(() => {
    if (layout !== 'stacked') return;
    const handle = resizeRef.current;
    if (!handle) return;
    let startY = 0; let startH = 0; let dragging = false;
    const onDown = (e) => { dragging = true; startY = e.clientY; startH = height; e.preventDefault(); };
    const onMove = (e) => {
      if (!dragging) return;
      const delta = startY - e.clientY;
      onResize(Math.max(140, Math.min(700, startH + delta)));
    };
    const onUp = () => { dragging = false; };
    handle.addEventListener('mousedown', onDown);
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
    return () => {
      handle.removeEventListener('mousedown', onDown);
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', onUp);
    };
  }, [layout, height, onResize]);

  const empty = docs.length === 0;

  const style = layout === 'stacked'
    ? { height: collapsed ? 38 : `min(${height}px, 55vh)` }
    : { width: collapsed ? 38 : 480, height: '100%', flex: '0 0 auto' };

  return (
    <section
      className={'docpanel' + (collapsed ? ' docpanel--collapsed' : '')}
      style={style}
    >
      {layout === 'stacked' && !collapsed && (
        <div className="docpanel__resize" ref={resizeRef} title="Drag to resize" />
      )}

      <div className="docpanel__bar">
        <div className="docpanel__label">
          <span className="ascii">[</span>
          SIDE FRAME
          <span className="ascii">]</span>
          <span style={{ color: 'var(--cream-muted)', fontWeight: 400, marginLeft: 4 }}>
            ({docs.length} doc{docs.length === 1 ? '' : 's'})
          </span>
        </div>
        {!collapsed && (
          <div className="docpanel__tabs">
            {docs.map(d => (
              <DocTab
                key={d.id}
                doc={d}
                active={d.id === activeId}
                dirty={d.dirty}
                onSelect={() => onSelectDoc(d.id)}
                onClose={() => onCloseDoc(d.id)}
              />
            ))}
          </div>
        )}
        <div className="docpanel__actions">
          <button
            className="docpanel__action"
            onClick={onToggleLayout}
            title={layout === 'stacked' ? 'Switch to side-by-side' : 'Switch to bottom split'}
          >
            {layout === 'stacked' ? '⎵ STACK' : '▭▭ SPLIT'}
          </button>
          <button
            className="docpanel__action docpanel__action--toggle"
            onClick={onToggleCollapsed}
            title={collapsed ? 'Expand' : 'Collapse'}
          >
            {collapsed ? '▴' : '▾'}
          </button>
        </div>
      </div>

      {!collapsed && presence && active && (
        <div className="presence-row">
          <span className="presence-row__dot" />
          TEACHERBOT IS EDITING <span style={{ color: 'var(--cream)', fontWeight: 700, marginLeft: 6 }}>{active.name}</span>
          <span style={{ marginLeft: 'auto', color: 'var(--cream-muted)' }}>
            LINE {presence.line || 1} · CO-CURSOR ACTIVE
          </span>
        </div>
      )}

      {!collapsed && (
        <div className="docpanel__body">
          {empty ? (
            <div className="docpanel__empty">
              <pre>{`╔══════════════════════════════╗
║   N O   A R T I F A C T S    ║
║   ─────────────────────────  ║
║   attach a file, or ask the  ║
║   bot to draft one for you   ║
╚══════════════════════════════╝`}</pre>
              <div>Side frame is empty. Paperclip ▸ or paste &gt;6 lines to open a doc here.</div>
            </div>
          ) : !active ? null : active.type === 'md' ? (
            <MdView doc={active} />
          ) : (
            <CodeView doc={active} editingLine={presence?.line} caretCol={presence?.col} />
          )}
        </div>
      )}
    </section>
  );
};

Object.assign(window, { DocPanel, CodeView, MdView });
