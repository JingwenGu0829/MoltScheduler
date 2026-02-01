async function postJSON(url, data) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const txt = await res.text().catch(() => '');
    throw new Error(`HTTP ${res.status} ${txt}`);
  }
  return res.json();
}

function debounce(fn, ms) {
  let t = null;
  return (...args) => {
    if (t) clearTimeout(t);
    t = setTimeout(() => fn(...args), ms);
  };
}

function currentMode() {
  const el = document.querySelector('input[name="mode"]:checked');
  return el ? el.value : 'commit';
}

function collectDraft() {
  const items = [];
  document.querySelectorAll('[data-item-row]').forEach(row => {
    const key = row.getAttribute('data-key');
    const label = row.querySelector('[data-label]')?.textContent || '';
    const done = row.querySelector('input[type=checkbox]')?.checked || false;
    const comment = row.querySelector('input[data-comment]')?.value || '';
    items.push({ key, label, done, comment });
  });
  const reflection = document.querySelector('#reflection')?.value || '';
  const mode = currentMode();
  return { mode, items, reflection };
}

async function saveDraftNow() {
  const status = document.querySelector('#saveStatus');
  try {
    if (status) status.textContent = 'Saving…';
    const payload = collectDraft();
    await postJSON('/api/checkin_draft', payload);
    if (status) status.textContent = 'Saved';
  } catch (e) {
    if (status) status.textContent = 'Save failed';
    console.error(e);
  }
}

const saveDraft = debounce(saveDraftNow, 500);

window.addEventListener('DOMContentLoaded', () => {
  // Plan: preview by default
  if (document.querySelector('#planPreview')) {
    showPlanPreview();
  }
  const planTA = document.querySelector('#plan');
  if (planTA) planTA.addEventListener('input', debounce(renderPlanPreview, 200));

  document.querySelectorAll('input, textarea, select').forEach(el => {
    if (el.closest('[data-checkin]')) {
      el.addEventListener('input', saveDraft);
      el.addEventListener('change', saveDraft);
    }
  });

  const manual = document.querySelector('#manualSave');
  if (manual) manual.addEventListener('click', (e) => { e.preventDefault(); saveDraftNow(); });
});


function renderPlanPreview() {
  const ta = document.querySelector('#plan');
  const pv = document.querySelector('#planPreview');
  if (!ta || !pv) return;
  const src = ta.value || '';
  if (window.marked) {
    pv.innerHTML = window.marked.parse(src);
  } else {
    pv.textContent = src;
  }
}

function showPlanPreview() {
  const ta = document.querySelector('#plan');
  const pv = document.querySelector('#planPreview');
  if (!ta || !pv) return;
  renderPlanPreview();
  ta.style.display = 'none';
  pv.style.display = 'block';
}
