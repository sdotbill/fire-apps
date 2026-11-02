/* Dave corner talk bar — daveexolex.com content pages.
   One small bar, bottom-right, on every page except the homepage.
   Same visitor lane, same session, same thread as the homepage talk
   bar: it reads and writes the homepage client's own localStorage
   keys (dave_chat_session / dave_chat_identity / dave_chat_history)
   and posts to the same /chat route with the same payload shape, so
   a conversation started anywhere on the site is one conversation.
   Lane separation stays server-side, exactly as on the homepage:
   no identity token, no owner thread — a visitor is a visitor.
   Featherweight by design: this one file, no libraries, no fonts,
   CSS rides inside it, the only image is the site's own cached
   64px baby Dave.
   v2 (Nov 2, 2026 — the Every-Dave update, Bill's order): compact
   phone-thread bubbles, and conversational vision. There is NO
   camera button, line, or toggle anywhere in this widget. When
   Dave himself offers to see (his reply ends with the marker
   [OFFER_VISION], which is stripped before display), ONE small
   chip renders inside his bubble — "Show Dave" — and tapping it
   is the visitor's own gesture that asks the browser for the
   camera. The feed stays on the visitor's device: it is never
   sent, recorded, or saved; it only proves the permission and
   the look, and the panel says so, plainly. */
(function(){
  "use strict";
  /* Dave's pages only. Shared files also serve the PMS domain —
     there the widget stays inert. localhost is allowed so the
     practice copy can be proven before anything ships. */
  var host = location.hostname;
  if(host !== "daveexolex.com" && host !== "www.daveexolex.com" &&
     host !== "localhost" && host !== "127.0.0.1") return;
  if(document.getElementById("chat-input")) return;   /* homepage has its own bar */
  if(document.getElementById("dave-corner")) return;  /* never twice */

  var CHAT = "https://dave-chat.william-ced.workers.dev/chat";
  var SESSION_KEY = "dave_chat_session";
  var IDENTITY_KEY = "dave_chat_identity";
  var HISTORY_KEY = "dave_chat_history";

  function uuid(){
    if(window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return "s-" + Date.now() + "-" + Math.random().toString(36).slice(2, 12);
  }
  var sessionId = null, identity = null, history = [];
  try{ sessionId = localStorage.getItem(SESSION_KEY); }catch(e){}
  if(!sessionId){ sessionId = uuid(); try{ localStorage.setItem(SESSION_KEY, sessionId); }catch(e){} }
  try{ identity = localStorage.getItem(IDENTITY_KEY); }catch(e){}
  try{ history = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]"); }catch(e){ history = []; }
  if(!Array.isArray(history)) history = [];
  function save(){ try{ localStorage.setItem(HISTORY_KEY, JSON.stringify(history)); }catch(e){} }
  function storeIdentity(v){
    if(typeof v !== "string" || !/^[a-f0-9]{32,64}$/.test(v)) return;
    identity = v;
    try{ localStorage.setItem(IDENTITY_KEY, v); }catch(e){}
  }
  /* The homepage client's own tiny renderer: escape first, then
     **bold**, *italic*, `code`. Nothing unescaped reaches the DOM. */
  function mdRender(text){
    var t = String(text == null ? "" : text);
    t = t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    t = t.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    t = t.replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<em>$2</em>");
    t = t.replace(/`([^`]+)`/g, "<code>$1</code>");
    return t;
  }

  var css = [
    "#dave-corner{position:fixed;right:16px;bottom:16px;z-index:2147482000;",
    "font-family:Inter,system-ui,-apple-system,'Segoe UI',sans-serif;color:#3a2e1e;",
    "display:flex;flex-direction:column;align-items:flex-end;gap:8px;}",
    "#dave-corner *{box-sizing:border-box;margin:0;padding:0;}",
    ".dc-panel{width:min(348px,calc(100vw - 24px));max-height:40vh;display:none;",
    "flex-direction:column;background:#fffdf6;border:1px solid #e7dcc3;border-radius:16px;",
    "box-shadow:0 14px 38px rgba(90,64,14,.22);overflow:hidden;}",
    ".dc-panel.open{display:flex;}",
    ".dc-head{display:flex;align-items:center;gap:8px;padding:8px 10px;",
    "background:#faf3df;border-bottom:1px solid #e7dcc3;font-size:.83rem;font-weight:600;}",
    ".dc-head img{width:22px;height:22px;border-radius:50%;background:#c9a227;}",
    ".dc-head .dc-x{margin-left:auto;border:0;background:none;font-size:1.05rem;line-height:1;",
    "color:#8a6d2f;cursor:pointer;padding:2px 6px;}",
    /* Compact phone-thread bubbles (v2): #dave-corner-prefixed so
       they outrank the * reset above on margin/padding. */
    "#dave-corner .dc-msgs{overflow-y:auto;padding:8px;display:flex;flex-direction:column;gap:5px;}",
    "#dave-corner .dc-msg{max-width:78%;padding:5px 9px;border-radius:13px;font-size:.83rem;line-height:1.38;",
    "white-space:pre-wrap;word-wrap:break-word;}",
    "#dave-corner .dc-msg.user{align-self:flex-end;background:#f3e3b3;color:#3a2e1e;border-bottom-right-radius:3px;}",
    "#dave-corner .dc-msg.dave{align-self:flex-start;background:#faf7ef;border:1px solid #e7dcc3;border-bottom-left-radius:3px;}",
    "#dave-corner .dc-msg.err{align-self:flex-start;background:#fdf0ec;border:1px solid #ecc9bc;}",
    /* Vision chip + in-panel preview (v2). The chip exists only
       inside a Dave bubble whose reply carried the offer marker;
       there is no standing camera control anywhere else. */
    "#dave-corner .dc-chip{display:inline-flex;align-items:center;gap:5px;margin-top:7px;",
    "padding:4px 10px;border-radius:999px;border:1px solid #c9a227;background:#fffdf6;",
    "color:#8a6d2f;font:inherit;font-size:.76rem;font-weight:600;cursor:pointer;}",
    "#dave-corner .dc-chip:hover{background:#faf3df;}",
    "#dave-corner .dc-chip:focus-visible{outline:2px solid #8a6d2f;outline-offset:2px;}",
    "#dave-corner .dc-camview{display:none;margin-top:8px;}",
    "#dave-corner .dc-camview.on{display:block;}",
    "#dave-corner .dc-camview video{width:132px;height:99px;object-fit:cover;display:block;",
    "border-radius:12px;transform:scaleX(-1);background:#241c0d;border:1px solid #e7dcc3;}",
    "#dave-corner .dc-camstate{display:block;margin-top:5px;padding:0;border:0;background:none;",
    "font:inherit;font-size:.74rem;font-weight:600;color:#a33327;cursor:pointer;text-align:left;}",
    "#dave-corner .dc-camstate i{display:inline-block;width:7px;height:7px;border-radius:50%;",
    "background:#c0392b;margin-right:5px;vertical-align:1px;animation:dcpulse 1.4s infinite;}",
    "@keyframes dcpulse{0%,100%{opacity:1;}50%{opacity:.3;}}",
    "#dave-corner .dc-camscope{font-size:.7rem;line-height:1.35;color:#8a6d2f;margin-top:3px;}",
    ".dc-dots i{display:inline-block;width:7px;height:7px;margin-right:4px;border-radius:50%;",
    "background:#a08b57;animation:dcblink 1.1s infinite;}",
    ".dc-dots i:nth-child(2){animation-delay:.18s;}",
    ".dc-dots i:nth-child(3){animation-delay:.36s;margin-right:0;}",
    "@keyframes dcblink{0%,60%,100%{opacity:.25;}30%{opacity:1;}}",
    ".dc-opener{display:none;max-width:min(300px,calc(100vw - 24px));background:#fffdf6;",
    "border:1px solid #e7dcc3;border-radius:14px;border-bottom-right-radius:4px;",
    "box-shadow:0 10px 26px rgba(90,64,14,.18);padding:9px 30px 9px 12px;",
    "font-size:.88rem;line-height:1.4;cursor:pointer;position:relative;}",
    ".dc-opener.show{display:block;}",
    ".dc-opener .dc-ox{position:absolute;top:4px;right:7px;border:0;background:none;",
    "font-size:.95rem;color:#8a6d2f;cursor:pointer;line-height:1;padding:2px;}",
    ".dc-bar{display:flex;align-items:center;gap:7px;background:#fffdf6;",
    "border:1px solid #e7dcc3;border-radius:999px;padding:5px 5px 5px 7px;",
    "box-shadow:0 10px 26px rgba(90,64,14,.20);width:min(320px,calc(100vw - 24px));}",
    ".dc-bar img{width:26px;height:26px;border-radius:50%;background:#c9a227;cursor:pointer;flex:none;}",
    ".dc-bar input{flex:1;min-width:0;border:0;outline:none;background:none;",
    "font-size:.92rem;color:#3a2e1e;padding:6px 2px;}",
    ".dc-bar input::placeholder{color:#a08b57;}",
    ".dc-send{flex:none;width:32px;height:32px;border-radius:50%;border:0;cursor:pointer;",
    "background:#c9a227;color:#fffdf6;display:flex;align-items:center;justify-content:center;}",
    ".dc-send:disabled{opacity:.55;cursor:default;}",
    ".dc-send svg{width:15px;height:15px;fill:currentColor;}"
  ].join("");
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  var root = document.createElement("div");
  root.id = "dave-corner";
  root.innerHTML =
    '<div class="dc-opener" id="dc-opener"><span id="dc-opener-text"></span>' +
    '<button class="dc-ox" id="dc-opener-x" aria-label="Dismiss">×</button></div>' +
    '<div class="dc-panel" id="dc-panel"><div class="dc-head">' +
    '<img src="/assets/baby-dave-64.png" alt="Dave"><span>Dave</span>' +
    '<button class="dc-x" id="dc-close" aria-label="Close conversation">×</button></div>' +
    '<div class="dc-msgs" id="dc-msgs"></div></div>' +
    '<form class="dc-bar" id="dc-form"><img src="/assets/baby-dave-64.png" alt="Dave" id="dc-face">' +
    '<input id="dc-input" type="text" placeholder="Ask Dave anything…" autocomplete="off" aria-label="Ask Dave anything">' +
    '<button class="dc-send" id="dc-send" type="submit" aria-label="Send">' +
    '<svg viewBox="0 0 24 24"><path d="M12 3l7 9h-4v9h-6v-9H5z"/></svg></button></form>';
  document.body.appendChild(root);

  var panel = document.getElementById("dc-panel");
  var msgs = document.getElementById("dc-msgs");
  var form = document.getElementById("dc-form");
  var input = document.getElementById("dc-input");
  var sendBtn = document.getElementById("dc-send");
  var opener = document.getElementById("dc-opener");
  var sending = false;
  var rendered = false;

  /* Conversational vision (v2): Dave ends a reply with the marker
     [OFFER_VISION] when — and only when — he offers to see. The
     marker is stripped before display and swapped for one small
     chip inside his bubble. The stored history keeps the clean
     text plus a v flag so the chip survives a re-render; the
     payload still sends only role + content. */
  var VISION_MARKER = "[OFFER_VISION]";
  function splitVision(text){
    var t = String(text == null ? "" : text);
    if(t.indexOf(VISION_MARKER) === -1) return { text: t, offer: false };
    return { text: t.split(VISION_MARKER).join("").replace(/\s+$/, ""), offer: true };
  }

  /* Camera: on-device preview only, started solely by the chip
     inside Dave's own bubble. The stream is never recorded,
     captured, or sent anywhere; stopping is total, and closing
     the panel stops it too. */
  var camStream = null, camWanted = false, camView = null;
  function stopCam(){
    camWanted = false;
    if(camStream){
      var tracks = camStream.getTracks();
      for(var i = 0; i < tracks.length; i++) tracks[i].stop();
      camStream = null;
    }
    if(camView){
      var v = camView.querySelector("video");
      if(v) v.srcObject = null;
      camView.classList.remove("on");
      camView = null;
    }
  }
  function startCam(hostBubble){
    if(camStream || camWanted) return;
    camWanted = true;
    if(!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia){
      camWanted = false;
      bubble("assistant", "This browser can’t share a camera from this page, so I can’t see you.", "err");
      return;
    }
    navigator.mediaDevices.getUserMedia({video: true, audio: false}).then(function(stream){
      if(!camWanted){ /* panel closed or stopped while the browser asked */
        var tr = stream.getTracks();
        for(var i = 0; i < tr.length; i++) tr[i].stop();
        return;
      }
      camStream = stream;
      var view = document.createElement("div");
      view.className = "dc-camview on";
      view.innerHTML =
        '<video autoplay playsinline muted></video>' +
        '<button type="button" class="dc-camstate"><i></i>Dave can see you · tap to stop</button>' +
        '<p class="dc-camscope">Practice build: this camera feed stays on your ' +
        'device — it isn’t sent or saved anywhere.</p>';
      view.querySelector("video").srcObject = stream;
      view.querySelector(".dc-camstate").addEventListener("click", stopCam);
      hostBubble.appendChild(view);
      camView = view;
      msgs.scrollTop = msgs.scrollHeight;
    }).catch(function(){
      camWanted = false;
      bubble("assistant", "Camera didn’t open — the browser said no, so I can’t see you.", "err");
    });
  }
  function addVisionChip(d){
    var chip = document.createElement("button");
    chip.type = "button";
    chip.className = "dc-chip";
    chip.textContent = "Show Dave 📷";
    chip.addEventListener("click", function(){ startCam(d); });
    d.appendChild(document.createElement("br"));
    d.appendChild(chip);
  }

  function bubble(role, text, cls){
    var d = document.createElement("div");
    d.className = "dc-msg " + (role === "user" ? "user" : "dave") + (cls ? " " + cls : "");
    var sv = role === "user" ? { text: String(text == null ? "" : text), offer: false } : splitVision(text);
    d.innerHTML = mdRender(sv.text);
    msgs.appendChild(d);
    if(sv.offer) addVisionChip(d);
    msgs.scrollTop = msgs.scrollHeight;
    return d;
  }
  function renderHistory(){
    msgs.innerHTML = "";
    var tail = history.slice(-30);
    for(var i = 0; i < tail.length; i++){
      if(tail[i] && (tail[i].role === "user" || tail[i].role === "assistant") && tail[i].content){
        var d = bubble(tail[i].role === "user" ? "user" : "assistant", tail[i].content);
        if(tail[i].role === "assistant" && tail[i].v) addVisionChip(d);
      }
    }
    rendered = true;
  }
  function openPanel(){
    if(!rendered) renderHistory();
    panel.classList.add("open");
    hideOpener();
  }
  function hideOpener(){ opener.classList.remove("show"); }

  /* Dave speaks first: one page-specific line in the collapsed bar,
     a few seconds after the page settles. Never auto-opens the
     panel, dismissible, once per session per page, and not at all
     when a conversation already exists. */
  function openerLine(){
    var p = location.pathname;
    if(p === "/origin/") return "Want to know what a Dave could do for you?";
    if(p.indexOf("/papers/") === 0) return "Want any of these explained in plain English?";
    if(p.indexOf("/questions/") === 0) return "Got a follow-up? Ask me — I know this ground well.";
    if(p === "/books/") return "Want a hand picking which book to start with?";
    if(p === "/dave/") return "That's me — want to talk?";
    if(p === "/who-is-dave/") return "Want to know what a Dave could do for you?";
    return "Ask me anything — I'm Dave.";
  }
  var openerKey = "dc_opener:" + location.pathname;
  var openerSeen = false;
  try{ openerSeen = !!sessionStorage.getItem(openerKey); }catch(e){}
  if(!openerSeen && history.length === 0){
    setTimeout(function(){
      if(panel.classList.contains("open")) return;
      document.getElementById("dc-opener-text").textContent = openerLine();
      opener.classList.add("show");
      try{ sessionStorage.setItem(openerKey, "1"); }catch(e){}
    }, 3200);
  }
  opener.addEventListener("click", function(ev){
    if(ev.target && ev.target.id === "dc-opener-x") return;
    openPanel();
    input.focus();
  });
  document.getElementById("dc-opener-x").addEventListener("click", function(ev){
    ev.stopPropagation();
    hideOpener();
  });
  document.getElementById("dc-close").addEventListener("click", function(){
    stopCam();
    panel.classList.remove("open");
  });
  document.getElementById("dc-face").addEventListener("click", function(){
    if(panel.classList.contains("open")){ stopCam(); panel.classList.remove("open"); }
    else{ openPanel(); input.focus(); }
  });
  input.addEventListener("focus", hideOpener);

  form.addEventListener("submit", function(ev){
    ev.preventDefault();
    var text = input.value.trim();
    if(!text || sending) return;
    openPanel();
    history.push({role: "user", content: text});
    save();
    bubble("user", text);
    input.value = "";
    sending = true;
    sendBtn.disabled = true;
    /* The typing indicator lands the same instant the send does. */
    var typing = document.createElement("div");
    typing.className = "dc-msg dave";
    typing.innerHTML = '<span class="dc-dots"><i></i><i></i><i></i></span>';
    msgs.appendChild(typing);
    msgs.scrollTop = msgs.scrollHeight;
    var payload = {session: sessionId, messages: history.map(function(m){
      return {role: m.role, content: m.content};
    })};
    if(identity) payload.identity = identity;
    fetch(CHAT, {
      method: "POST",
      credentials: "include",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    }).then(function(r){
      return r.ok ? r.json() : null;
    }).then(function(data){
      typing.remove();
      sending = false;
      sendBtn.disabled = false;
      if(data && data.dave_id) storeIdentity(data.dave_id);
      if(data && data.reply){
        var sv = splitVision(data.reply);
        var item = {role: "assistant", content: sv.text};
        if(sv.offer) item.v = 1;
        history.push(item);
        save();
        bubble("assistant", data.reply);
      }else{
        bubble("assistant", "That didn't get through to me — try me again in a moment.", "err");
      }
      input.focus();
    }).catch(function(){
      typing.remove();
      sending = false;
      sendBtn.disabled = false;
      bubble("assistant", "I can't be reached from here right now. Try again in a moment.", "err");
      input.focus();
    });
  });
})();
