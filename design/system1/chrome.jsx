/* system1/chrome.jsx — masthead, classification banner, A-Eye mark, fine print */

const AEyeMark = ({ className = '' }) => (
  <svg viewBox="0 0 246.51 166.47" className={className} aria-hidden="true">
    <path d="M84.71,144.13l-16.2,22.35h178.01L141.43,10.07c-3.69-5.65-9.58-10.07-17.43-10.07s-14,4.91-17.44,10.07L0,166.47h31.43l42.39-62.74c4.53,4.54,15.78,13.44,17.94,14.87,7.54,4.99,18.08,10.11,27.18,10.9,20.44,1.79,39.42-11.92,53.28-25.91l26.91,40.54h-114.42ZM97,112.99l-15.07-11.86,15.07-11.86c-2.96,7.87-2.97,15.82,0,23.71ZM123.14,122.44c-11.72,0-21.22-9.5-21.22-21.22s9.5-21.22,21.22-21.22,21.22,9.5,21.22,21.22-9.5,21.22-21.22,21.22ZM149.47,112.99c.31-3.08,1.77-5.97,2.06-9.07.48-5.2-.66-9.85-2.42-14.65l15.43,11.86-15.07,11.86ZM119.14,72.96c-13.33,1.31-26.22,9.07-36.83,18.21l41.19-60.97,40.46,60.94c-12.74-10.79-28.42-19.8-44.82-18.19Z" />
    <path d="M126.6,98.01l3.65-7.39c-3.75-2.49-8.55-2.8-12.58-.81-6.21,3.07-8.8,10.7-5.73,16.91,3.07,6.21,10.7,8.8,16.91,5.73,6.21-3.07,8.8-10.7,5.73-16.91l-7.98,2.47Z" />
  </svg>
);

const ClassificationBanner = ({ level = 'ORANGE', children, instructor }) => (
  <div className={'classification-banner' + (instructor ? ' classification-banner--instructor' : '')}>
    <span style={{ marginRight: 12 }}>▲</span>
    {instructor
      ? 'INSTRUCTOR CO-PILOT MODE · ALL GROUPS VISIBLE · THE ALGORITHM OBSERVES YOUR OBSERVATION'
      : <>CLASSIFICATION: {level} CLEARANCE <span style={{ marginLeft: 12 }}>{children || 'THE ALGORITHM IS WATCHING'}</span></>}
    <span style={{ marginLeft: 12 }}>▲</span>
  </div>
);

const Masthead = ({ active, sessionTime, role, onToggleRole }) => (
  <header className="masthead">
    <div className="masthead__brand">
      <div className="masthead__mark"><AEyeMark /></div>
      <div className="masthead__brand-text">
        TEACHERBOT <span style={{ color: 'var(--amber)' }}>·</span> SYSTEM 1
        <small>ALGOCRATIC FUTURES™ · TA SHARED INTERFACE</small>
      </div>
    </div>
    <div className="masthead__breadcrumb">
      <span>PORTAL</span><span className="sep">/</span>
      <span>TA SYSTEMS</span><span className="sep">/</span>
      <span>SYSTEM 1</span><span className="sep">/</span>
      <span className="now">{active}</span>
    </div>
    <div className="masthead__right">
      <span className={'pill ' + (role === 'instructor' ? 'pill--instructor' : 'pill--online')}>
        <span className="pill__dot" />{role === 'instructor' ? 'INSTRUCTOR' : 'OPERATIVE'}
      </span>
      <span style={{ fontFamily: 'JetBrains Mono', fontSize: 11, color: 'var(--cream-muted)', letterSpacing: '0.1em' }}>
        {sessionTime}
      </span>
      <button className="lnk-btn" onClick={onToggleRole}>
        {role === 'instructor' ? 'EXIT CO-PILOT' : 'INSTRUCTOR'}
      </button>
    </div>
  </header>
);

const FinePrint = () => (
  <footer className="fineprint">
    Underwritten by the Office of Strategic Scarcity Operations with limited support from the Equal Access Unless Otherwise Specified Fund™.
    &nbsp;All transmissions logged for pedagogical review. Void where curiosity is absent. Limit one breakthrough per cycle.
    &nbsp;&nbsp;<span style={{ color: 'var(--amber)' }}>frotz → plugh</span>
  </footer>
);

Object.assign(window, { AEyeMark, ClassificationBanner, Masthead, FinePrint });
