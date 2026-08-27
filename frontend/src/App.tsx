import {
  Activity,
  Archive,
  BarChart3,
  FlaskConical,
  LayoutDashboard,
  ShieldCheck,
  Waypoints,
} from 'lucide-react'
import { NavLink, Route, Routes } from 'react-router-dom'
import { ArtifactsPage } from './pages/ArtifactsPage'
import { ComparePage } from './pages/ComparePage'
import { DashboardPage } from './pages/DashboardPage'
import { NewExperimentPage } from './pages/NewExperimentPage'
import { RunsPage } from './pages/RunsPage'

const navItems = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/new-experiment', label: 'New Experiment', icon: FlaskConical },
  { to: '/runs', label: 'Runs', icon: Activity },
  { to: '/compare', label: 'Compare', icon: BarChart3 },
  { to: '/artifacts', label: 'Artifacts', icon: Archive },
]

export default function App() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark" aria-hidden="true">
            <Waypoints size={22} strokeWidth={1.9} />
          </div>
          <div>
            <div className="brand-title">Resilient Agents</div>
            <div className="brand-subtitle">Thesis research lab</div>
          </div>
        </div>

        <nav className="primary-nav" aria-label="Primary navigation">
          {navItems.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) => `nav-link${isActive ? ' is-active' : ''}`}
            >
              <Icon size={18} strokeWidth={1.8} aria-hidden="true" />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-note">
          <ShieldCheck size={18} aria-hidden="true" />
          <div>
            <strong>Evidence-safe UI</strong>
            <span>Scientific execution remains in the validated Python core.</span>
          </div>
        </div>
      </aside>

      <main className="main-column">
        <header className="topbar">
          <div className="topbar-context">
            <span className="eyebrow">Pre-WP7 application refinement</span>
            <span className="topbar-separator" aria-hidden="true" />
            <span className="topbar-context-text">Protocol v1.1 candidate</span>
          </div>
          <div
            className="topbar-status"
            title="Writing/defense work remains blocked until explicit approval"
          >
            <span className="status-dot status-dot-warning" aria-hidden="true" />
            WP7 blocked
          </div>
        </header>

        <div className="page-frame">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/new-experiment" element={<NewExperimentPage />} />
            <Route path="/runs" element={<RunsPage />} />
            <Route path="/compare" element={<ComparePage />} />
            <Route path="/artifacts" element={<ArtifactsPage />} />
            <Route
              path="*"
              element={
                <section className="panel">
                  <span className="section-kicker">Navigation</span>
                  <h1>Page not found</h1>
                  <p>The requested application route does not exist.</p>
                  <NavLink className="button button-primary" to="/">
                    Return to Dashboard
                  </NavLink>
                </section>
              }
            />
          </Routes>
        </div>
      </main>
    </div>
  )
}
