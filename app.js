// Premium Marketing Apps — site behavior
(function () {
  "use strict";

  // Footer year
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Download buttons: real URLs get wired in later via data-apk.
  // For now, placeholder hrefs ("#") are intercepted so nothing jumps.
  var APK_URLS = {
    "codex-press": "downloads/codex-press.apk",
    // forge-studio: "downloads/forge-studio.apk",
  };

  document.querySelectorAll("a[data-apk]").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      var key = btn.getAttribute("data-apk");
      if (APK_URLS[key]) {
        btn.setAttribute("href", APK_URLS[key]);
        return; // let the browser follow the real URL
      }
      e.preventDefault();
      toast(
        key === "codex-press" ? "Codex Press is coming soon." :
        key === "forge-studio" ? "Forge Studio is coming soon." :
        "Download link coming soon."
      );
    });
  });

  var toastTimer = null;
  function toast(msg) {
    var el = document.getElementById("toast");
    if (!el) {
      el = document.createElement("div");
      el.id = "toast";
      el.setAttribute("role", "status");
      document.body.appendChild(el);
    }
    el.textContent = msg;
    el.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.classList.remove("show"); }, 2600);
  }

})();
