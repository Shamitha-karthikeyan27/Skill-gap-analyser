import React, { useState, useEffect, useRef } from 'react';
import './index.css';

const API = 'http://127.0.0.1:5000';

// ============ ICONS ============
const Ic = ({ path, size = 18 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        {path}
    </svg>
);
const I = {
    logo: <><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" /></>,
    mail: <><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" /><polyline points="22,6 12,13 2,6" /></>,
    lock: <><rect x="3" y="11" width="18" height="11" rx="2" ry="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" /></>,
    user: <><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" /></>,
    upload: <><polyline points="16 16 12 12 8 16" /><line x1="12" y1="12" x2="12" y2="21" /><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3" /></>,
    search: <><circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" /></>,
    check: <><polyline points="20 6 9 17 4 12" /></>,
    x: <><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></>,
    arrow: <><line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" /></>,
    back: <><line x1="19" y1="12" x2="5" y2="12" /><polyline points="12 19 5 12 12 5" /></>,
    chat: <><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /></>,
    send: <><line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" /></>,
    logout: <><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" /><polyline points="16 17 21 12 16 7" /><line x1="21" y1="12" x2="9" y2="12" /></>,
    trophy: <><polyline points="8 17 12 21 16 17" /><line x1="12" y1="21" x2="12" y2="11" /><path d="M20 4H4v8a8 8 0 0 0 16 0V4z" /></>,
    timer: <><circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" /></>,
    book: <><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" /><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" /></>,
    building: <><rect x="2" y="3" width="20" height="20" rx="1" /><path d="M16 3v18M8 3v18M2 12h20M2 7h6M16 7h6M2 17h6M16 17h6" /></>,
    map: <><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21 3 6" /></>,
};

// ============ CIRCULAR CHART ============
const Circle = ({ pct, size = 130 }) => {
    const r = 50; const c = 2 * Math.PI * r;
    return (
        <div style={{ position: 'relative', width: size, height: size }}>
            <svg width={size} height={size} viewBox="0 0 120 120" style={{ transform: 'rotate(-90deg)' }}>
                <circle cx="60" cy="60" r={r} fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="10" />
                <circle cx="60" cy="60" r={r} fill="none" strokeWidth="10"
                    stroke={pct >= 70 ? '#10b981' : pct >= 40 ? '#f59e0b' : '#ef4444'}
                    strokeDasharray={c} strokeDashoffset={c - (pct / 100) * c} strokeLinecap="round"
                    style={{ transition: 'stroke-dashoffset 1.4s cubic-bezier(0.4,0,0.2,1)' }}
                />
            </svg>
            <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%,-50%)', textAlign: 'center' }}>
                <div style={{ fontSize: 22, fontWeight: 800 }}>{pct}%</div>
                <div style={{ fontSize: 10, color: 'var(--text-secondary)' }}>Match</div>
            </div>
        </div>
    );
};

// ============ APP ROOT ============
export default function App() {
    const [token, setToken] = useState(localStorage.getItem('sg_token'));
    const [user, setUser] = useState(localStorage.getItem('sg_user') || '');
    const [page, setPage] = useState('upload'); // upload | roles | results | mock | mock-results
    const [extractedSkills, setExtractedSkills] = useState({}); // { name: score }
    const [selectedRole, setSelectedRole] = useState(null);
    const [analysisResult, setAnalysisResult] = useState(null);
    const [mockResult, setMockResult] = useState(null);
    const [chatOpen, setChatOpen] = useState(false);
    const [chatMsgs, setChatMsgs] = useState([{ role: 'bot', text: "👋 Hi! I'm your AI Career Mentor. Ask me for a roadmap, skill advice, or job tips!" }]);
    const [chatIn, setChatIn] = useState('');
    const chatRef = useRef(null);

    useEffect(() => { chatRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [chatMsgs]);

    const doLogout = () => {
        localStorage.removeItem('sg_token'); localStorage.removeItem('sg_user');
        setToken(null); setUser(''); setPage('upload');
        setExtractedSkills({}); setSelectedRole(null); setAnalysisResult(null);
    };

    const sendChat = async () => {
        if (!chatIn.trim()) return;
        const msg = chatIn; setChatIn('');
        setChatMsgs(p => [...p, { role: 'user', text: msg }]);
        try {
            const r = await fetch(`${API}/api/chatbot`, {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: msg,
                    role: selectedRole?.title || '',
                    missing_skills: analysisResult?.missing_skills || []
                })
            });
            const d = await r.json();
            setChatMsgs(p => [...p, { role: 'bot', text: d.response }]);
        } catch {
            setChatMsgs(p => [...p, { role: 'bot', text: 'Connection error. Please check the backend.' }]);
        }
    };

    if (!token) return <AuthPage setToken={setToken} setUser={setUser} />;

    return (
        <div className="app-layout">
            {/* sidebar */}
            <aside className="sidebar">
                <div className="sidebar-logo"><div className="sidebar-logo-icon"><Ic path={I.logo} size={16} /></div>
                    <span className="sidebar-logo-text">Skill<span>Gap</span></span></div>

                <nav className="sidebar-nav">
                    <span className="sidebar-section-label">Steps</span>
                    {[
                        { id: 'upload', label: '1. Upload Resume', icon: I.upload },
                        { id: 'roles', label: '2. Select Role', icon: I.search },
                        { id: 'results', label: '3. View Results', icon: I.trophy },
                        { id: 'mock', label: '4. Mock Test', icon: I.timer },
                    ].map(s => (
                        <button key={s.id} className={`nav-item ${page === s.id ? 'active' : ''}`} onClick={() => setPage(s.id)}>
                            <Ic path={s.icon} size={16} />{s.label}
                        </button>
                    ))}
                    <span className="sidebar-section-label">Resources</span>
                    <button className="nav-item" onClick={() => setChatOpen(o => !o)}><Ic path={I.chat} size={16} />AI Career Mentor</button>
                </nav>

                <div className="sidebar-footer">
                    <div className="user-card">
                        <div className="user-avatar">{user.charAt(0).toUpperCase()}</div>
                        <div><div className="user-name">{user}</div><div className="user-role">Job Seeker</div></div>
                        <button onClick={doLogout} style={{ marginLeft: 'auto', background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-secondary)', padding: 4 }} title="Logout"><Ic path={I.logout} size={15} /></button>
                    </div>
                </div>
            </aside>

            {/* main */}
            <div className="main-content">
                <header className="topbar">
                    <span className="topbar-title">
                        {{ upload: 'Upload Resume', roles: 'Select Role', results: 'Skill Analysis Results', mock: 'Mock Test', 'mock-results': 'Test Results' }[page]}
                    </span>
                    <div className="topbar-actions">
                        {selectedRole && <span className="topbar-badge">🎯 {selectedRole.title}</span>}
                        {analysisResult && (
                            <span className={`topbar-badge ${analysisResult.suitability_score >= 70 ? 'badge-green' : 'badge-red'}`}>
                                {analysisResult.suitability_score >= 70 ? '✅ Ready to Apply' : '🔶 Needs Improvement'}
                            </span>
                        )}
                    </div>
                </header>
                <main className="page-content">
                    {page === 'upload' && <UploadPage setExtractedSkills={setExtractedSkills} setPage={setPage} />}
                    {page === 'roles' && <RolePage extractedSkills={extractedSkills} setSelectedRole={setSelectedRole} setAnalysisResult={setAnalysisResult} setPage={setPage} />}
                    {page === 'results' && <ResultsPage result={analysisResult} role={selectedRole} setPage={setPage} />}
                    {page === 'mock' && <MockPage role={selectedRole} setMockResult={setMockResult} setPage={setPage} />}
                    {page === 'mock-results' && <MockResultPage result={mockResult} role={selectedRole} setPage={setPage} />}
                </main>
            </div>

            {/* chatbot */}
            <button className="chatbot-fab" onClick={() => setChatOpen(o => !o)}>
                {chatOpen ? <Ic path={I.x} size={20} /> : <Ic path={I.chat} size={20} />}
            </button>
            {chatOpen && (
                <div className="chatbot-window">
                    <div className="chatbot-header">
                        <div className="chatbot-avatar">🤖</div>
                        <div><div style={{ fontWeight: 600, fontSize: 14 }}>AI Career Mentor</div><div style={{ fontSize: 11, color: 'var(--text-secondary)' }}>Roadmaps · Skills · Tips</div></div>
                        <div className="chatbot-status" />
                    </div>
                    <div className="chat-messages">
                        {chatMsgs.map((m, i) => (
                            <div key={i} className={`chat-msg ${m.role}`}>
                                <div className="chat-bubble" style={{ whiteSpace: 'pre-wrap' }}>{m.text}</div>
                            </div>
                        ))}
                        <div ref={chatRef} />
                    </div>
                    <div className="chat-input-row">
                        <input className="chat-input" value={chatIn} onChange={e => setChatIn(e.target.value)}
                            onKeyDown={e => e.key === 'Enter' && sendChat()} placeholder="Ask for a roadmap…" />
                        <button className="chat-send" onClick={sendChat}><Ic path={I.send} size={15} /></button>
                    </div>
                </div>
            )}
        </div>
    );
}

// ============ AUTH PAGE ============
function AuthPage({ setToken, setUser }) {
    const [tab, setTab] = useState('login');
    const [form, setForm] = useState({ username: '', email: '', password: '' });
    const [err, setErr] = useState('');
    const [loading, setLoading] = useState(false);

    const submit = async () => {
        setLoading(true); setErr('');
        const url = tab === 'login' ? `${API}/api/auth/login` : `${API}/api/auth/register`;
        try {
            const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) });
            if (!r.ok) throw new Error('Server returned an error.');
            const d = await r.json();
            if (d.error) { setErr(d.error); setLoading(false); return; }
            localStorage.setItem('sg_token', d.token);
            const uname = tab === 'login' ? (form.email.split('@')[0]) : form.username;
            localStorage.setItem('sg_user', uname);
            setToken(d.token); setUser(uname);
        } catch (e) { setErr(e.message || 'Cannot connect to server. Make sure the backend is running.'); }
        setLoading(false);
    };

    return (
        <div style={{ minHeight: '100vh', background: 'var(--bg-base)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            {/* bg orbs */}
            <div style={{ position: 'fixed', top: '-20%', left: '-10%', width: '40%', height: '40%', background: 'rgba(99,102,241,0.12)', filter: 'blur(100px)', borderRadius: '50%', pointerEvents: 'none' }} />
            <div style={{ position: 'fixed', bottom: '-15%', right: '-10%', width: '35%', height: '35%', background: 'rgba(6,182,212,0.1)', filter: 'blur(100px)', borderRadius: '50%', pointerEvents: 'none' }} />

            <div className="card fade-up" style={{ width: 420, padding: 40 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 32 }}>
                    <div className="sidebar-logo-icon"><Ic path={I.logo} size={16} /></div>
                    <div style={{ fontSize: 20, fontWeight: 800, letterSpacing: '-0.5px' }}>Skill<span style={{ color: 'var(--accent)' }}>Gap</span></div>
                </div>

                <div style={{ display: 'flex', background: 'var(--bg-elevated)', borderRadius: 10, padding: 4, marginBottom: 28, gap: 4 }}>
                    {['login', 'register'].map(t => (
                        <button key={t} onClick={() => setTab(t)} style={{
                            flex: 1, padding: '9px 0', borderRadius: 8, border: 'none', cursor: 'pointer', fontFamily: 'inherit',
                            fontWeight: 600, fontSize: 13,
                            background: tab === t ? 'var(--bg-card)' : 'transparent',
                            color: tab === t ? 'var(--text-primary)' : 'var(--text-secondary)',
                            transition: 'all 0.2s'
                        }}>
                            {t === 'login' ? 'Sign In' : 'Create Account'}
                        </button>
                    ))}
                </div>

                <h2 style={{ fontSize: 22, fontWeight: 800, letterSpacing: '-0.5px', marginBottom: 6 }}>
                    {tab === 'login' ? 'Welcome back' : 'Get started'}
                </h2>
                <p style={{ color: 'var(--text-secondary)', fontSize: 13.5, marginBottom: 28 }}>
                    {tab === 'login' ? 'Sign in to your account to continue.' : 'Create your free account today.'}
                </p>

                {tab === 'register' && (
                    <div className="form-group">
                        <label className="form-label">Username</label>
                        <div style={{ position: 'relative' }}>
                            <span style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-secondary)' }}><Ic path={I.user} size={15} /></span>
                            <input className="form-control" style={{ paddingLeft: 36 }} placeholder="e.g. shamitha" value={form.username} onChange={e => setForm({ ...form, username: e.target.value })} />
                        </div>
                    </div>
                )}

                <div className="form-group">
                    <label className="form-label">Email</label>
                    <div style={{ position: 'relative' }}>
                        <span style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-secondary)' }}><Ic path={I.mail} size={15} /></span>
                        <input className="form-control" style={{ paddingLeft: 36 }} type="email" placeholder="you@example.com" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} />
                    </div>
                </div>

                <div className="form-group">
                    <label className="form-label">Password</label>
                    <div style={{ position: 'relative' }}>
                        <span style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-secondary)' }}><Ic path={I.lock} size={15} /></span>
                        <input className="form-control" style={{ paddingLeft: 36 }} type="password" placeholder="••••••••" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} onKeyDown={e => e.key === 'Enter' && submit()} />
                    </div>
                </div>

                {err && <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', color: '#ef4444', padding: '10px 14px', borderRadius: 8, fontSize: 13, marginBottom: 16 }}>{err}</div>}

                <button className="btn btn-primary btn-lg w-full" onClick={submit} disabled={loading}>
                    {loading ? 'Please wait…' : tab === 'login' ? 'Sign In' : 'Create Account'}
                </button>
            </div>
        </div>
    );
}

// ============ UPLOAD PAGE ============
function UploadPage({ setExtractedSkills, setPage }) {
    const [mode, setMode] = useState('pdf');
    const [text, setText] = useState('');
    const [skills, setSkills] = useState([]);
    const [skillLevels, setSkillLevels] = useState({}); // { name: level }
    const [nlpMetadata, setNlpMetadata] = useState(null);
    const [loading, setLoading] = useState(false);
    const [drag, setDrag] = useState(false);
    const fileRef = useRef();

    const handleFile = async (file) => {
        if (!file || !file.name.endsWith('.pdf')) { alert('Please upload a PDF file'); return; }
        setLoading(true);
        const fd = new FormData(); fd.append('file', file);
        try {
            const r = await fetch(`${API}/api/resume/upload`, { method: 'POST', body: fd });
            const d = await r.json();
            const extracted = d.extracted_skills || [];
            setSkills(extracted);
            const initialLevels = {};
            extracted.forEach(s => initialLevels[s] = 6); // Default: Intermediate
            setSkillLevels(initialLevels);
            setNlpMetadata(d.nlp_metadata || null);
        } catch { alert('Upload failed. Check backend.'); }
        setLoading(false);
    };

    const handleText = async () => {
        if (!text.trim()) return;
        setLoading(true);
        try {
            const r = await fetch(`${API}/api/extract-skills`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text }) });
            const d = await r.json();
            const extracted = d.extracted_skills || [];
            setSkills(extracted);
            const initialLevels = {};
            extracted.forEach(s => initialLevels[s] = 6); // Default: Intermediate
            setSkillLevels(initialLevels);
            setNlpMetadata(d.nlp_metadata || null);
        } catch { alert('Failed. Check backend.'); }
        setLoading(false);
    };

    const proceed = () => { 
        const final = {};
        skills.forEach(s => final[s] = skillLevels[s] || 6);
        setExtractedSkills(final); 
        setPage('roles'); 
    };

    return (
        <div className="fade-up" style={{ maxWidth: 760, margin: '0 auto' }}>
            <div style={{ marginBottom: 28 }}>
                <h1 style={{ fontSize: 24, fontWeight: 800, letterSpacing: '-0.5px', marginBottom: 6 }}>Upload Your Resume</h1>
                <p style={{ color: 'var(--text-secondary)', fontSize: 14 }}>Our NLP engine will automatically extract your skills.</p>
            </div>

            {/* mode toggle */}
            <div style={{ display: 'flex', background: 'var(--bg-elevated)', borderRadius: 10, padding: 4, marginBottom: 24, width: 'fit-content', gap: 4 }}>
                {['pdf', 'text'].map(m => (
                    <button key={m} onClick={() => setMode(m)} style={{
                        padding: '8px 20px', borderRadius: 8, border: 'none', cursor: 'pointer', fontFamily: 'inherit',
                        fontWeight: 600, fontSize: 13,
                        background: mode === m ? 'var(--bg-card)' : 'transparent',
                        color: mode === m ? 'var(--text-primary)' : 'var(--text-secondary)',
                        transition: 'all 0.2s'
                    }}>{m === 'pdf' ? '📄 Upload PDF' : '📝 Type / Paste'}</button>
                ))}
            </div>

            {mode === 'pdf' ? (
                <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
                    <div
                        className={`drop-zone ${drag ? 'drag-active' : ''}`}
                        style={{
                            padding: 60, textAlign: 'center', cursor: 'pointer', border: '2px dashed var(--border)', borderRadius: 12, transition: 'all 0.2s',
                            background: drag ? 'var(--accent-glow)' : 'transparent', borderColor: drag ? 'var(--accent)' : 'var(--border)'
                        }}
                        onClick={() => fileRef.current.click()}
                        onDragOver={e => { e.preventDefault(); setDrag(true); }}
                        onDragLeave={() => setDrag(false)}
                        onDrop={e => { e.preventDefault(); setDrag(false); handleFile(e.dataTransfer.files[0]); }}
                    >
                        <div style={{ fontSize: 48, marginBottom: 16 }}>📄</div>
                        <div style={{ fontWeight: 700, fontSize: 16, marginBottom: 8 }}>Drag & drop your PDF resume</div>
                        <div style={{ color: 'var(--text-secondary)', fontSize: 13, marginBottom: 20 }}>or click to browse</div>
                        <button className="btn btn-outline" onClick={e => { e.stopPropagation(); fileRef.current.click(); }}>
                            <Ic path={I.upload} size={15} /> Browse File
                        </button>
                        <input ref={fileRef} type="file" accept=".pdf" style={{ display: 'none' }} onChange={e => handleFile(e.target.files[0])} />
                    </div>
                </div>
            ) : (
                <div className="card">
                    <div className="form-group" style={{ marginBottom: 16 }}>
                        <label className="form-label">Paste your resume or describe your skills</label>
                        <textarea className="form-control" rows={10} value={text} onChange={e => setText(e.target.value)}
                            placeholder="e.g. I have 2 years of experience in Python, SQL, and Machine Learning. I have worked with Pandas, NumPy, and Scikit-learn to build predictive models. I also know Tableau and Power BI for visualization..." />
                    </div>
                    <button className="btn btn-primary" onClick={handleText} disabled={loading || !text.trim()}>
                        <Ic path={I.search} size={15} /> {loading ? 'Extracting…' : 'Extract Skills'}
                    </button>
                </div>
            )}

            {loading && (
                <div className="card mt-4" style={{ textAlign: 'center', padding: 32 }}>
                    <div style={{ fontSize: 32, marginBottom: 12 }}>⚙️</div>
                    <div style={{ fontWeight: 600 }}>Analyzing with NLP…</div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: 13, marginTop: 6 }}>Extracting skill entities from your document</div>
                </div>
            )}

            {skills.length > 0 && !loading && (
                <div className="card mt-4 fade-up">
                    <div className="card-header">
                        <div className="card-title">✅ Skills Extracted ({skills.length})</div>
                    </div>

                    {nlpMetadata && nlpMetadata.chunks_detected?.length > 0 && (
                        <div style={{marginBottom: 16, fontSize: 13, color: 'var(--text-secondary)'}}>
                            <strong style={{color: 'var(--text-primary)'}}>Resume Chunks Parsed:</strong> {nlpMetadata.chunks_detected.join(', ')}
                        </div>
                    )}
                    
                    {nlpMetadata && (nlpMetadata.entities?.organizations?.length > 0 || nlpMetadata.entities?.dates?.length > 0) && (
                        <div style={{marginBottom: 16, fontSize: 13, background: 'var(--bg-elevated)', padding: 12, borderRadius: 8}}>
                            <strong style={{color: 'var(--accent)'}}>Named Entities Extracted (NER):</strong>
                            {nlpMetadata.entities.organizations?.length > 0 && <div style={{marginTop: 6}}>🏢 Organizations: {nlpMetadata.entities.organizations.join(', ')}</div>}
                            {nlpMetadata.entities.dates?.length > 0 && <div style={{marginTop: 6}}>📅 Dates: {nlpMetadata.entities.dates.join(', ')}</div>}
                        </div>
                    )}

                    <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 24 }}>
                        {skills.map(s => (
                            <div key={s} className="card" style={{ padding: '12px 16px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: 'var(--bg-elevated)', border: 'none' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                                    <div className="badge badge-accent" style={{ margin: 0 }}>{s}</div>
                                    <span style={{ fontSize: 12, color: 'var(--text-secondary)' }}>Expertise: {nlpMetadata?.skills?.[s]?.score || 'N/A'}</span>
                                </div>
                                <div style={{ display: 'flex', background: 'var(--bg-base)', borderRadius: 8, padding: 3, gap: 2 }}>
                                    {[
                                        { label: 'Beg', val: 3 },
                                        { label: 'Int', val: 6 },
                                        { label: 'Exp', val: 10 }
                                    ].map(lvl => (
                                        <button
                                            key={lvl.label}
                                            onClick={() => setSkillLevels(p => ({ ...p, [s]: lvl.val }))}
                                            style={{
                                                padding: '4px 10px', fontSize: 11, fontWeight: 700, borderRadius: 6, border: 'none', cursor: 'pointer',
                                                background: skillLevels[s] === lvl.val ? 'var(--accent)' : 'transparent',
                                                color: skillLevels[s] === lvl.val ? '#fff' : 'var(--text-secondary)',
                                                transition: 'all 0.2s'
                                            }}
                                        >
                                            {lvl.label}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                    <button className="btn btn-primary btn-lg w-full" onClick={proceed}>
                        Continue to Role Selection <Ic path={I.arrow} size={16} />
                    </button>
                </div>
            )}
        </div>
    );
}

// ============ ROLE SELECT PAGE ============
function RolePage({ extractedSkills, setSelectedRole, setAnalysisResult, setPage }) {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [analyzing, setAnalyzing] = useState(null);

    useEffect(() => {
        fetch(`${API}/api/jobs`).then(r => r.json()).then(setJobs).catch(() => { });
    }, []);

    const analyze = async (job) => {
        if (Object.keys(extractedSkills).length === 0) { alert('Please upload your resume first!'); setPage('upload'); return; }
        setAnalyzing(job.id); setLoading(true);
        try {
            const r = await fetch(`${API}/api/analyze`, {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ skills: extractedSkills, job_id: job.id })
            });
            const d = await r.json();
            setSelectedRole(job);
            setAnalysisResult(d);
            setPage('results');
        } catch { alert('Analysis failed. Check backend.'); }
        setLoading(false); setAnalyzing(null);
    };

    return (
        <div className="fade-up">
            <div style={{ marginBottom: 28 }}>
                <h1 style={{ fontSize: 24, fontWeight: 800, letterSpacing: '-0.5px', marginBottom: 6 }}>Choose Your Target Role</h1>
                <p style={{ color: 'var(--text-secondary)', fontSize: 14 }}>Select the role you want to apply for. We'll match your skills against its requirements.</p>
            </div>

            {Object.keys(extractedSkills).length === 0 && (
                <div className="card" style={{ marginBottom: 20, background: 'rgba(245,158,11,0.08)', borderColor: 'rgba(245,158,11,0.25)' }}>
                    <div style={{ color: '#f59e0b', fontWeight: 600, fontSize: 13 }}>⚠️ No skills detected yet. <button className="btn btn-outline" style={{ marginLeft: 8, padding: '4px 12px', fontSize: 12 }} onClick={() => setPage('upload')}>Upload Resume first →</button></div>
                </div>
            )}

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: 16 }}>
                {jobs.map(job => (
                    <div key={job.id} className="card" style={{ cursor: 'pointer', transition: 'all 0.2s', display: 'flex', flexDirection: 'column', gap: 12 }}
                        onClick={() => analyze(job)}>
                        <div style={{ fontSize: 36 }}>{job.icon || '💼'}</div>
                        <div style={{ fontWeight: 700, fontSize: 16 }}>{job.title}</div>
                        <div style={{ color: 'var(--text-secondary)', fontSize: 13, lineHeight: 1.5, flex: 1 }}>{job.description}</div>
                        <button className="btn btn-primary w-full" disabled={analyzing === job.id}>
                            {analyzing === job.id ? 'Analyzing…' : 'Analyze My Fit'} {analyzing !== job.id && <Ic path={I.arrow} size={14} />}
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

// ============ RESULTS PAGE ============
function ResultsPage({ result, role, setPage }) {
    const [companies, setCompanies] = useState([]);

    useEffect(() => {
        if (role) fetch(`${API}/api/companies?job_id=${role.id}`).then(r => r.json()).then(setCompanies).catch(() => { });
    }, [role]);

    if (!result) return (
        <div className="empty-state fade-up">
            <div className="empty-icon">📊</div>
            <div className="empty-title">No Analysis Yet</div>
            <div className="empty-desc">Upload your resume and select a role to see results.</div>
            <button className="btn btn-primary mt-4" onClick={() => setPage('upload')}>Get Started</button>
        </div>
    );

    const { suitability_score: pct, matched_skills = [], semantic_matches = [], missing_skills = [], recommendations = [], learning_topics = [] } = result;
    const ready = pct >= 70;

    return (
        <div className="fade-up">
            {/* header banner */}
            <div className="card mb-6" style={{
                background: ready
                    ? 'linear-gradient(135deg, rgba(16,185,129,0.15), rgba(6,182,212,0.08))'
                    : 'linear-gradient(135deg, rgba(239,68,68,0.12), rgba(245,158,11,0.08))',
                borderColor: ready ? 'rgba(16,185,129,0.3)' : 'rgba(239,68,68,0.3)',
                display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 20
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
                    <Circle pct={pct} />
                    <div>
                        <div style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 4 }}>Target Role</div>
                        <div style={{ fontSize: 22, fontWeight: 800, letterSpacing: '-0.5px', marginBottom: 8 }}>{role?.title}</div>
                        <span className={`badge ${ready ? 'badge-green' : 'badge-red'}`} style={{ fontSize: 13, padding: '6px 16px' }}>
                            {ready ? '✅ Ready to Apply!' : '🔶 Skill Gaps Found'}
                        </span>
                    </div>
                </div>
                <div style={{ display: 'flex', gap: 10 }}>
                    <button className="btn btn-outline" onClick={() => setPage('mock')}><Ic path={I.timer} size={15} />Take Mock Test</button>
                    {ready && <button className="btn btn-primary" onClick={() => document.getElementById('companies')?.scrollIntoView({ behavior: 'smooth' })}><Ic path={I.building} size={15} />View Companies</button>}
                </div>
            </div>

            <div className="dashboard-grid">
                <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
                    {/* matched */}
                    <div className="card">
                        <div className="card-header">
                            <div className="card-title"><div className="card-title-icon" style={{ background: 'rgba(16,185,129,0.12)' }}>✅</div>Exact Match Skills</div>
                            <span className="badge badge-green">{matched_skills.length}</span>
                        </div>
                        <div className="badges-wrap">{matched_skills.map(s => <span key={s} className="badge badge-green">{s}</span>)}</div>
                    </div>

                    {/* Semantic Matches */}
                    {semantic_matches?.length > 0 && (
                        <div className="card">
                            <div className="card-header">
                                <div className="card-title"><div className="card-title-icon" style={{ background: 'rgba(6,182,212,0.12)' }}>🧠</div>Semantic Matches (Word2Vec)</div>
                                <span className="badge badge-cyan">{semantic_matches.length} found</span>
                            </div>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                                {semantic_matches.map((sm, i) => (
                                    <div key={i} className="skill-item" style={{background: 'var(--bg-elevated)', border: 'none'}}>
                                        <div>
                                            <span style={{fontWeight: 600, color: 'var(--text-primary)'}}>{sm.required_skill}</span>
                                            <span style={{fontSize: 13, color: 'var(--text-secondary)', marginLeft: 8}}>matched with <em>"{sm.user_skill}"</em></span>
                                        </div>
                                        <span className="badge badge-cyan" style={{fontSize: 11}}>Similarity: {Math.round(sm.similarity_score * 100)}%</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* missing */}
                    {missing_skills.length > 0 && (
                        <div className="card">
                            <div className="card-header">
                                <div className="card-title"><div className="card-title-icon" style={{ background: 'rgba(239,68,68,0.12)' }}>📌</div>Missing Skills</div>
                                <span className="badge badge-red">{missing_skills.length} gaps</span>
                            </div>
                            <div style={{ display: 'flex', flexDirection: 'column' }}>
                                {missing_skills.map((s, i) => (
                                    <div key={s} className="skill-item">
                                        <span className="skill-name">{s}</span>
                                        <span className="badge badge-red">To Learn</span>
                                    </div>
                                ))}
                            </div>
                            
                            {learning_topics?.length > 0 && (
                                <div style={{marginTop: 16, padding: '12px 14px', background: 'rgba(6,182,212,0.08)', borderRadius: 10, border: '1px solid rgba(6,182,212,0.2)'}}>
                                    <div style={{fontSize: 13, fontWeight: 700, color: '#06b6d4', marginBottom: 6}}>🧭 Suggested Learning Tracks (LDA Topic Modeling)</div>
                                    <ul style={{margin: 0, paddingLeft: 20, fontSize: 13, color: 'var(--text-secondary)'}}>
                                        {learning_topics.map((t, i) => <li key={i} style={{marginBottom: 4}}>{t}</li>)}
                                    </ul>
                                </div>
                            )}

                            <div style={{ marginTop: 16, padding: 14, background: 'rgba(99,102,241,0.08)', borderRadius: 10, border: '1px solid var(--border-active)', fontSize: 13, color: 'var(--text-secondary)' }}>
                                💡 Ask the <strong style={{ color: 'var(--accent)' }}>AI Career Mentor</strong> chatbot (bottom-right) for a step-by-step roadmap on how to learn these skills!
                            </div>
                        </div>
                    )}

                    {/* courses */}
                    {recommendations.length > 0 && (
                        <div className="card">
                            <div className="card-header">
                                <div className="card-title"><div className="card-title-icon" style={{ background: 'rgba(6,182,212,0.12)' }}>📚</div>Recommended Courses</div>
                            </div>
                            <div className="course-grid" style={{ gridTemplateColumns: '1fr' }}>
                                {recommendations.map((r, i) => (
                                    <div key={i} className="course-card">
                                        <div className="course-type course">{r.resource_type || 'Course'}</div>
                                        <div className="course-title">{r.title}</div>
                                        <div className="course-desc">{r.description}</div>
                                        <div className="course-footer">
                                            <span className="badge badge-accent" style={{ fontSize: 11 }}>{r.skill_name}</span>
                                            <a href={r.resource_url} target="_blank" rel="noopener noreferrer" className="course-link">
                                                Start Learning <Ic path={I.arrow} size={13} />
                                            </a>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                {/* right column */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
                    <div className="card" style={{ textAlign: 'center', padding: 32 }}>
                        <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 20 }}>Readiness Score</div>
                        <Circle pct={pct} size={150} />
                        <div style={{ marginTop: 20, color: 'var(--text-secondary)', fontSize: 13, lineHeight: 1.6 }}>
                            {ready ? '🎉 You have the proficiency needed. Apply to jobs now!' : `Your average proficiency is ${pct}%, which is lower than the recommended 70%.`}
                        </div>
                    </div>

                    <div className="card">
                        <div className="card-title" style={{ marginBottom: 16 }}>Quick Actions</div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                            <button className="btn btn-primary w-full" onClick={() => setPage('mock')}><Ic path={I.timer} size={15} />Take Mock Test</button>
                            <button className="btn btn-outline w-full" onClick={() => setPage('upload')}><Ic path={I.upload} size={15} />Re-upload Resume</button>
                            <button className="btn btn-outline w-full" onClick={() => setPage('roles')}><Ic path={I.search} size={15} />Change Role</button>
                        </div>
                    </div>
                </div>
            </div>

            {/* companies */}
            <div id="companies" style={{ marginTop: 32 }}>
                <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 16 }}>
                    {ready ? '🏢 Companies Hiring for ' : '🏢 Companies You Can Target After Upskilling — '}{role?.title}
                </h2>
                <div className="course-grid">
                    {companies.map(c => (
                        <div key={c.id} className="course-card">
                            <div style={{ fontSize: 28, marginBottom: 4 }}>🏢</div>
                            <div className="course-title">{c.name}</div>
                            <div className="course-desc">{c.description}</div>
                            <div className="course-footer">
                                <span className="badge badge-cyan" style={{ fontSize: 11 }}>📍 {c.location}</span>
                                <a href={c.apply_url} target="_blank" rel="noopener noreferrer" className="course-link">
                                    Apply Now <Ic path={I.arrow} size={13} />
                                </a>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

// ============ MOCK TEST PAGE ============
function MockPage({ role, setMockResult, setPage }) {
    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState({});
    const [timer, setTimer] = useState(600); // 10 min
    const [loading, setLoading] = useState(false);
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        if (!role) return;
        setLoading(true);
        fetch(`${API}/api/mock-test?job_id=${role.id}`).then(r => r.json()).then(q => { setQuestions(q); setLoading(false); }).catch(() => setLoading(false));
    }, [role]);

    useEffect(() => {
        if (!questions.length) return;
        const t = setInterval(() => setTimer(p => { if (p <= 1) { clearInterval(t); submitAnswers(); return 0; } return p - 1; }), 1000);
        return () => clearInterval(t);
    }, [questions.length]);

    const submitAnswers = async () => {
        if (submitting) return;
        setSubmitting(true);
        try {
            const r = await fetch(`${API}/api/mock-test/submit`, {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ answers, job_id: role?.id })
            });
            const d = await r.json();
            setMockResult(d);
            setPage('mock-results');
        } catch { alert('Submit failed. Check backend.'); setSubmitting(false); }
    };

    const mm = String(Math.floor(timer / 60)).padStart(2, '0');
    const ss = String(timer % 60).padStart(2, '0');
    const opts = ['A', 'B', 'C', 'D'];
    const optKeys = ['option_a', 'option_b', 'option_c', 'option_d'];

    if (!role) return <div className="empty-state fade-up"><div className="empty-icon">🎯</div><div className="empty-title">No Role Selected</div><button className="btn btn-primary mt-4" onClick={() => setPage('roles')}>Select a Role</button></div>;
    if (loading) return <div className="empty-state"><div style={{ fontSize: 40 }}>⏳</div><div className="empty-title">Loading Questions…</div></div>;
    if (!questions.length) return <div className="empty-state"><div className="empty-icon">📝</div><div className="empty-title">No Questions Found</div><div className="empty-desc">No mock questions available for this role yet.</div></div>;

    return (
        <div className="fade-up" style={{ maxWidth: 760, margin: '0 auto' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 28 }}>
                <div>
                    <h1 style={{ fontSize: 22, fontWeight: 800, letterSpacing: '-0.5px', marginBottom: 4 }}>Mock Test — {role.title}</h1>
                    <p style={{ color: 'var(--text-secondary)', fontSize: 14 }}>Answer all questions. Score ≥60% to pass.</p>
                </div>
                <div className={`badge ${timer < 60 ? 'badge-red' : 'badge-cyan'}`} style={{ fontSize: 16, padding: '10px 18px', fontFamily: 'monospace', fontWeight: 700 }}>
                    ⏱ {mm}:{ss}
                </div>
            </div>

            {/* progress */}
            <div style={{ marginBottom: 24 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: 'var(--text-secondary)', marginBottom: 6 }}>
                    <span>{Object.keys(answers).length} of {questions.length} answered</span>
                    <span>{Math.round((Object.keys(answers).length / questions.length) * 100)}%</span>
                </div>
                <div className="progress-bar-wrap"><div className="progress-bar-fill" style={{ width: `${(Object.keys(answers).length / questions.length) * 100}%` }} /></div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                {questions.map((q, qi) => (
                    <div key={q.id} className="card">
                        <div style={{ fontWeight: 600, fontSize: 14, marginBottom: 16 }}>Q{qi + 1}. {q.question}</div>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                            {opts.map((opt, oi) => {
                                const selected = answers[q.id] === opt;
                                return (
                                    <button key={opt} onClick={() => setAnswers({ ...answers, [q.id]: opt })} style={{
                                        padding: '12px 16px', borderRadius: 10, border: '1px solid', cursor: 'pointer',
                                        fontFamily: 'inherit', fontSize: 13, textAlign: 'left', transition: 'all 0.15s',
                                        background: selected ? 'var(--accent-glow)' : 'var(--bg-elevated)',
                                        borderColor: selected ? 'var(--accent)' : 'var(--border)',
                                        color: selected ? 'var(--accent)' : 'var(--text-primary)',
                                        fontWeight: selected ? 600 : 400,
                                    }}>
                                        <span style={{ fontWeight: 700, marginRight: 8 }}>{opt}.</span> {q[optKeys[oi]]}
                                    </button>
                                );
                            })}
                        </div>
                    </div>
                ))}
            </div>

            <button className="btn btn-primary btn-lg w-full" style={{ marginTop: 24 }} onClick={submitAnswers} disabled={submitting}>
                {submitting ? 'Submitting…' : `Submit Test (${Object.keys(answers).length}/${questions.length} answered)`}
            </button>
        </div>
    );
}

// ============ MOCK RESULTS PAGE ============
function MockResultPage({ result, role, setPage }) {
    if (!result) return <div className="empty-state fade-up"><div className="empty-icon">📝</div><div className="empty-title">No Test Results</div><button className="btn btn-primary mt-4" onClick={() => setPage('mock')}>Take Mock Test</button></div>;

    const { score, total, percentage, passed, feedback = [] } = result;

    return (
        <div className="fade-up" style={{ maxWidth: 760, margin: '0 auto' }}>
            {/* result banner */}
            <div className="card mb-6" style={{
                textAlign: 'center', padding: 40,
                background: passed
                    ? 'linear-gradient(135deg, rgba(16,185,129,0.15), rgba(6,182,212,0.08))'
                    : 'linear-gradient(135deg, rgba(239,68,68,0.12), rgba(245,158,11,0.08))',
                borderColor: passed ? 'rgba(16,185,129,0.3)' : 'rgba(239,68,68,0.3)',
            }}>
                <div style={{ fontSize: 60, marginBottom: 16 }}>{passed ? '🏆' : '📚'}</div>
                <h1 style={{ fontSize: 28, fontWeight: 800, letterSpacing: '-1px', marginBottom: 8 }}>
                    {passed ? 'You Passed!' : 'Keep Learning!'}
                </h1>
                <div style={{ fontSize: 48, fontWeight: 900, letterSpacing: '-2px', color: passed ? '#10b981' : '#ef4444', marginBottom: 8 }}>
                    {score}/{total}
                </div>
                <div style={{ fontSize: 16, color: 'var(--text-secondary)', marginBottom: 20 }}>{percentage}% score</div>
                <span className={`badge ${passed ? 'badge-green' : 'badge-red'}`} style={{ fontSize: 14, padding: '8px 20px' }}>
                    {passed ? '✅ Eligible for the Role' : '🔶 Not yet eligible — practice more'}
                </span>
            </div>

            {/* feedback */}
            <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 16 }}>Question Review</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 24 }}>
                {feedback.map((f, i) => (
                    <div key={i} className="card" style={{ borderColor: f.is_correct ? 'rgba(16,185,129,0.25)' : 'rgba(239,68,68,0.25)' }}>
                        <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                            <span style={{ fontSize: 18, marginTop: 2 }}>{f.is_correct ? '✅' : '❌'}</span>
                            <div style={{ flex: 1 }}>
                                <div style={{ fontWeight: 600, marginBottom: 8, fontSize: 13 }}>Question {i + 1}</div>
                                <div style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 6 }}>
                                    Your answer: <strong style={{ color: f.is_correct ? '#10b981' : '#ef4444' }}>{f.your_answer}</strong>
                                    {!f.is_correct && <> &nbsp;|&nbsp; Correct: <strong style={{ color: '#10b981' }}>{f.correct_answer}</strong></>}
                                </div>
                                {f.explanation && <div style={{ fontSize: 12.5, color: 'var(--text-secondary)', background: 'var(--bg-elevated)', padding: '8px 12px', borderRadius: 8 }}>💡 {f.explanation}</div>}
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <div style={{ display: 'flex', gap: 12 }}>
                <button className="btn btn-outline" onClick={() => setPage('mock')}><Ic path={I.timer} size={15} />Retry Test</button>
                <button className="btn btn-primary" onClick={() => setPage('results')}><Ic path={I.trophy} size={15} />Back to Results</button>
            </div>
        </div>
    );
}
