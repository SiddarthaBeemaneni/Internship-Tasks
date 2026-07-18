// home.js — live ticket-triage demo + contact form
document.addEventListener('DOMContentLoaded', () => {
  const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

  const SAMPLE_TICKETS = [
    {
      name: 'Jordan Lee',
      email: 'jordan@company.com',
      subject: 'Invoice export keeps failing at 90%',
      body: "Since the last release our billing export keeps failing at 90% with a timeout error. This is blocking our month-end close and we need it fixed urgently.",
    },
    {
      name: 'Mira Tan',
      email: 'mira@example.com',
      subject: 'Frage zur Rechnungsstellung',
      body: 'Ich habe eine Frage zu meiner letzten Rechnung. Der Betrag scheint nicht mit meinem Abonnement übereinzustimmen. Können Sie das bitte prüfen?',
    },
    {
      name: 'Alex Rivera',
      email: 'alex@example.com',
      subject: 'Feature request: dark mode',
      body: "It would be great to have a dark mode option in the dashboard settings. Not urgent, just a nice-to-have for the team.",
    },
  ];

  const form = document.getElementById('ticketForm');
  const submitBtn = document.getElementById('submitBtn');
  const sampleBtn = document.getElementById('sampleBtn');
  const errorEl = document.getElementById('formError');
  const resultBox = document.getElementById('resultBox');

  function clearFieldErrors() {
    form.querySelectorAll('.field-error').forEach(el => { el.textContent = ''; });
    form.querySelectorAll('.field input, .field textarea').forEach(el => el.classList.remove('invalid'));
  }

  function showFieldError(field, message) {
    const el = document.getElementById(`err-${field}`);
    const input = document.getElementById(field);
    if (el) el.textContent = message;
    if (input) input.classList.add('invalid');
  }

  function validateClientSide(payload) {
    const errors = {};
    if (!payload.name || payload.name.length < 2) {
      errors.name = 'Please enter your name.';
    }
    if (!payload.email) {
      errors.email = 'Email is required.';
    } else if (!EMAIL_RE.test(payload.email)) {
      errors.email = "That email address doesn't look right.";
    }
    if (!payload.subject) errors.subject = 'Subject is required.';
    if (!payload.body) {
      errors.body = 'Please describe the issue.';
    } else if (payload.body.length < 10) {
      errors.body = 'Please add a bit more detail (at least 10 characters).';
    }
    return errors;
  }

  if (sampleBtn) {
    sampleBtn.addEventListener('click', () => {
      const sample = SAMPLE_TICKETS[Math.floor(Math.random() * SAMPLE_TICKETS.length)];
      document.getElementById('name').value = sample.name;
      document.getElementById('email').value = sample.email;
      document.getElementById('subject').value = sample.subject;
      document.getElementById('body').value = sample.body;
      clearFieldErrors();
      errorEl.style.display = 'none';
      resultBox.classList.remove('show');
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearFieldErrors();
    errorEl.style.display = 'none';
    resultBox.classList.remove('show');

    const payload = {
      name: document.getElementById('name').value.trim(),
      email: document.getElementById('email').value.trim(),
      subject: document.getElementById('subject').value.trim(),
      body: document.getElementById('body').value.trim(),
    };

    const clientErrors = validateClientSide(payload);
    if (Object.keys(clientErrors).length) {
      Object.entries(clientErrors).forEach(([field, msg]) => showFieldError(field, msg));
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Analyzing…';

    try {
      const res = await fetch('/api/tickets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        errorEl.textContent = data.error || 'Something went wrong. Please try again.';
        errorEl.style.display = 'block';
        return;
      }

      const prediction = data.prediction || {};
      const priority = (prediction.priority || '').toLowerCase();
      const isUrgent = priority === 'high' || priority === 'urgent' || priority === 'critical';

      const badge = document.getElementById('resultBadge');
      badge.textContent = isUrgent ? 'Needs attention' : 'Looks routine';
      resultBox.classList.remove('result-positive', 'result-negative');
      resultBox.classList.add(isUrgent ? 'result-negative' : 'result-positive');

      // Confidence = average of the per-field confidences the model returned.
      const confidences = ['queue', 'priority', 'type']
        .map(f => prediction[`${f}_confidence`])
        .filter(v => typeof v === 'number');
      const avgConfidence = confidences.length
        ? Math.round(confidences.reduce((a, b) => a + b, 0) / confidences.length)
        : null;

      const fill = document.getElementById('resConfidenceFill');
      const text = document.getElementById('resConfidenceText');
      if (avgConfidence !== null) {
        fill.style.width = `${avgConfidence}%`;
        fill.classList.toggle('low', avgConfidence < 60);
        text.textContent = `${avgConfidence}%`;
      } else {
        fill.style.width = '0%';
        text.textContent = 'n/a';
      }

      document.getElementById('resultRef').textContent = `Ticket ${data.ticket_ref} created`;
      document.getElementById('resQueue').textContent = prediction.queue || '—';
      document.getElementById('resPriority').textContent = prediction.priority || '—';
      document.getElementById('resType').textContent = prediction.type || '—';
      resultBox.classList.add('show');
      form.reset();
    } catch (err) {
      errorEl.textContent = 'Could not reach the server. Is the Flask app running?';
      errorEl.style.display = 'block';
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Analyze & submit ticket';
    }
  });

  const contactForm = document.getElementById('contactForm');
  const contactBtn = document.getElementById('contactBtn');
  const contactStatus = document.getElementById('contactStatus');

  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      contactBtn.disabled = true;
      contactBtn.textContent = 'Sending…';
      contactStatus.style.color = 'var(--ink-soft)';

      const payload = {
        name: document.getElementById('cname').value.trim(),
        email: document.getElementById('cemail').value.trim(),
        message: document.getElementById('cmessage').value.trim(),
      };

      if (!payload.name || !payload.email || !payload.message) {
        contactStatus.style.color = '#C81E33';
        contactStatus.textContent = 'Please fill in every field.';
        contactBtn.disabled = false;
        contactBtn.textContent = 'Send message';
        return;
      }
      if (!EMAIL_RE.test(payload.email)) {
        contactStatus.style.color = '#C81E33';
        contactStatus.textContent = "That email address doesn't look right.";
        contactBtn.disabled = false;
        contactBtn.textContent = 'Send message';
        return;
      }

      try {
        const res = await fetch('/api/contact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
          contactStatus.style.color = '#C81E33';
          contactStatus.textContent = data.error || 'Something went wrong.';
        } else {
          contactStatus.style.color = '#0E7E56';
          contactStatus.textContent = 'Message sent — thank you.';
          contactForm.reset();
        }
      } catch {
        contactStatus.style.color = '#C81E33';
        contactStatus.textContent = 'Could not reach the server.';
      } finally {
        contactBtn.disabled = false;
        contactBtn.textContent = 'Send message';
      }
    });
  }
});
