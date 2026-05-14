/* Cryton — contact.js */
const form      = document.getElementById('contact-form');
const submitBtn = document.getElementById('submit-btn');
const spinner   = document.getElementById('btn-spinner');
const successEl = document.getElementById('form-success');
const errorEl   = document.getElementById('form-error');

if (form) {
  form.addEventListener('submit', async e => {
    e.preventDefault();

    // Clear previous messages
    successEl.classList.add('hidden');
    errorEl.classList.add('hidden');

    // Basic validation
    const name    = form.name.value.trim();
    const email   = form.email.value.trim();
    const message = form.message.value.trim();

    if (!name || !email || !message) {
      errorEl.textContent = '⚠ Please fill in all required fields.';
      errorEl.classList.remove('hidden');
      return;
    }

    // Loading state
    submitBtn.disabled = true;
    spinner.classList.remove('hidden');

    const payload = {
      name,
      email,
      company: form.company.value.trim(),
      service: form.service.value,
      message,
    };

    try {
      const res = await fetch('/api/contact', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(payload),
      });

      const data = await res.json();

      if (data.ok) {
        successEl.classList.remove('hidden');
        form.reset();
      } else {
        throw new Error(data.error || 'Unknown error');
      }
    } catch (err) {
      errorEl.classList.remove('hidden');
      console.error('Contact form error:', err);
    } finally {
      submitBtn.disabled = false;
      spinner.classList.add('hidden');
    }
  });
}
