// auth.js — login & signup form handling
document.addEventListener('DOMContentLoaded', () => {
  const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

  function clearErrors(form) {
    form.querySelectorAll('.field-error').forEach(el => { el.textContent = ''; });
    form.querySelectorAll('.field input').forEach(el => el.classList.remove('invalid'));
  }

  function showFieldError(form, field, message) {
    const el = document.getElementById(`err-${field}`);
    const input = document.getElementById(field);
    if (el) el.textContent = message;
    if (input) input.classList.add('invalid');
  }

  function showStatus(form, message, ok) {
    const status = form.querySelector('#formStatus');
    if (!status) return;
    status.textContent = message;
    status.style.color = ok ? 'var(--green)' : '#C81E33';
  }

  async function submitForm(form, url, buildPayload, validate) {
    const btn = form.querySelector('button[type="submit"]');
    const originalText = btn.textContent;

    return async (e) => {
      e.preventDefault();
      clearErrors(form);
      showStatus(form, '', true);

      const payload = buildPayload();
      const clientErrors = validate(payload);
      if (Object.keys(clientErrors).length) {
        Object.entries(clientErrors).forEach(([field, msg]) => showFieldError(form, field, msg));
        return;
      }

      btn.disabled = true;
      btn.textContent = 'Please wait…';

      try {
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
          if (data.fields) {
            Object.entries(data.fields).forEach(([field, msg]) => showFieldError(form, field, msg));
          }
          showStatus(form, data.error || 'Something went wrong. Please try again.', false);
          return;
        }

        showStatus(form, 'Success — redirecting…', true);
        window.location.href = data.redirect || '/';
      } catch (err) {
        showStatus(form, 'Could not reach the server. Is the app running?', false);
      } finally {
        btn.disabled = false;
        btn.textContent = originalText;
      }
    };
  }

  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    submitForm(
      loginForm,
      '/login',
      () => ({
        email: document.getElementById('email').value.trim(),
        password: document.getElementById('password').value,
      }),
      (payload) => {
        const errors = {};
        if (!EMAIL_RE.test(payload.email)) errors.email = 'Enter a valid email address.';
        if (!payload.password) errors.password = 'Password is required.';
        return errors;
      }
    ).then(handler => loginForm.addEventListener('submit', handler));
  }

  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
    submitForm(
      signupForm,
      '/signup',
      () => ({
        name: document.getElementById('name').value.trim(),
        email: document.getElementById('email').value.trim(),
        password: document.getElementById('password').value,
        confirm_password: document.getElementById('confirm_password').value,
      }),
      (payload) => {
        const errors = {};
        if (!payload.name || payload.name.length < 2) errors.name = 'Please enter your full name.';
        if (!EMAIL_RE.test(payload.email)) errors.email = 'Enter a valid email address.';
        if (!payload.password || payload.password.length < 8) errors.password = 'Password must be at least 8 characters.';
        if (payload.password !== payload.confirm_password) errors.confirm_password = 'Passwords do not match.';
        return errors;
      }
    ).then(handler => signupForm.addEventListener('submit', handler));
  }
});
