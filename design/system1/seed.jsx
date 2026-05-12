/* system1/seed.jsx — seed data: groups, sample docs, scripted bot replies */

const GROUPS = [
  {
    id: 'g1',
    code: 'GROUP 01',
    alias: 'Crimson Spire',
    project: 'DataMan Math Platform',
    clearance: 'RED',
    members: 4,
    tokens: { used: 41200, cap: 100000 },
    activity: 'alert',
  },
  {
    id: 'g2',
    code: 'GROUP 02',
    alias: 'Ashen Plains',
    project: 'BAG Financial Manager',
    clearance: 'ORANGE',
    members: 5,
    tokens: { used: 22800, cap: 100000 },
    activity: 'active',
  },
  {
    id: 'g3',
    code: 'GROUP 03',
    alias: 'Mustard Meridian',
    project: 'Inventory Optimizer',
    clearance: 'YELLOW',
    members: 4,
    tokens: { used: 9620, cap: 100000 },
  },
  {
    id: 'g4',
    code: 'GROUP 04',
    alias: 'Moss Hollow',
    project: 'Sleep Tracker (mobile)',
    clearance: 'GREEN',
    members: 3,
    tokens: { used: 51400, cap: 100000 },
  },
  {
    id: 'g5',
    code: 'GROUP 05',
    alias: 'Teal Expanse',
    project: 'Recipe Vault & ML pairing',
    clearance: 'BLUE',
    members: 4,
    tokens: { used: 67250, cap: 100000 },
    activity: 'active',
  },
];

// Sample seed convo per group — illustrates document-sharing flow
const SEED_BY_GROUP = {
  g2: {
    docs: [],
    messages: [
      {
        id: 'm1', role: 'user', text: 'Our /login route returns 404 only in production. Works locally. Render env vars look fine.',
        time: '14:02:17',
      },
      {
        id: 'm2', role: 'bot',
        text: "Three suspects, in priority order.\n\n(1) Render is running gunicorn with a different app entry than `flask run`. Check your `Procfile` or render.yaml — is it pointing at the right module:app?\n(2) Blueprint registration: in your local `if __name__ == '__main__'` block but missing in `wsgi.py`. Production never executes the `__main__` branch.\n(3) Trailing slash strictness: Flask's default is strict. `/login` and `/login/` are different routes in production behind some proxies.\n\nMy bet: (2). Want me to draft a corrected `wsgi.py` you can drop in? Show me your current one first.",
        time: '14:02:43',
      },
      {
        id: 'm3', role: 'user',
        text: "Yeah here it is.",
        time: '14:03:51',
        attachment: { id: 'd_wsgi_old', name: 'wsgi.py', type: 'py' },
      },
      {
        id: 'm4', role: 'bot',
        text: "Confirmed. You import `app` but never register the auth blueprint. Production loads `wsgi:app` and `auth_bp` is never attached. I've drafted a fix in the side frame — open it and skim. Note the blueprint import + register call, and the explicit `url_prefix=''` so `/login` stays at root.",
        time: '14:04:18',
        artifact: { id: 'd_wsgi_new', name: 'wsgi.py (proposed)', type: 'py', author: 'bot' },
      },
    ],
  },
  g1: {
    docs: [],
    messages: [
      {
        id: 'm1', role: 'user',
        text: 'I burned half our token budget already and we still cannot decide an architecture. Help.',
        time: '11:14:08',
      },
      {
        id: 'm2', role: 'bot',
        text: "Pop quiz before I help: in one sentence, what's the actual decision you're stuck on? Database? Hosting? Auth? When students burn budget without progress it's usually because the meta-question isn't pinned down.\n\nAlso — RED clearance team carries the heaviest pedagogical weight on this. I'd rather draft you a one-page decision matrix than answer twelve sub-questions. Want me to?",
        time: '11:14:31',
      },
    ],
  },
  g5: {
    docs: [],
    messages: [
      {
        id: 'm1', role: 'user',
        text: 'Draft a sprint plan markdown for our next two weeks. Recipe Vault, focus on the ML pairing endpoint.',
        time: '09:22:00',
      },
      {
        id: 'm2', role: 'bot',
        text: "Drafted. See the side frame. I structured it as **goal → user-visible outcome → 5 issues per week**, sized so any one issue is half a day. Two notes:\n\n• Week 1 issue 3 is risky — it depends on the embedding model being reachable from Render. If it's not, swap with an offline batch step.\n• I left week-2 issue 5 deliberately empty. That's your slack day. Use it.",
        time: '09:22:34',
        artifact: { id: 'd_sprint_md', name: 'sprint-plan.md', type: 'md', author: 'bot' },
      },
    ],
  },
};

// Documents keyed by id — referenced from messages above
const SEED_DOCS = {
  d_wsgi_old: {
    id: 'd_wsgi_old',
    name: 'wsgi.py',
    type: 'py',
    author: 'user',
    content: `# wsgi.py — production entry for Render
from app import create_app

app = create_app()

# Local-only init (production never runs this branch)
if __name__ == "__main__":
    from auth import auth_bp
    app.register_blueprint(auth_bp)
    app.run(debug=True)
`,
  },
  d_wsgi_new: {
    id: 'd_wsgi_new',
    name: 'wsgi.py (proposed)',
    type: 'py',
    author: 'bot',
    content: `# wsgi.py — production entry for Render
# Fixed: blueprint registration now happens at module load, not only in __main__.
from app import create_app
from auth import auth_bp   # ← was missing in module scope

app = create_app()
app.register_blueprint(auth_bp, url_prefix="")   # ← explicit prefix

# Local dev only
if __name__ == "__main__":
    app.run(debug=True)
`,
  },
  d_sprint_md: {
    id: 'd_sprint_md',
    name: 'sprint-plan.md',
    type: 'md',
    author: 'bot',
    content: `# Sprint Plan — Recipe Vault

## Goal
Ship a working ML pairing endpoint to staging by end of week 2.

**User-visible outcome:** A logged-in user can paste a recipe and receive 3 suggested wine pairings with confidence scores.

---

## Week 1 — wire it up

- **W1-1** · Define the \`POST /api/pair\` request/response schema
- **W1-2** · Stub the endpoint, return canned data, write the integration test
- **W1-3** · Spike: can the embedding model be reached from Render? Timebox 4h
- **W1-4** · Persist recipe + pairings to Postgres (\`pairings\` table)
- **W1-5** · Add basic rate limit (10 req/min/user)

## Week 2 — make it real

- **W2-1** · Replace stub with real embedding lookup + nearest-neighbor over the wine corpus
- **W2-2** · Confidence score: cosine similarity → 0-1 scale, three tiers
- **W2-3** · Frontend: pairing card component
- **W2-4** · Telemetry: log queries (anonymized) for instructor review
- **W2-5** · *(slack day — keep empty)*

---

## Risks

- Embedding model latency from Render → consider caching layer
- Wine corpus licensing — confirm with instructor before final demo

*The Algorithm provides. The Algorithm watches. The Algorithm ships.*
`,
  },
};

// canned replies — generic fallback
const CANNED_REPLIES = {
  '404': "Three suspects, in priority order.\n\n(1) Production entry point — is gunicorn pointing at the right `module:app`?\n(2) Blueprint registration — registered in `__main__` only? Production never runs that branch.\n(3) Trailing slash strictness — `/login` vs `/login/` behind a proxy.\n\nMy bet's (2). Want me to draft a corrected `wsgi.py`? Attach your current one first.",
  flask: "Flask sessions in 30 seconds.\n\nA `session` is a tiny dictionary that lives on the server side but is keyed by a cookie on the client. The cookie holds an opaque ID; the dictionary holds whatever you put in it.\n\nYou write `session['user_id'] = 42` and Flask hands the cookie back. Next request: cookie → lookup → `session['user_id']` is 42 again.\n\nThe trick: you MUST set `app.secret_key` or sessions silently do nothing. Pop quiz: where in your app are you setting it today?",
  sqlite: "SQLite for the capstone. Zero ops, no server, no connection string. Faster than Postgres for one-semester load. SQLAlchemy lets you swap later in one config line.\n\nThe only reason to start with Postgres: concurrent writers or instructor mandate. Neither is probably true. Push back if you're being told otherwise.",
  review: "Happy to. Paste the PR URL or attach the diff. While you grab it, three quick questions I'll need:\n\n(1) What problem does this PR solve, in one sentence?\n(2) What did you try first that didn't work?\n(3) Where do you think the weakest part is?\n\nLead with these and you'll get a better review — that's what a senior reviewer expects anyway.",
  sprint: "Drafted a two-week sprint plan in the side frame. Structured as goal → user-visible outcome → five half-day issues per week. Week-2 slot 5 is intentionally empty — that's your slack day, defend it.",
  draft: "Drafting a markdown plan for you — opening in the side frame now. Skim and tell me which bullets feel wrong.",
  attach: "Got the file. Reading it now.\n\nFirst pass: the blueprint registration is in your `__main__` block, which production never runs. That's the 404. I've put a corrected version in the side frame — open the artifact card to view it side-by-side with your original.",
  pasted: "I've moved that block into the side frame so you can keep it visible while we talk. Walk me through what you've tried — line by line if you can. What's the actual error?",
  default: "Good question. Before I answer: what have you tried so far? That's usually the fastest way for me to be useful.\n\n*(Pop quiz to keep you sharp: in one sentence, what's the goal here?)*",
};

const STARTER_DOC = {
  name: 'pasted.py',
  type: 'py',
  author: 'user',
  content: `# Pasted from chat
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.check_password(request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    return render_template('login.html')
`,
};

Object.assign(window, { GROUPS, SEED_BY_GROUP, SEED_DOCS, CANNED_REPLIES, STARTER_DOC });
