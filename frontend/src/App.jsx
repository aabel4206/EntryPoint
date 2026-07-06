import { useEffect, useState } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8001";

function App() {
  const [profileId, setProfileId] = useState(null);
  const [resources, setResources] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [monitoredPages, setMonitoredPages] = useState([]);
  const [changes, setChanges] = useState([]);
  const [status, setStatus] = useState("");

  async function createDemoStudent() {
    const res = await fetch(`${API_BASE}/api/demo/student`, { method: "POST" });
    const data = await res.json();
    setProfileId(data.profile_id);
    setStatus(`Demo international student loaded. Profile ID: ${data.profile_id}`);
  }

  async function loadResources() {
    const res = await fetch(`${API_BASE}/api/resources/`);
    const data = await res.json();
    setResources(data);
  }

  async function loadNotifications(id = profileId) {
    if (!id) return;
    const res = await fetch(`${API_BASE}/api/notifications/${id}`);
    const data = await res.json();
    setNotifications(data);
  }

  async function loadMonitoringData() {
    const pagesRes = await fetch(`${API_BASE}/api/monitoring/pages`);
    const pagesData = await pagesRes.json();
    setMonitoredPages(pagesData);

    const changesRes = await fetch(`${API_BASE}/api/monitoring/changes`);
    const changesData = await changesRes.json();
    setChanges(changesData);
  }

  async function subscribe(resourceId) {
    if (!profileId) {
      setStatus("Load the demo student first.");
      return;
    }

    const res = await fetch(`${API_BASE}/api/subscriptions/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        profile_id: profileId,
        resource_id: resourceId,
      }),
    });

    const data = await res.json();
    setStatus(`Subscribed to resource ID ${data.resource_id}.`);
  }

  async function addMonitoredPage(resource) {
    const res = await fetch(`${API_BASE}/api/monitoring/pages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        resource_id: resource.resource_id,
        category_id: resource.category_id,
        title: resource.title,
        url: resource.url,
      }),
    });

    const data = await res.json();
    setStatus(`Monitoring enabled for ${data.title}.`);
    loadMonitoringData();
  }

  async function checkPage(pageId) {
    const res = await fetch(`${API_BASE}/api/monitoring/check/${pageId}`, {
      method: "POST",
    });

    const data = await res.json();
    setStatus(
      data.changed
        ? `Change detected. Notifications created: ${data.created_notifications.length}`
        : data.message
    );

    loadMonitoringData();
    loadNotifications();
  }

  useEffect(() => {
    loadResources();
    loadMonitoringData();
  }, []);

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">E</div>
          <div>
            <h1>EntryPoint</h1>
            <p>Personalized onboarding</p>
          </div>
        </div>

        <nav>
          <a href="#dashboard">Dashboard</a>
          <a href="#transportation">Transportation</a>
          <a href="#accommodation">Accommodation</a>
          <a href="#monitoring">Monitoring</a>
          <a href="#notifications">Notifications</a>
          <a href="#evaluation">Evaluation</a>
        </nav>
      </aside>

      <main className="main">
        <section id="dashboard" className="hero">
          <div>
            <p className="eyebrow">International Student Pilot</p>
            <h2>Personalized onboarding that adapts to each student.</h2>
            <p>
              EntryPoint connects student needs, onboarding resources, webpage monitoring,
              and personalized notifications into one framework.
            </p>
            <button onClick={createDemoStudent}>Load Demo Student</button>
            {profileId && <span className="pill">Profile ID: {profileId}</span>}
          </div>

          <div className="hero-card">
            <h3>Framework Flow</h3>
            <p>Student → Resource Subscription → Monitoring → Notification</p>
          </div>
        </section>

        <section id="transportation" className="section">
          <div className="section-header">
            <div>
              <p className="eyebrow">Pilot Domain</p>
              <h2>Transportation Onboarding</h2>
            </div>
          </div>

          <div className="checklist">
            <div>✓ Learn Bobcat Shuttle system</div>
            <div>✓ Review campus maps</div>
            <div>✓ Understand ride-sharing options</div>
            <div>✓ Review transportation safety</div>
            <div>✓ Review Texas driver license information</div>
          </div>

          <div className="grid">
            {resources.map((resource) => (
              <div className="card" key={resource.resource_id}>
                <h3>{resource.title}</h3>
                <p>{resource.description}</p>
                <a href={resource.url} target="_blank" rel="noreferrer">
                  Open official resource
                </a>
                <div className="actions">
                  <button onClick={() => subscribe(resource.resource_id)}>
                    Subscribe
                  </button>
                  <button className="secondary" onClick={() => addMonitoredPage(resource)}>
                    Monitor
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section id="accommodation" className="section">
          <p className="eyebrow">Scalability Domain</p>
          <h2>Accommodation Onboarding</h2>
          <p>
            The same framework can scale beyond transportation by replacing the domain
            resources, templates, and monitored webpages.
          </p>

          <div className="grid">
            {[
              "Residence Life",
              "Off-Campus Housing",
              "Lease Guidance",
              "Utilities Setup",
              "Move-In Checklist",
              "Roommate Guidance",
            ].map((item) => (
              <div className="card mini" key={item}>
                <h3>{item}</h3>
                <p>Accommodation onboarding module example.</p>
              </div>
            ))}
          </div>
        </section>

        <section id="monitoring" className="section">
          <p className="eyebrow">Automatic Monitoring</p>
          <h2>Monitored Pages</h2>

          <div className="grid">
            {monitoredPages.map((page) => (
              <div className="card" key={page.page_id}>
                <h3>{page.title}</h3>
                <p>{page.url}</p>
                <p className="muted">
                  Last checked: {page.last_checked_at || "Not checked yet"}
                </p>
                <button onClick={() => checkPage(page.page_id)}>
                  Check for Updates
                </button>
              </div>
            ))}
          </div>

          <h3 className="subheading">Change History</h3>
          {changes.length === 0 ? (
            <p className="muted">No detected changes yet.</p>
          ) : (
            changes.map((change) => (
              <div className="notice" key={change.change_id}>
                <strong>Change #{change.change_id}</strong>
                <p>{change.change_summary}</p>
                <small>{change.detected_at}</small>
              </div>
            ))
          )}
        </section>

        <section id="notifications" className="section">
          <div className="section-header">
            <div>
              <p className="eyebrow">Personalized Alerts</p>
              <h2>Student Notifications</h2>
            </div>
            <button onClick={() => loadNotifications()}>Refresh Notifications</button>
          </div>

          {notifications.length === 0 ? (
            <p className="muted">No notifications yet.</p>
          ) : (
            notifications.map((notification) => (
              <div className="notice" key={notification.notification_id}>
                <strong>{notification.title}</strong>
                <p>{notification.message}</p>
                <small>
                  Read: {notification.is_read ? "Yes" : "No"} · {notification.created_at}
                </small>
              </div>
            ))
          )}
        </section>

        <section id="evaluation" className="section">
          <p className="eyebrow">Research Evaluation</p>
          <h2>Student Feedback</h2>
          <p>
            Participants compare existing Texas State webpages with EntryPoint and
            provide feedback on ease of use, clarity, confidence, and preference.
          </p>
          <a className="survey-button" href="#" target="_blank" rel="noreferrer">
            Complete Feedback Survey
          </a>
        </section>

        {status && <div className="toast">{status}</div>}
      </main>
    </div>
  );
}

export default App;