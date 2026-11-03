// Mobile menu ------------------------------------------------------------
const toggle = document.querySelector('.menu-toggle');
const nav = document.getElementById('site-nav');

function setMenu(open) {
  toggle.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('is-open', open);
}

toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
nav.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
    setMenu(false);
    toggle.focus();
  }
});

// Mark the nav link for the section in view ---------------------------------
const links = [...nav.querySelectorAll('a[href^="#"]')];
const sections = links.map((a) => document.querySelector(a.getAttribute('href')));

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    links.forEach((a) => {
      if (a.getAttribute('href') === `#${entry.target.id}`) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
  });
}, { rootMargin: '-40% 0px -55% 0px' });

sections.forEach((s) => s && observer.observe(s));
observer.observe(document.getElementById('top')); // clears the highlight back at the hero

// Phone preview tabs (arrow keys, Home and End move between tabs) -------------
const tabs = [...document.querySelectorAll('.bottom-nav [role="tab"]')];

function selectTab(tab, focus = false) {
  tabs.forEach((t) => {
    const selected = t === tab;
    t.setAttribute('aria-selected', String(selected));
    t.tabIndex = selected ? 0 : -1;
    document.getElementById(t.getAttribute('aria-controls')).hidden = !selected;
  });
  if (focus) tab.focus();
}

tabs.forEach((tab, i) => {
  tab.addEventListener('click', () => selectTab(tab));
  tab.addEventListener('keydown', (e) => {
    const keys = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 };
    if (!(e.key in keys)) return;
    e.preventDefault();
    selectTab(tabs[(keys[e.key] + tabs.length) % tabs.length], true);
  });
});

// Case-study dialogs -----------------------------------------------------------
// Fallback for browsers without invoker commands (command / commandfor)
if (!('commandForElement' in HTMLButtonElement.prototype)) {
  document.querySelectorAll('button[command="show-modal"]').forEach((btn) => {
    btn.addEventListener('click', () => document.getElementById(btn.getAttribute('commandfor'))?.showModal());
  });
}

// Fallback for browsers without closedby (click outside to close)
if (!('closedBy' in HTMLDialogElement.prototype)) {
  document.querySelectorAll('dialog.case').forEach((dialog) => {
    dialog.addEventListener('click', (event) => {
      if (event.target !== dialog) return;
      const r = dialog.getBoundingClientRect();
      const inside = r.top <= event.clientY && event.clientY <= r.top + r.height
        && r.left <= event.clientX && event.clientX <= r.left + r.width;
      if (!inside) dialog.close();
    });
  });
}

// Copy email ---------------------------------------------------------------------
const copyBtn = document.getElementById('copy-email');
const status = document.getElementById('copy-status');
let statusTimer;

copyBtn.addEventListener('click', async () => {
  const email = document.getElementById('email-link').textContent.trim();
  try {
    await navigator.clipboard.writeText(email);
    status.textContent = 'Email copied.';
  } catch {
    status.textContent = 'Could not copy automatically. Select the address above instead.';
  }
  clearTimeout(statusTimer);
  statusTimer = setTimeout(() => { status.textContent = ''; }, 4000);
});
