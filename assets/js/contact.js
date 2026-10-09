'use strict';

(function () {
  const page = document.querySelector('article.contact');
  if (!page) return;

  const copy = page.querySelector('[data-copy-email]');
  if (!navigator.clipboard) copy.hidden = true;
  copy.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText('fujiang@arizona.edu');
      copy.querySelector('span').textContent = 'Copied';
      copy.setAttribute('aria-label', 'Email address copied');
    } catch {
      copy.querySelector('span').textContent = 'Use email link';
    }
  });

  const form = page.querySelector('[data-form]');
  const button = form.querySelector('[data-form-btn]');
  const notification = page.querySelector('#formNotification');
  let sending = false;
  form.addEventListener('input', () => {
    if (!sending) button.disabled = !form.checkValidity();
  });
  function showNotification(message, error) {
    notification.hidden = false;
    notification.classList.toggle('error', error);
    notification.textContent = message;
  }
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (sending || !form.reportValidity()) return;
    sending = true;
    button.disabled = true;
    button.querySelector('span').textContent = 'Sending…';
    notification.hidden = true;
    try {
      const response = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      });
      if (response.ok) {
        showNotification('Message sent. Thank you for getting in touch!', false);
        form.reset();
      } else {
        showNotification('Your message could not be sent. Please try again or email me directly.', true);
      }
    } catch {
      showNotification('Your message could not be sent. Please try again or email me directly.', true);
    } finally {
      sending = false;
      button.disabled = !form.checkValidity();
      button.querySelector('span').textContent = 'Send message';
    }
  });
})();
