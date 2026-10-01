// 🔥 Fire Apps — site behavior
(function () {
  "use strict";

  // Footer year
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Download buttons: real URLs get wired in later via data-apk.
  // For now, placeholder hrefs ("#") are intercepted so nothing jumps.
  var APK_URLS = {
    // infinity: "https://example.com/infinity.apk",
    // "codex-press": "https://example.com/codex-press.apk",
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
        key === "night-owl" ? "Night Owl is coming soon." :
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

  // Gentle starfield on the hero canvas
  var canvas = document.getElementById("stars");
  if (canvas && canvas.getContext) {
    var ctx = canvas.getContext("2d");
    var stars = [];
    var W = 0, H = 0;

    function resize() {
      W = canvas.width = window.innerWidth;
      H = canvas.height = window.innerHeight;
      stars = [];
      var n = Math.min(220, Math.floor((W * H) / 9000));
      for (var i = 0; i < n; i++) {
        stars.push({
          x: Math.random() * W,
          y: Math.random() * H,
          r: Math.random() * 1.4 + 0.3,
          s: Math.random() * 0.25 + 0.05,
          tw: Math.random() * Math.PI * 2,
        });
      }
    }

    function tick() {
      ctx.clearRect(0, 0, W, H);
      for (var i = 0; i < stars.length; i++) {
        var st = stars[i];
        st.y += st.s;
        st.tw += 0.02;
        if (st.y > H) { st.y = 0; st.x = Math.random() * W; }
        var a = 0.35 + 0.35 * Math.sin(st.tw);
        ctx.beginPath();
        ctx.arc(st.x, st.y, st.r, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(200, 170, 255," + a.toFixed(2) + ")";
        ctx.fill();
      }
      requestAnimationFrame(tick);
    }

    window.addEventListener("resize", resize);
    resize();
    tick();
  }
})();
