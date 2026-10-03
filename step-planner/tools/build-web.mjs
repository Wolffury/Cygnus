// Builds the claude.ai artifact copy of the planner: page content without the <html>/<head> wrapper,
// script lowered to ES2017 and CSS given fallbacks so older tablet browsers (Chrome/WebView 61+) run it,
// plus an error banner so a failure shows a message instead of a dead page.
// Usage: node tools/build-web.mjs <output.html>
import { readFileSync, writeFileSync } from "node:fs";
import { transformSync } from "esbuild";

const src = readFileSync(new URL("../index.html", import.meta.url), "utf8");
const head = src.slice(src.indexOf("<title>"), src.indexOf("</head>")).replace(/<link rel="preconnect"[^>]*>\n/g, "");
// the last </body>: the quote template inside the script contains one too
let body = src.slice(src.indexOf("<body>") + 6, src.lastIndexOf("</body>"));

const open = "<script>\n", start = body.indexOf(open), end = body.lastIndexOf("</script>");
const js = body.slice(start + open.length, end);
const lowered = transformSync(js + "\nwindow.__bspReady = true;\n", { loader: "js", target: "es2017", charset: "utf8" }).code;
body = body.slice(0, start) + open + lowered.replace(/<\/script/gi, "<\\/script") + body.slice(end);

const guard = `<script>
(function () {
  function show(msg) {
    var b = document.getElementById("bspErr");
    if (!b) { b = document.createElement("div"); b.id = "bspErr"; b.setAttribute("role", "alert");
      b.style.cssText = "position:fixed;left:12px;right:12px;top:12px;z-index:99;background:#b3261e;color:#fff;padding:12px 14px;border-radius:8px;font:14px/1.4 system-ui,sans-serif";
      (document.body || document.documentElement).appendChild(b); }
    b.textContent = msg;
  }
  window.onerror = function (msg, src, line) { show("Something went wrong: " + msg + (line ? " (line " + line + ")" : "") + ". Send Claude a screenshot of this."); };
  setTimeout(function () { if (!window.__bspReady) show("The planner didn't start. Your browser may be out of date: update Chrome or Android System WebView from the Play Store, then reopen this page."); }, 6000);
})();
</script>
`;

// CSS fallbacks for browsers without color-mix() or the inset shorthand
let css = head
  .replace(/inset:\s*0;/g, "top: 0; right: 0; bottom: 0; left: 0;")
  .replace(/background:\s*color-mix\(in srgb, var\(--panel\)[^;]*;/g, (m) => "background: var(--panel); " + m)
  .replace(/background:\s*color-mix\(in srgb, var\(--(good|warn|bad)\)[^;]*;/g, (m) => "background: var(--chip); " + m);

writeFileSync(process.argv[2], css + guard + body);
console.log("wrote", process.argv[2], (css + guard + body).length, "bytes");
