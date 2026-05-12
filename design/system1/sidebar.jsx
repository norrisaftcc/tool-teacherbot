/* system1/sidebar.jsx — 5-group switcher rail with token meters + role context */

const MiniMeter = ({ used, cap, color }) => {
  const pct = Math.min(100, Math.round((used / cap) * 100));
  const barColor =
    pct > 85 ? 'var(--rust)' :
    pct > 65 ? 'var(--mustard)' :
    color || 'var(--moss)';
  return (
    <div className="mini-meter">
      <span>T</span>
      <div className="mini-meter__bar">
        <div className="mini-meter__fill" style={{ width: pct + '%', background: barColor }} />
      </div>
      <span className="mini-meter__val">{pct}%</span>
    </div>
  );
};

const GroupRow = ({ group, active, onClick, showAll, role }) => {
  // when student-mode, hide non-active groups completely
  if (role === 'student' && !active && !showAll) return null;
  return (
    <button
      className={'group-row' + (active ? ' group-row--active' : '')}
      onClick={onClick}
    >
      {group.activity && (
        <span className={'activity' + (group.activity === 'alert' ? ' activity--alert' : '')} />
      )}
      <div className="group-row__head">
        <span className="group-row__name">{group.code}</span>
        <span className={'group-row__clearance clearance--' + group.clearance.toLowerCase()}>
          ● {group.clearance}
        </span>
      </div>
      <div className="group-row__alias">{group.alias}</div>
      <div className="group-row__project">{group.project}</div>
      <MiniMeter used={group.tokens.used} cap={group.tokens.cap} />
    </button>
  );
};

const Sidebar = ({ groups, activeId, onSelect, role, onToggleRole, totalTokens }) => {
  const active = groups.find(g => g.id === activeId);
  return (
    <aside className="sidebar">
      {/* role toggle */}
      <div className="sidebar__section">
        <div className="sidebar__heading">
          <span>ROLE</span>
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: 9, color: 'var(--cream-muted)', letterSpacing: '0.1em' }}>
            FROM PORTAL
          </span>
        </div>
        <div className="role-toggle">
          <button
            className={'role-toggle__btn' + (role === 'student' ? ' role-toggle__btn--active' : '')}
            onClick={() => onToggleRole('student')}
          >
            OPERATIVE
          </button>
          <button
            className={'role-toggle__btn role-toggle__btn--teal' + (role === 'instructor' ? ' role-toggle__btn--active' : '')}
            onClick={() => onToggleRole('instructor')}
          >
            INSTRUCTOR
          </button>
        </div>
        <div style={{
          marginTop: 10,
          fontFamily: 'var(--font-mono)',
          fontSize: 10,
          color: 'var(--cream-muted)',
          letterSpacing: '0.06em',
          lineHeight: 1.5,
        }}>
          {role === 'student'
            ? 'You see your group only. Conversations logged for instructor review.'
            : 'You see all groups. You may post as INSTRUCTOR alongside the bot.'}
        </div>
      </div>

      {/* group switcher */}
      <div className="sidebar__section sidebar__section--scroll">
        <div className="sidebar__heading">
          <span>{role === 'instructor' ? 'ASSIGNED GROUPS · 05' : 'YOUR GROUP'}</span>
          {role === 'instructor' && (
            <span className="pill pill--instructor" style={{ fontSize: 8 }}>
              <span className="pill__dot" />CO-PILOT
            </span>
          )}
        </div>
        <ul className="group-list">
          {groups.map(g => (
            <GroupRow
              key={g.id}
              group={g}
              active={g.id === activeId}
              onClick={() => onSelect(g.id)}
              role={role}
              showAll={role === 'instructor'}
            />
          ))}
        </ul>

        {role === 'student' && active && (
          <div style={{
            marginTop: 18,
            padding: 10,
            border: '1px dashed var(--ink-muted)',
            fontFamily: 'var(--font-mono)',
            fontSize: 10,
            color: 'var(--cream-muted)',
            lineHeight: 1.6,
            letterSpacing: '0.04em',
          }}>
            <strong style={{ color: 'var(--mustard)', display: 'block', marginBottom: 4, letterSpacing: '0.1em' }}>
              ▲ ISOLATION NOTICE
            </strong>
            Other groups exist but their conversations are not visible to OPERATIVE clearance.
            Switch to INSTRUCTOR to observe across the cohort.
          </div>
        )}
      </div>

      {/* cohort summary */}
      <div className="sidebar__section">
        <div className="sidebar__heading">
          <span>{role === 'instructor' ? 'COHORT TOKENS · CYCLE 03' : 'YOUR TOKENS · CYCLE 03'}</span>
        </div>
        <div style={{
          fontFamily: 'var(--font-mono)',
          fontSize: 11,
          color: 'var(--cream)',
          display: 'flex', justifyContent: 'space-between',
          marginBottom: 6,
        }}>
          <span style={{ color: 'var(--cream-muted)', letterSpacing: '0.06em', textTransform: 'uppercase' }}>
            {role === 'instructor' ? 'Σ used' : 'used'}
          </span>
          <span style={{ color: 'var(--mustard)', fontWeight: 700 }}>
            {totalTokens.used.toLocaleString()} / {totalTokens.cap.toLocaleString()}
          </span>
        </div>
        <div style={{
          height: 6,
          background: 'var(--ink)',
          border: '1px solid var(--ink-muted)',
          position: 'relative',
          overflow: 'hidden',
        }}>
          <div style={{
            position: 'absolute', inset: 0, right: 'auto',
            width: Math.min(100, (totalTokens.used / totalTokens.cap) * 100) + '%',
            background: 'var(--mustard)',
          }} />
        </div>
        <div style={{
          fontFamily: 'var(--font-mono)',
          fontSize: 9,
          color: 'var(--cream-muted)',
          letterSpacing: '0.08em',
          textTransform: 'uppercase',
          marginTop: 6,
          display: 'flex',
          justifyContent: 'space-between',
        }}>
          <span>resets monday</span>
          <span>budget by directive AF-TOK-2026</span>
        </div>
      </div>
    </aside>
  );
};

Object.assign(window, { Sidebar, GroupRow, MiniMeter });
