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

function collectDraft() {
  const items = [];
  document.querySelectorAll('[data-item-row]').forEach(row => {
    const key = row.getAttribute('data-key');
    const label = row.querySelector('[data-label]')?.textContent || '';
    const done = row.querySelector('input[type=checkbox]')?.checked || false;
    const minutes = parseInt(row.querySelector('input[data-minutes]')?.value || '0', 10) || 0;
    const comment = row.querySelector('input[data-comment]')?.value || '';
    items.push({ key, label, done, minutes, comment });
  });
  const reflection = document.querySelector('#reflection')?.value || '';
  return { items, reflection };
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
  document.querySelectorAll('input, textarea').forEach(el => {
    if (el.closest('[data-checkin]')) {
      el.addEventListener('input', saveDraft);
      el.addEventListener('change', saveDraft);
    }
  });

  const manual = document.querySelector('#manualSave');
  if (manual) manual.addEventListener('click', (e) => { e.preventDefault(); saveDraftNow(); });
});
