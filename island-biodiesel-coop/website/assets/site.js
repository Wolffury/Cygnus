// Mobile nav toggle + current-year footer. No dependencies.
document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  // Forms post to the endpoint in data-endpoint (e.g. Formspree, Netlify Forms).
  // Until one is configured, show a friendly message instead of failing silently.
  document.querySelectorAll("form[data-endpoint]").forEach(function (form) {
    var endpoint = form.getAttribute("data-endpoint");
    if (endpoint && endpoint.indexOf("[") === -1) {
      form.setAttribute("action", endpoint);
      form.setAttribute("method", "POST");
      return;
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = form.querySelector(".form-status");
      if (msg) msg.textContent = "Thanks! The online form isn't connected yet — please email us at the address below.";
    });
  });
});
