import { useState } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8001";

function App() {
  const [profileId, setProfileId] = useState(null);
  const [resources, setResources] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [message, setMessage] = useState("");

  async function createDemoStudent() {
    const res = await fetch(`${API_BASE}/api/demo/student`, {
      method: "POST",
    });
    const data = await res.json();
    setProfileId(data.profile_id);
    setMessage(`Demo international student loaded. Profile ID: ${data.profile_id}`);
  }

  async function loadResources() {
    const res = await fetch(`${API_BASE}/api/resources/`);
    const data = await res.json();
    setResources(data);
    setMessage("Transportation resources loaded.");
  }

  async function subscribe(resourceId) {
    if (!profileId) {
      setMessage("Create/load demo student first.");
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
    setMessage(`Subscribed to resource ID ${data.resource_id}.`);
  }

  async function simulateChange(resourceId) {
    const res = await fetch(`${API_BASE}/api/monitoring/demo-change/${resourceId}`, {
      method: "POST",
    });

    const data = await res.json();
    setMessage(
      `Change simulated for ${data.resource_title}. Notifications created: ${data.created_notifications.length}`
    );
  }

  async function loadNotifications() {
    if (!profileId) {
      setMessage("Create/load demo student first.");
      return;
    }

    const res = await fetch(`${API_BASE}/api/notifications/${profileId}`);
    const data = await res.json();
    setNotifications(data);
    setMessage("Notifications loaded.");
  }

  return (
    <div className="page">
      <h1>EntryPoint</h1>
      <h2>Personalized Onboarding Framework</h2>
      <p className="subtitle">
        Transportation pilot with accommodation scalability.
      </p>

      <section className="card">
        <h3>1. Demo Student</h3>
        <p>
          Load a demo international student profile to test personalized onboarding.
        </p>
        <button onClick={createDemoStudent}>Load Demo International Student</button>
        {profileId && <p>Current Profile ID: {profileId}</p>}
      </section>

      <section className="card">
        <h3>2. Transportation Resources</h3>
        <p>
          These resources come from the FastAPI backend and PostgreSQL database.
        </p>
        <button onClick={loadResources}>Load Resources</button>

        <div className="resource-list">
          {resources.map((resource) => (
            <div key={resource.resource_id} className="resource">
              <h4>{resource.title}</h4>
              <p>{resource.description}</p>
              <a href={resource.url} target="_blank" rel="noreferrer">
                Open Resource
              </a>
              <div className="button-row">
                <button onClick={() => subscribe(resource.resource_id)}>
                  Subscribe
                </button>
                <button onClick={() => simulateChange(resource.resource_id)}>
                  Simulate Change
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="card">
        <h3>3. Personalized Notifications</h3>
        <p>
          If a subscribed transportation resource changes, the student receives a
          personalized notification.
        </p>
        <button onClick={loadNotifications}>Load Notifications</button>

        {notifications.map((notification) => (
          <div key={notification.notification_id} className="notification">
            <strong>{notification.title}</strong>
            <p>{notification.message}</p>
            <small>Read: {notification.is_read ? "Yes" : "No"}</small>
          </div>
        ))}
      </section>

      <section className="card">
        <h3>4. Accommodation Scalability Example</h3>
        <p>
          The same framework can later support accommodation onboarding by
          replacing transportation resources with housing resources, lease
          information, move-in requirements, utilities, and roommate guidance.
        </p>
        <ul>
          <li>Residence Life</li>
          <li>Off-Campus Housing</li>
          <li>Lease and utility guidance</li>
          <li>Move-in checklist</li>
        </ul>
      </section>

      <section className="card">
        <h3>5. Feedback</h3>
        <p>
          After testing EntryPoint, students can complete a short feedback survey
          comparing this framework to existing university webpages.
        </p>
      </section>

      {message && <p className="status">{message}</p>}
    </div>
  );
}

export default App;