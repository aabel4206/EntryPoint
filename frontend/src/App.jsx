import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8001";

const navigationItems = [
  { id: "dashboard", label: "Dashboard", icon: "⌂" },
  { id: "transportation", label: "Transportation", icon: "↗" },
  { id: "accommodation", label: "Accommodation", icon: "⌁" },
  { id: "monitoring", label: "Monitoring", icon: "◎" },
  { id: "notifications", label: "Notifications", icon: "◌" },
  { id: "evaluation", label: "Evaluation", icon: "✓" },
];

const transportationChecklist = [
  "Learn the Bobcat Shuttle system",
  "Review campus transportation maps",
  "Understand ride-sharing options",
  "Review transportation safety information",
  "Review Texas driver-license information",
];

const accommodationModules = [
  {
    title: "Residence Life",
    description:
      "Explore university housing, residence halls, policies, and important contacts.",
    icon: "⌂",
  },
  {
    title: "Off-Campus Housing",
    description:
      "Compare off-campus options and find official housing-support resources.",
    icon: "⌖",
  },
  {
    title: "Lease Guidance",
    description:
      "Understand common lease terms, deposits, responsibilities, and warning signs.",
    icon: "▤",
  },
  {
    title: "Utilities Setup",
    description:
      "Learn how to arrange electricity, water, internet, and other essential services.",
    icon: "ϟ",
  },
  {
    title: "Move-In Checklist",
    description:
      "Follow a structured checklist for a smoother and more organized move-in.",
    icon: "✓",
  },
  {
    title: "Roommate Guidance",
    description:
      "Review communication, shared-expense, and conflict-prevention guidance.",
    icon: "♢",
  },
];

function formatDate(value) {
  if (!value) {
    return "Not checked yet";
  }

  const parsedDate = new Date(value);

  if (Number.isNaN(parsedDate.getTime())) {
    return value;
  }

  return parsedDate.toLocaleString([], {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

function App() {
  const [profileId, setProfileId] = useState(null);
  const [resources, setResources] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [monitoredPages, setMonitoredPages] = useState([]);
  const [changes, setChanges] = useState([]);
  const [status, setStatus] = useState("");
  const [statusType, setStatusType] = useState("success");
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState("");
  const [activeSection, setActiveSection] = useState("dashboard");
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const unreadNotifications = useMemo(
    () => notifications.filter((notification) => !notification.is_read).length,
    [notifications]
  );

  const onboardingProgress = profileId ? 60 : 20;

  function showStatus(message, type = "success") {
    setStatus(message);
    setStatusType(type);

    window.clearTimeout(showStatus.timeoutId);
    showStatus.timeoutId = window.setTimeout(() => {
      setStatus("");
    }, 4500);
  }

  async function request(url, options = {}) {
    const response = await fetch(url, options);

    let data = null;

    try {
      data = await response.json();
    } catch {
      data = null;
    }

    if (!response.ok) {
      const message =
        data?.detail ||
        data?.message ||
        `The request failed with status ${response.status}.`;

      throw new Error(message);
    }

    return data;
  }

  async function createDemoStudent() {
    setActionLoading("profile");

    try {
      const data = await request(`${API_BASE}/api/demo/student`, {
        method: "POST",
      });

      setProfileId(data.profile_id);

      await loadNotifications(data.profile_id);

      showStatus("International student demo profile loaded.");
    } catch (error) {
      showStatus(error.message, "error");
    } finally {
      setActionLoading("");
    }
  }

  async function loadResources() {
    try {
      const data = await request(`${API_BASE}/api/resources/`);
      setResources(Array.isArray(data) ? data : []);
    } catch (error) {
      showStatus(`Resources could not be loaded: ${error.message}`, "error");
    }
  }

  async function loadNotifications(id = profileId) {
    if (!id) {
      showStatus("Load the student profile before viewing notifications.", "info");
      return;
    }

    setActionLoading("notifications");

    try {
      const data = await request(`${API_BASE}/api/notifications/${id}`);
      setNotifications(Array.isArray(data) ? data : []);
    } catch (error) {
      showStatus(`Notifications could not be loaded: ${error.message}`, "error");
    } finally {
      setActionLoading("");
    }
  }

  async function loadMonitoringData() {
    try {
      const [pagesData, changesData] = await Promise.all([
        request(`${API_BASE}/api/monitoring/pages`),
        request(`${API_BASE}/api/monitoring/changes`),
      ]);

      setMonitoredPages(Array.isArray(pagesData) ? pagesData : []);
      setChanges(Array.isArray(changesData) ? changesData : []);
    } catch (error) {
      showStatus(`Monitoring data could not be loaded: ${error.message}`, "error");
    }
  }

  async function subscribe(resourceId, resourceTitle) {
    if (!profileId) {
      showStatus("Load the demo student before subscribing.", "info");
      scrollToSection("dashboard");
      return;
    }

    setActionLoading(`subscribe-${resourceId}`);

    try {
      await request(`${API_BASE}/api/subscriptions/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          profile_id: profileId,
          resource_id: resourceId,
        }),
      });

      showStatus(`Subscribed to ${resourceTitle}.`);
    } catch (error) {
      showStatus(error.message, "error");
    } finally {
      setActionLoading("");
    }
  }

  async function addMonitoredPage(resource) {
    setActionLoading(`monitor-${resource.resource_id}`);

    try {
      await request(`${API_BASE}/api/monitoring/pages`, {
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

      await loadMonitoringData();
      showStatus(`Monitoring enabled for ${resource.title}.`);
    } catch (error) {
      showStatus(error.message, "error");
    } finally {
      setActionLoading("");
    }
  }

  async function checkPage(pageId, pageTitle) {
    setActionLoading(`check-${pageId}`);

    try {
      const data = await request(
        `${API_BASE}/api/monitoring/check/${pageId}`,
        {
          method: "POST",
        }
      );

      await Promise.all([
        loadMonitoringData(),
        profileId ? loadNotifications(profileId) : Promise.resolve(),
      ]);

      if (data.changed) {
        const notificationCount = data.created_notifications?.length || 0;

        showStatus(
          `${pageTitle} changed. ${notificationCount} personalized notification${
            notificationCount === 1 ? "" : "s"
          } created.`
        );
      } else {
        showStatus(data.message || `${pageTitle} has no new changes.`, "info");
      }
    } catch (error) {
      showStatus(error.message, "error");
    } finally {
      setActionLoading("");
    }
  }

  function scrollToSection(sectionId) {
    setActiveSection(sectionId);
    setMobileMenuOpen(false);

    document
      .getElementById(sectionId)
      ?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  useEffect(() => {
    async function initialize() {
      setLoading(true);

      await Promise.all([loadResources(), loadMonitoringData()]);

      setLoading(false);
    }

    initialize();
  }, []);

  useEffect(() => {
    const sections = navigationItems
      .map((item) => document.getElementById(item.id))
      .filter(Boolean);

    const observer = new IntersectionObserver(
      (entries) => {
        const visibleSection = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

        if (visibleSection) {
          setActiveSection(visibleSection.target.id);
        }
      },
      {
        rootMargin: "-25% 0px -60% 0px",
        threshold: [0.05, 0.25, 0.5],
      }
    );

    sections.forEach((section) => observer.observe(section));

    return () => observer.disconnect();
  }, [loading]);

  return (
    <div className="app-shell">
      <button
        type="button"
        className="mobile-menu-button"
        onClick={() => setMobileMenuOpen((current) => !current)}
        aria-label="Toggle navigation"
      >
        <span />
        <span />
        <span />
      </button>

      <aside className={`sidebar ${mobileMenuOpen ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-icon">E</div>

          <div className="brand-copy">
            <h1>EntryPoint</h1>
            <p>Student onboarding</p>
          </div>
        </div>

        <div className="sidebar-context">
          <span className="context-label">Research prototype</span>
          <strong>Texas State University</strong>
          <p>International student pilot</p>
        </div>

        <nav className="sidebar-nav" aria-label="Primary navigation">
          {navigationItems.map((item) => (
            <button
              type="button"
              key={item.id}
              className={`nav-link ${
                activeSection === item.id ? "nav-link-active" : ""
              }`}
              onClick={() => scrollToSection(item.id)}
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>

              {item.id === "notifications" && unreadNotifications > 0 && (
                <span className="nav-badge">{unreadNotifications}</span>
              )}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div
            className={`system-indicator ${
              loading ? "system-loading" : "system-ready"
            }`}
          />

          <div>
            <strong>{loading ? "Connecting…" : "System ready"}</strong>
            <span>FastAPI · PostgreSQL · Ollama</span>
          </div>
        </div>
      </aside>

      {mobileMenuOpen && (
        <button
          type="button"
          className="mobile-overlay"
          aria-label="Close navigation"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      <main className="main-content">
        <section id="dashboard" className="hero-section">
          <div className="hero-background-orb hero-orb-one" />
          <div className="hero-background-orb hero-orb-two" />

          <div className="hero-content">
            <div className="hero-copy">
              <div className="eyebrow">
                <span className="eyebrow-dot" />
                International Student Pilot
              </div>

              <h2>
                University onboarding,
                <span> personalized around the student.</span>
              </h2>

              <p className="hero-description">
                EntryPoint organizes official resources, adapts onboarding
                guidance to student needs, monitors changing webpages, and
                delivers understandable AI-assisted updates.
              </p>

              <div className="hero-actions">
                <button
                  type="button"
                  className="button button-primary"
                  onClick={createDemoStudent}
                  disabled={actionLoading === "profile"}
                >
                  {actionLoading === "profile"
                    ? "Loading profile…"
                    : profileId
                      ? "Reload Demo Profile"
                      : "Start Demo Experience"}
                </button>

                <button
                  type="button"
                  className="button button-ghost"
                  onClick={() => scrollToSection("transportation")}
                >
                  Explore onboarding
                  <span aria-hidden="true">→</span>
                </button>
              </div>

              <div className="hero-trust-row">
                <span>✓ Official resources</span>
                <span>✓ Personalized guidance</span>
                <span>✓ Local AI summaries</span>
              </div>
            </div>

            <div className="student-profile-card">
              <div className="profile-card-header">
                <div className="profile-avatar">IS</div>

                <div>
                  <span className="profile-status">
                    {profileId ? "Profile active" : "Demo profile"}
                  </span>
                  <h3>International Student</h3>
                  <p>Texas State onboarding profile</p>
                </div>
              </div>

              <div className="progress-header">
                <span>Onboarding progress</span>
                <strong>{onboardingProgress}%</strong>
              </div>

              <div
                className="progress-track"
                role="progressbar"
                aria-valuemin="0"
                aria-valuemax="100"
                aria-valuenow={onboardingProgress}
              >
                <div
                  className="progress-fill"
                  style={{ width: `${onboardingProgress}%` }}
                />
              </div>

              <div className="profile-details">
                <div>
                  <span>Profile ID</span>
                  <strong>{profileId || "Not loaded"}</strong>
                </div>

                <div>
                  <span>Primary domain</span>
                  <strong>Transportation</strong>
                </div>

                <div>
                  <span>Subscriptions</span>
                  <strong>{profileId ? "Ready" : "Profile required"}</strong>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="metrics-grid" aria-label="System summary">
          <article className="metric-card">
            <div className="metric-icon">◇</div>
            <div>
              <span>Available resources</span>
              <strong>{resources.length}</strong>
              <p>Official onboarding links</p>
            </div>
          </article>

          <article className="metric-card">
            <div className="metric-icon">◎</div>
            <div>
              <span>Monitored pages</span>
              <strong>{monitoredPages.length}</strong>
              <p>Automated change tracking</p>
            </div>
          </article>

          <article className="metric-card">
            <div className="metric-icon">◌</div>
            <div>
              <span>Notifications</span>
              <strong>{notifications.length}</strong>
              <p>{unreadNotifications} currently unread</p>
            </div>
          </article>

          <article className="metric-card">
            <div className="metric-icon">✦</div>
            <div>
              <span>AI summaries</span>
              <strong>{changes.length}</strong>
              <p>Generated locally with Ollama</p>
            </div>
          </article>
        </section>

        <section id="transportation" className="page-section">
          <div className="section-heading-row">
            <div>
              <div className="eyebrow">Pilot Domain</div>
              <h2>Transportation onboarding</h2>
              <p>
                A structured starting point for navigating transportation at
                Texas State and in the surrounding community.
              </p>
            </div>

            <span className="section-status">
              <span />
              Pilot implemented
            </span>
          </div>

          <div className="onboarding-layout">
            <div className="checklist-panel">
              <div className="panel-heading">
                <div>
                  <span className="panel-label">Personalized checklist</span>
                  <h3>Your transportation pathway</h3>
                </div>

                <span className="completion-badge">
                  {transportationChecklist.length} steps
                </span>
              </div>

              <div className="checklist-list">
                {transportationChecklist.map((item, index) => (
                  <div className="checklist-item" key={item}>
                    <span className="checklist-number">{index + 1}</span>

                    <div>
                      <strong>{item}</strong>
                      <p>
                        Recommended for a newly arriving international student.
                      </p>
                    </div>

                    <span className="checklist-check">✓</span>
                  </div>
                ))}
              </div>
            </div>

            <aside className="journey-panel">
              <span className="panel-label">How EntryPoint works</span>
              <h3>A complete information journey</h3>

              <div className="journey-steps">
                {[
                  ["01", "Personalize", "Identify the student’s needs."],
                  ["02", "Guide", "Recommend relevant official resources."],
                  ["03", "Monitor", "Track subscribed webpages for changes."],
                  ["04", "Notify", "Explain updates in clear language."],
                ].map(([number, title, description]) => (
                  <div className="journey-step" key={number}>
                    <span>{number}</span>
                    <div>
                      <strong>{title}</strong>
                      <p>{description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </aside>
          </div>

          <div className="subsection-heading">
            <div>
              <span className="panel-label">Recommended resources</span>
              <h3>Official transportation information</h3>
            </div>

            <p>{resources.length} resources available</p>
          </div>

          {loading ? (
            <div className="resource-grid">
              {[1, 2, 3, 4].map((item) => (
                <div className="skeleton-card" key={item}>
                  <div className="skeleton skeleton-short" />
                  <div className="skeleton skeleton-title" />
                  <div className="skeleton skeleton-line" />
                  <div className="skeleton skeleton-line" />
                  <div className="skeleton skeleton-button" />
                </div>
              ))}
            </div>
          ) : resources.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">◇</div>
              <h3>No transportation resources found</h3>
              <p>
                Confirm that the backend is running and that resources have been
                added to the database.
              </p>
            </div>
          ) : (
            <div className="resource-grid">
              {resources.map((resource, index) => (
                <article className="resource-card" key={resource.resource_id}>
                  <div className="resource-card-top">
                    <div className="resource-icon">
                      {["↗", "⌖", "◇", "◎"][index % 4]}
                    </div>

                    <span className="official-badge">Official resource</span>
                  </div>

                  <h3>{resource.title}</h3>
                  <p>{resource.description}</p>

                  <a
                    className="resource-link"
                    href={resource.url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Visit official webpage
                    <span aria-hidden="true">↗</span>
                  </a>

                  <div className="card-actions">
                    <button
                      type="button"
                      className="button button-primary button-small"
                      onClick={() =>
                        subscribe(resource.resource_id, resource.title)
                      }
                      disabled={
                        actionLoading ===
                        `subscribe-${resource.resource_id}`
                      }
                    >
                      {actionLoading ===
                      `subscribe-${resource.resource_id}`
                        ? "Subscribing…"
                        : "Subscribe"}
                    </button>

                    <button
                      type="button"
                      className="button button-secondary button-small"
                      onClick={() => addMonitoredPage(resource)}
                      disabled={
                        actionLoading === `monitor-${resource.resource_id}`
                      }
                    >
                      {actionLoading === `monitor-${resource.resource_id}`
                        ? "Enabling…"
                        : "Monitor updates"}
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        <section id="accommodation" className="page-section">
          <div className="section-heading-row">
            <div>
              <div className="eyebrow">Scalability Demonstration</div>
              <h2>Accommodation onboarding</h2>
              <p>
                The same architecture can support another onboarding domain by
                replacing resource content, checklist templates, and monitored
                webpages.
              </p>
            </div>

            <span className="section-status section-status-secondary">
              Framework extension
            </span>
          </div>

          <div className="scalability-callout">
            <div className="callout-icon">↗</div>

            <div>
              <span>Reusable framework</span>
              <h3>One architecture, multiple onboarding domains</h3>
              <p>
                Student profiles, resource recommendations, subscriptions,
                monitoring, AI summaries, and notifications can all be reused
                without rebuilding the entire application.
              </p>
            </div>
          </div>

          <div className="module-grid">
            {accommodationModules.map((module) => (
              <article className="module-card" key={module.title}>
                <div className="module-icon">{module.icon}</div>
                <h3>{module.title}</h3>
                <p>{module.description}</p>
                <span>Scalability module</span>
              </article>
            ))}
          </div>
        </section>

        <section id="monitoring" className="page-section">
          <div className="section-heading-row">
            <div>
              <div className="eyebrow">Automated Monitoring</div>
              <h2>Webpage change tracking</h2>
              <p>
                EntryPoint periodically compares official webpage content and
                records meaningful changes for subscribed students.
              </p>
            </div>

            <button
              type="button"
              className="button button-secondary"
              onClick={loadMonitoringData}
            >
              Refresh monitoring
            </button>
          </div>

          <div className="monitor-summary">
            <div>
              <span className="monitor-live-dot" />
              <strong>Monitoring service active</strong>
              <p>
                SHA-256 comparison with local AI-assisted change summarization
              </p>
            </div>

            <div className="monitor-summary-stats">
              <div>
                <span>Pages</span>
                <strong>{monitoredPages.length}</strong>
              </div>

              <div>
                <span>Changes</span>
                <strong>{changes.length}</strong>
              </div>
            </div>
          </div>

          {monitoredPages.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">◎</div>
              <h3>No webpages are being monitored</h3>
              <p>
                Choose “Monitor updates” on a transportation resource to add it
                here.
              </p>
            </div>
          ) : (
            <div className="monitoring-grid">
              {monitoredPages.map((page) => (
                <article className="monitor-card" key={page.page_id}>
                  <div className="monitor-card-header">
                    <div className="monitor-icon">◎</div>
                    <span className="monitoring-badge">
                      <span />
                      Monitoring
                    </span>
                  </div>

                  <h3>{page.title}</h3>

                  <div className="monitor-details">
                    <div>
                      <span>Last checked</span>
                      <strong>{formatDate(page.last_checked_at)}</strong>
                    </div>

                    <div>
                      <span>Resource ID</span>
                      <strong>{page.resource_id}</strong>
                    </div>
                  </div>

                  <a
                    href={page.url}
                    target="_blank"
                    rel="noreferrer"
                    className="subtle-link"
                  >
                    Open monitored webpage ↗
                  </a>

                  <button
                    type="button"
                    className="button button-primary button-full"
                    onClick={() => checkPage(page.page_id, page.title)}
                    disabled={actionLoading === `check-${page.page_id}`}
                  >
                    {actionLoading === `check-${page.page_id}`
                      ? "Checking webpage…"
                      : "Check for updates"}
                  </button>
                </article>
              ))}
            </div>
          )}

          <div className="subsection-heading change-history-heading">
            <div>
              <span className="panel-label">Change history</span>
              <h3>AI-assisted update summaries</h3>
            </div>

            <p>{changes.length} recorded changes</p>
          </div>

          {changes.length === 0 ? (
            <div className="empty-state compact-empty-state">
              <div className="empty-state-icon">✦</div>
              <h3>No changes detected yet</h3>
              <p>
                When monitored content changes, the generated summary will
                appear here.
              </p>
            </div>
          ) : (
            <div className="change-list">
              {changes.map((change) => (
                <article className="change-card" key={change.change_id}>
                  <div className="change-card-icon">✦</div>

                  <div className="change-card-content">
                    <div className="change-card-heading">
                      <div>
                        <span className="ai-badge">Local AI summary</span>
                        <h3>Detected webpage update</h3>
                      </div>

                      <time>{formatDate(change.detected_at)}</time>
                    </div>

                    <p>{change.change_summary}</p>

                    <div className="change-meta">
                      <span>Change #{change.change_id}</span>
                      <span>Generated with Ollama</span>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        <section id="notifications" className="page-section">
          <div className="section-heading-row">
            <div>
              <div className="eyebrow">Personalized Alerts</div>
              <h2>Student notifications</h2>
              <p>
                Students receive concise updates only for resources to which
                they have subscribed.
              </p>
            </div>

            <button
              type="button"
              className="button button-secondary"
              onClick={() => loadNotifications()}
              disabled={actionLoading === "notifications"}
            >
              {actionLoading === "notifications"
                ? "Refreshing…"
                : "Refresh notifications"}
            </button>
          </div>

          {!profileId ? (
            <div className="empty-state notification-empty-state">
              <div className="empty-state-icon">◌</div>
              <h3>Load the demo profile first</h3>
              <p>
                A student profile is required before personalized notifications
                can be retrieved.
              </p>
              <button
                type="button"
                className="button button-primary"
                onClick={createDemoStudent}
              >
                Load Demo Profile
              </button>
            </div>
          ) : notifications.length === 0 ? (
            <div className="empty-state notification-empty-state">
              <div className="empty-state-icon">✓</div>
              <h3>You are all caught up</h3>
              <p>
                New notifications will appear after a subscribed resource
                changes.
              </p>
            </div>
          ) : (
            <div className="notification-list">
              {notifications.map((notification) => (
                <article
                  className={`notification-card ${
                    notification.is_read ? "notification-read" : ""
                  }`}
                  key={notification.notification_id}
                >
                  <div className="notification-icon">◌</div>

                  <div className="notification-content">
                    <div className="notification-heading">
                      <div>
                        {!notification.is_read && (
                          <span className="unread-badge">New</span>
                        )}
                        <h3>{notification.title}</h3>
                      </div>

                      <time>{formatDate(notification.created_at)}</time>
                    </div>

                    <p>{notification.message}</p>

                    <span className="notification-category">
                      Personalized student alert
                    </span>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        <section id="evaluation" className="evaluation-section">
          <div className="evaluation-content">
            <div>
              <div className="eyebrow eyebrow-light">Research Evaluation</div>
              <h2>Help evaluate the EntryPoint experience.</h2>
              <p>
                Participants compare the existing Texas State information
                experience with EntryPoint and provide feedback on clarity,
                confidence, ease of use, and overall preference.
              </p>

              <a
                className="button button-light"
                href="#"
                target="_blank"
                rel="noreferrer"
              >
                Complete Feedback Survey
                <span aria-hidden="true">↗</span>
              </a>
            </div>

            <div className="evaluation-metrics">
              <div>
                <strong>4</strong>
                <span>Evaluation dimensions</span>
              </div>

              <div>
                <strong>2</strong>
                <span>Experiences compared</span>
              </div>

              <div>
                <strong>1</strong>
                <span>Student-centered goal</span>
              </div>
            </div>
          </div>
        </section>

        <footer className="app-footer">
          <div>
            <strong>EntryPoint</strong>
            <span>Independent Study Research Prototype</span>
          </div>

          <p>
            FastAPI · PostgreSQL · React · Ollama · Texas State University
          </p>
        </footer>
      </main>

      {status && (
        <div
          className={`toast toast-${statusType}`}
          role="status"
          aria-live="polite"
        >
          <span className="toast-icon">
            {statusType === "error" ? "!" : statusType === "info" ? "i" : "✓"}
          </span>
          <span>{status}</span>

          <button
            type="button"
            aria-label="Dismiss message"
            onClick={() => setStatus("")}
          >
            ×
          </button>
        </div>
      )}
    </div>
  );
}

export default App;