// dashboard.js — loads stats + tickets, wires filters and status changes
const state = { status: 'all', priority: 'all', queue: 'all', q: '' };

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str ?? '';
  return div.innerHTML;
}

function badgeClass(prefix, value) {
  return `badge badge-${(value || '').toLowerCase().replace(/\s+/g, '_')}`;
}

function timeAgo(iso) {
  const diffMs = Date.now() - new Date(iso + 'Z').getTime();
  const mins = Math.floor(diffMs / 60000);
  if (mins < 1) return 'just now';
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

async function loadStats() {
  const res = await fetch('/api/stats');
  const s = await res.json();

  document.getElementById('statTotal').textContent = s.total;
  document.getElementById('statOpen').textContent = s.open;
  document.getElementById('statResolved').textContent = s.resolved;
  document.getElementById('statHigh').textContent = (s.by_priority && s.by_priority.high) || 0;

  const bars = document.querySelectorAll('.dstat .bar i');
  const total = s.total || 1;
  bars[1].style.width = `${(s.open / total) * 100}%`;
  bars[2].style.width = `${(((s.by_priority && s.by_priority.high) || 0) / total) * 100}%`;
  bars[3].style.width = `${(s.resolved / total) * 100}%`;

  const queueFilter = document.getElementById('queueFilter');
  const existing = new Set(Array.from(queueFilter.options).map(o => o.value));
  Object.keys(s.by_queue || {}).forEach(q => {
    if (!existing.has(q)) {
      const opt = document.createElement('option');
      opt.value = q;
      opt.textContent = q;
      queueFilter.appendChild(opt);
    }
  });
}

async function loadTickets() {
  const params = new URLSearchParams();
  if (state.status !== 'all') params.set('status', state.status);
  if (state.priority !== 'all') params.set('priority', state.priority);
  if (state.queue !== 'all') params.set('queue', state.queue);
  if (state.q) params.set('q', state.q);

  const res = await fetch(`/api/tickets?${params.toString()}`);
  const tickets = await res.json();

  const body = document.getElementById('ticketsBody');
  const empty = document.getElementById('emptyState');

  if (!tickets.length) {
    body.innerHTML = '';
    empty.style.display = 'block';
    return;
  }
  empty.style.display = 'none';

  body.innerHTML = tickets.map(t => `
    <tr data-ref="${escapeHtml(t.ticket_ref)}">
      <td class="td-ref">${escapeHtml(t.ticket_ref)}</td>
      <td class="td-subject">
        <span class="s">${escapeHtml(t.subject)}</span>
        <span class="b">${escapeHtml(t.body)}</span>
      </td>
      <td>${escapeHtml(t.predicted_queue)}</td>
      <td><span class="${badgeClass('priority', t.predicted_priority)}">${escapeHtml(t.predicted_priority)}</span></td>
      <td>${escapeHtml(t.predicted_type)}</td>
      <td>${escapeHtml((t.language || '').toUpperCase())}</td>
      <td>
        <select class="status-select" data-ref="${escapeHtml(t.ticket_ref)}">
          <option value="open" ${t.status === 'open' ? 'selected' : ''}>Open</option>
          <option value="in_progress" ${t.status === 'in_progress' ? 'selected' : ''}>In progress</option>
          <option value="resolved" ${t.status === 'resolved' ? 'selected' : ''}>Resolved</option>
        </select>
      </td>
      <td>${timeAgo(t.created_at)}</td>
    </tr>
  `).join('');

  body.querySelectorAll('.status-select').forEach(sel => {
    sel.addEventListener('change', async (e) => {
      const ref = e.target.dataset.ref;
      await fetch(`/api/tickets/${ref}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: e.target.value }),
      });
      loadStats();
    });
  });
}

function refreshAll() {
  loadStats();
  loadTickets();
}

document.addEventListener('DOMContentLoaded', () => {
  refreshAll();

  document.getElementById('statusFilter').addEventListener('change', e => { state.status = e.target.value; loadTickets(); });
  document.getElementById('priorityFilter').addEventListener('change', e => { state.priority = e.target.value; loadTickets(); });
  document.getElementById('queueFilter').addEventListener('change', e => { state.queue = e.target.value; loadTickets(); });
  document.getElementById('refreshBtn').addEventListener('click', refreshAll);

  let searchTimer;
  document.getElementById('searchInput').addEventListener('input', e => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => { state.q = e.target.value; loadTickets(); }, 300);
  });

  setInterval(refreshAll, 15000);
});
