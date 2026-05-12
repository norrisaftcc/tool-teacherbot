/* system1/app.jsx — top-level state + orchestration */

const stamp = () => {
  const d = new Date();
  return String(d.getHours()).padStart(2, '0') + ':' +
         String(d.getMinutes()).padStart(2, '0') + ':' +
         String(d.getSeconds()).padStart(2, '0');
};
const mkId = () => Math.random().toString(36).slice(2, 9);

// ----- which canned reply for which user prompt
const replyKeyFor = (text, hasAttach) => {
  const t = text.toLowerCase();
  if (hasAttach) return 'attach';
  if (/(sprint|plan)/.test(t)) return 'sprint';
  if (/(draft|write|generate).*(markdown|spec|readme|doc)/.test(t)) return 'draft';
  if (/(404|route)/.test(t)) return '404';
  if (/(flask|session)/.test(t)) return 'flask';
  if (/(sqlite|postgres|database)/.test(t)) return 'sqlite';
  if (/(review|pr|pull request)/.test(t)) return 'review';
  return 'default';
};

// reply might produce an artifact in the side frame
const artifactFor = (replyKey) => {
  if (replyKey === 'attach') {
    return { id: 'd_wsgi_new', name: 'wsgi.py (proposed)', type: 'py', author: 'bot' };
  }
  if (replyKey === 'sprint' || replyKey === 'draft') {
    return { id: 'd_sprint_md', name: 'sprint-plan.md', type: 'md', author: 'bot' };
  }
  return null;
};

// =============================================================================
// MAIN APP
// =============================================================================
const App = () => {
  // ---- which group is active
  const [activeGroupId, setActiveGroupId] = React.useState('g2');

  // ---- role: student vs instructor (toggle)
  const [role, setRole] = React.useState('student');

  // ---- per-group chat state, keyed by group id
  const [chatsByGroup, setChatsByGroup] = React.useState(() => {
    const map = {};
    for (const g of GROUPS) {
      const seed = SEED_BY_GROUP[g.id];
      map[g.id] = seed
        ? { messages: seed.messages.slice() }
        : { messages: [] };
    }
    return map;
  });

  // ---- open documents (tabs in side frame) per group
  const [docsByGroup, setDocsByGroup] = React.useState(() => {
    const map = {};
    for (const g of GROUPS) {
      if (g.id === 'g2') {
        map[g.id] = {
          openDocs: [SEED_DOCS.d_wsgi_old, SEED_DOCS.d_wsgi_new],
          activeDocId: 'd_wsgi_new',
        };
      } else if (g.id === 'g5') {
        map[g.id] = {
          openDocs: [SEED_DOCS.d_sprint_md],
          activeDocId: 'd_sprint_md',
        };
      } else {
        map[g.id] = { openDocs: [], activeDocId: null };
      }
    }
    return map;
  });

  // ---- pending attachments in the composer
  const [pendingAttachments, setPendingAttachments] = React.useState([]);
  React.useEffect(() => { setPendingAttachments([]); }, [activeGroupId]);

  // ---- streaming state
  const [streaming, setStreaming] = React.useState(false);

  // ---- doc-panel UI state
  const [docPanelCollapsed, setDocPanelCollapsed] = React.useState(false);
  const [docPanelHeight, setDocPanelHeight] = React.useState(300);
  const [docLayout, setDocLayout] = React.useState('stacked'); // or 'side'

  // ---- presence (TEACHERBOT IS EDITING…)
  const [presence, setPresence] = React.useState(null);
  // ---- tweaks
  const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
    "showPoster": true,
    "showPresence": true,
    "docLayout": "stacked",
    "showBanner": true
  }/*EDITMODE-END*/;
  const [tweaks, setTweak] = window.useTweaks(TWEAK_DEFAULTS);

  React.useEffect(() => { setDocLayout(tweaks.docLayout); }, [tweaks.docLayout]);

  // ---- clock
  const [sessionTime, setSessionTime] = React.useState(stamp());
  React.useEffect(() => {
    const id = setInterval(() => setSessionTime(stamp()), 1000);
    return () => clearInterval(id);
  }, []);

  // ---- derived ---------------------------------------------------------------
  const activeGroup = GROUPS.find(g => g.id === activeGroupId);
  const chat = chatsByGroup[activeGroupId];
  const docState = docsByGroup[activeGroupId];

  const totalTokens = role === 'instructor'
    ? GROUPS.reduce((acc, g) => ({ used: acc.used + g.tokens.used, cap: acc.cap + g.tokens.cap }), { used: 0, cap: 0 })
    : activeGroup.tokens;

  // ---- helpers ---------------------------------------------------------------
  const updateChat = (groupId, mut) => {
    setChatsByGroup(prev => ({ ...prev, [groupId]: mut(prev[groupId]) }));
  };
  const updateDocs = (groupId, mut) => {
    setDocsByGroup(prev => ({ ...prev, [groupId]: mut(prev[groupId]) }));
  };

  const openDoc = (docId) => {
    const doc = SEED_DOCS[docId];
    if (!doc) return;
    updateDocs(activeGroupId, st => {
      if (st.openDocs.find(d => d.id === docId)) return { ...st, activeDocId: docId };
      return { openDocs: [...st.openDocs, doc], activeDocId: docId };
    });
    setDocPanelCollapsed(false);
  };

  const closeDoc = (docId) => {
    updateDocs(activeGroupId, st => {
      const filtered = st.openDocs.filter(d => d.id !== docId);
      const newActive = st.activeDocId === docId
        ? (filtered[0]?.id ?? null)
        : st.activeDocId;
      return { openDocs: filtered, activeDocId: newActive };
    });
  };

  const selectDoc = (docId) => {
    updateDocs(activeGroupId, st => ({ ...st, activeDocId: docId }));
  };

  // ----- attaching from composer paperclip ----------------------------------
  const onAttach = () => {
    // Simulate file picker — attach a starter doc
    const newDoc = {
      ...STARTER_DOC,
      id: 'doc_' + mkId(),
      name: pendingAttachments.length === 0 ? 'auth.py' : `attached-${pendingAttachments.length + 1}.py`,
    };
    SEED_DOCS[newDoc.id] = newDoc;
    setPendingAttachments(prev => [...prev, newDoc]);
    // also open in side frame as preview
    updateDocs(activeGroupId, st => ({
      openDocs: [...st.openDocs.filter(d => d.id !== newDoc.id), newDoc],
      activeDocId: newDoc.id,
    }));
    setDocPanelCollapsed(false);
  };

  const onRemoveAttach = (docId) => {
    setPendingAttachments(prev => prev.filter(a => a.id !== docId));
  };

  // ----- paste-to-doc -------------------------------------------------------
  const onPasteCode = (text) => {
    const newDoc = {
      id: 'doc_' + mkId(),
      name: 'pasted-' + new Date().toTimeString().slice(0, 5).replace(':', '') + '.py',
      type: 'py',
      author: 'user',
      content: text,
    };
    SEED_DOCS[newDoc.id] = newDoc;
    setPendingAttachments(prev => [...prev, newDoc]);
    updateDocs(activeGroupId, st => ({
      openDocs: [...st.openDocs, newDoc],
      activeDocId: newDoc.id,
    }));
    setDocPanelCollapsed(false);
  };

  // ----- send a message -----------------------------------------------------
  const handleSend = (text) => {
    const userMsg = {
      id: mkId(),
      role: role === 'instructor' ? 'instructor' : 'user',
      authorName: role === 'instructor' ? 'INSTRUCTOR · TA' : null,
      text: text || (pendingAttachments.length ? '(attached for review)' : ''),
      time: stamp(),
      attachment: pendingAttachments[0] || null,
    };

    const hadAttach = pendingAttachments.length > 0;
    updateChat(activeGroupId, st => ({ messages: [...st.messages, userMsg] }));
    setPendingAttachments([]);

    // instructor messages don't trigger the bot
    if (role === 'instructor') return;

    setStreaming(true);
    const replyKey = replyKeyFor(text || '', hadAttach);
    const reply = CANNED_REPLIES[replyKey] || CANNED_REPLIES.default;
    const artifact = artifactFor(replyKey);
    const botId = mkId();

    setTimeout(() => {
      // start streaming reply
      updateChat(activeGroupId, st => ({
        messages: [...st.messages, {
          id: botId, role: 'bot', text: '', time: stamp(),
          streaming: true, artifact: null,
        }]
      }));

      let i = 0;
      const interval = setInterval(() => {
        i += 6 + Math.floor(Math.random() * 8);
        updateChat(activeGroupId, st => ({
          messages: st.messages.map(m =>
            m.id === botId
              ? { ...m, text: reply.slice(0, i), streaming: i < reply.length }
              : m
          )
        }));
        if (i >= reply.length) {
          clearInterval(interval);
          setStreaming(false);
          // attach the artifact reference + open it in side frame
          if (artifact) {
            updateChat(activeGroupId, st => ({
              messages: st.messages.map(m => m.id === botId ? { ...m, artifact } : m)
            }));
            // simulate teacherbot "writing" the doc with presence indicator
            simulateBotEditing(artifact.id);
          }
        }
      }, 40);
    }, 500);
  };

  // ----- simulate pair-programming presence ---------------------------------
  const simulateBotEditing = (docId) => {
    const doc = SEED_DOCS[docId];
    if (!doc) return;
    updateDocs(activeGroupId, st => ({
      openDocs: st.openDocs.find(d => d.id === docId)
        ? st.openDocs
        : [...st.openDocs, doc],
      activeDocId: docId,
    }));
    setDocPanelCollapsed(false);

    if (!tweaks.showPresence) return;

    const lineCount = doc.content.split('\n').length;
    let line = 1;
    setPresence({ line, col: 0 });
    const id = setInterval(() => {
      line = Math.min(lineCount, line + 1);
      setPresence({ line, col: 0 });
      if (line >= lineCount) {
        clearInterval(id);
        setTimeout(() => setPresence(null), 1200);
      }
    }, 220);
  };

  // ----- render -------------------------------------------------------------
  const appClass = 'app' + (tweaks.showPoster ? '' : ' app--no-poster');

  return (
    <div className={appClass}>
      {tweaks.showBanner && (
        <ClassificationBanner level={activeGroup.clearance} instructor={role === 'instructor'} />
      )}
      <Masthead
        active={activeGroup.code}
        sessionTime={sessionTime}
        role={role}
        onToggleRole={() => setRole(r => r === 'student' ? 'instructor' : 'student')}
      />
      <div className="main">
        <Sidebar
          groups={GROUPS}
          activeId={activeGroupId}
          onSelect={setActiveGroupId}
          role={role}
          onToggleRole={setRole}
          totalTokens={totalTokens}
        />
        <div className={'workspace' + (docLayout === 'side' ? ' workspace--split-row' : '')}>
          <ChatThread
            messages={chat.messages}
            streaming={streaming}
            opId={role === 'instructor' ? 'TA' : 'OP-' + activeGroup.id.toUpperCase()}
            group={activeGroup}
            role={role}
            onSend={handleSend}
            onOpenDoc={openDoc}
            attachments={pendingAttachments}
            onAttach={onAttach}
            onRemoveAttach={onRemoveAttach}
            onPasteCode={onPasteCode}
            presence={presence}
          />
          <DocPanel
            docs={docState.openDocs}
            activeId={docState.activeDocId}
            onSelectDoc={selectDoc}
            onCloseDoc={closeDoc}
            collapsed={docPanelCollapsed}
            onToggleCollapsed={() => setDocPanelCollapsed(c => !c)}
            presence={tweaks.showPresence ? presence : null}
            layout={docLayout}
            onToggleLayout={() => {
              const next = docLayout === 'stacked' ? 'side' : 'stacked';
              setDocLayout(next);
              setTweak('docLayout', next);
            }}
            height={docPanelHeight}
            onResize={setDocPanelHeight}
          />
        </div>
      </div>

      <window.TweaksPanel>
        <window.TweakSection title="Layout">
          <window.TweakRadio
            label="Side frame position"
            value={tweaks.docLayout}
            options={[
              { value: 'stacked', label: 'Bottom' },
              { value: 'side',    label: 'Side' },
            ]}
            onChange={(v) => setTweak('docLayout', v)}
          />
        </window.TweakSection>
        <window.TweakSection title="Pair Programming">
          <window.TweakToggle
            label="TEACHERBOT IS EDITING… presence"
            value={tweaks.showPresence}
            onChange={(v) => setTweak('showPresence', v)}
          />
        </window.TweakSection>
        <window.TweakSection title="Poster mode">
          <window.TweakToggle
            label="Classification banner"
            value={tweaks.showBanner}
            onChange={(v) => setTweak('showBanner', v)}
          />
          <window.TweakToggle
            label="Poster accents in empty state"
            value={tweaks.showPoster}
            onChange={(v) => setTweak('showPoster', v)}
          />
        </window.TweakSection>
        <window.TweakSection title="Demo">
          <window.TweakButton
            label="Trigger 'editing doc' presence demo"
            onClick={() => {
              const docId = docState.activeDocId || 'd_wsgi_new';
              simulateBotEditing(docId);
            }}
          />
          <window.TweakButton
            label="Clear active group's conversation"
            onClick={() => updateChat(activeGroupId, () => ({ messages: [] }))}
          />
        </window.TweakSection>
      </window.TweaksPanel>

      <FinePrint />
    </div>
  );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
