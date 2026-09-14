/**
 * Placeholder pageview tracker for the /blog/rendered pages.
 *
 * This intentionally does NOT send data anywhere. It was a broken external
 * reference (404) with no real analytics backend wired up. Replace the body
 * of track() with a real call (e.g. to GA4 or a self-hosted endpoint) when
 * one is ready — see assets/dashboard.css / config.py for the analytics
 * config already used elsewhere on the site.
 */
(function () {
  function track() {
    // No-op by design. Intentionally does not collect or transmit any data.
    // console.debug('[tracker] pageview:', window.location.pathname);
  }

  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    track();
  } else {
    document.addEventListener('DOMContentLoaded', track);
  }
})();
