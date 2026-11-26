#!/usr/bin/env python3
"""
Renders two showcases from the live VaultVale Hearthwood theme.css:
  1. screenshot.png (exact 512x288 16:9 thumbnail for Obsidian Community Themes)
  2. docs/hearthwood-showcase.png (1280x720 rich README gallery hero)
Zero third-party game IP references; original 16-bit pixel diorama + live CSS UI.
"""
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CSS_TEXT = (ROOT / "theme.css").read_text(encoding="utf-8")
OUT_THUMB = ROOT / "screenshot.png"
OUT_HERO = ROOT / "docs" / "hearthwood-showcase.png"

DIORAMA_JS = r"""
function drawPixelSplitBanner(canvas, lw, lh, scale) {
  canvas.width = lw * scale;
  canvas.height = lh * scale;
  const ctx = canvas.getContext('2d');
  ctx.imageSmoothingEnabled = false;
  const p = (x, y, w, h, c) => {
    ctx.fillStyle = c;
    ctx.fillRect(Math.round(x) * scale, Math.round(y) * scale, Math.round(w) * scale, Math.round(h) * scale);
  };
  const mid = Math.floor(lw / 2);

  // Left half sky (Warm Sunlit Hearthwood Dawn-Day)
  p(0, 0, mid, 9, '#4c86bc');
  p(0, 9, mid, 9, '#79aed5');
  p(0, 18, mid, 10, '#badbed');
  p(0, 28, mid, lh - 28, '#4f8342');

  // Sun & drifting pixel clouds
  p(10, 4, 6, 6, '#fde68a');
  p(11, 5, 4, 4, '#fef9c3');
  p(36, 6, 16, 3, '#fffdf7');
  p(39, 4, 9, 2, '#fffdf7');
  p(88, 7, 15, 3, '#f7f3ea');
  p(92, 5, 7, 2, '#fffdf7');

  // Distant sage hills
  for (let x = 0; x < mid; x += 2) {
    const h1 = Math.floor(7 + Math.sin(x * 0.065) * 3.5);
    p(x, 29 - h1, 2, h1, '#58826b');
    const h2 = Math.floor(4 + Math.cos(x * 0.11 + 1.2) * 2.5);
    p(x, 29 - h2, 2, h2, '#3a6648');
  }

  // Meadow turf & warm loam stratum bar
  p(0, 29, mid, 2, '#8cb856');
  p(0, 31, mid, 2, '#4f8342');
  p(0, 33, mid, lh - 33, '#5c3824');
  for (let x = 0; x < mid; x += 8) p(x, 33, 6, 1, '#9c663b');

  // Cedar Hearth Cottage
  const cx = 20;
  p(cx + 15, 11, 3, 7, '#64748b');
  p(cx + 16, 8, 2, 2, '#f8fafc');
  p(cx + 18, 5, 2, 2, '#e2e8f0');
  p(cx + 2, 14, 20, 2, '#7c3f23');
  p(cx + 0, 16, 24, 3, '#9a4d2c');
  p(cx + 4, 15, 16, 1, '#be6a3e');
  p(cx + 2, 19, 20, 10, '#a66b3c');
  p(cx + 2, 19, 20, 2, '#694022');
  p(cx + 5, 22, 4, 7, '#5c3419');
  p(cx + 6, 24, 1, 1, '#fbbf24');
  p(cx + 12, 21, 5, 4, '#3b2416');
  p(cx + 13, 22, 3, 2, '#fbbf24');
  p(cx + 14, 22, 1, 2, '#fef08a');

  // Pine trees
  const drawPine = (tx, gy) => {
    p(tx + 2, gy - 3, 2, 3, '#5c3824');
    p(tx, gy - 7, 6, 4, '#244d39');
    p(tx + 1, gy - 11, 4, 4, '#376c47');
    p(tx + 2, gy - 13, 2, 2, '#689d58');
  };
  drawPine(5, 29);
  drawPine(12, 29);
  drawPine(115, 29);

  // Campfire + Garden Bed + Crops + Ember Fox
  const fx = 53;
  p(fx, 28, 6, 2, '#475569');
  p(fx + 1, 25, 4, 3, '#ea580c');
  p(fx + 2, 23, 2, 3, '#fbbf24');
  p(fx + 2, 24, 1, 1, '#fef9c3');

  // Crops (Sunroot, Dewberry, Moonfern, Hearthwheat)
  p(68, 29, 32, 3, '#4a2e1b');
  p(71, 26, 2, 3, '#4d7c3f'); p(71, 24, 2, 2, '#f59e0b');
  p(79, 25, 3, 4, '#2f5929'); p(79, 25, 1, 1, '#60a5fa'); p(81, 26, 1, 1, '#93c5fd');
  p(87, 25, 3, 4, '#2a6f68'); p(88, 24, 2, 2, '#5eead4');
  p(94, 24, 3, 5, '#689d58'); p(94, 23, 3, 2, '#fde047');

  // Ember Fox
  const ax = 104;
  p(ax, 25, 4, 3, '#e06324');
  p(ax - 2, 25, 2, 2, '#fb923c');
  p(ax - 3, 25, 1, 1, '#fff7ed');
  p(ax + 3, 23, 3, 3, '#e06324');
  p(ax + 3, 22, 1, 1, '#9a3412');
  p(ax + 5, 22, 1, 1, '#9a3412');
  p(ax + 5, 24, 1, 1, '#0f172a');
  p(ax, 28, 1, 1, '#7c2d12');
  p(ax + 3, 28, 1, 1, '#7c2d12');

  // Right half (Starlit Subterranean Cavern Sanctum)
  p(mid, 0, lw - mid, 9, '#0d1322');
  p(mid, 9, lw - mid, 8, '#131b30');
  p(mid, 17, lw - mid, lh - 17, '#182238');

  // Scattered non-grid stars & crescent moon
  const stars = [
    [10, 3], [26, 7], [42, 4], [58, 8], [73, 3], [91, 6], [108, 4], [119, 9],
    [18, 11], [49, 10], [82, 11], [101, 10]
  ];
  stars.forEach(([sx, sy], idx) => {
    if (mid + sx < lw - 4) {
      p(mid + sx, sy, 1, 1, idx % 3 === 0 ? '#7dd3fc' : '#f1f5f9');
    }
  });
  p(lw - 18, 4, 4, 5, '#fde68a');
  p(lw - 16, 5, 3, 3, '#0d1322');

  // Stone cavern masonry backdrop + ceiling arch + stalactites
  p(mid, 14, lw - mid, 3, '#25334d');
  for (let row = 0; row < 2; row++) {
    const yy = 18 + row * 5;
    for (let x = mid + (row % 2) * 5 + 3; x < lw - 4; x += 10) {
      p(x, yy, 6, 3, '#1e2b45');
    }
  }
  [14, 38, 64, 92, 114].forEach((ox, idx) => {
    if (mid + ox < lw - 6) {
      p(mid + ox, 17, 3, 2 + (idx % 2), '#2c3d5c');
      p(mid + ox + 1, 19 + (idx % 2), 1, 1, '#3b5075');
    }
  });
  p(mid, 30, lw - mid, 3, '#243147');
  p(mid, 30, lw - mid, 1, '#476087');
  p(mid, 33, lw - mid, lh - 33, '#0f1624');

  // Hanging hearth lanterns with soft amber pixel aura
  const drawLantern = (lx) => {
    p(lx - 2, 19, 7, 7, 'rgba(251, 191, 36, 0.14)');
    p(lx + 1, 16, 1, 3, '#64748b');
    p(lx, 19, 3, 4, '#334155');
    p(lx + 1, 20, 1, 2, '#fbbf24');
    p(lx + 1, 20, 1, 1, '#fef9c3');
  };
  drawLantern(mid + 16);
  drawLantern(lw - 30);

  // Glowing crystal veins
  const drawCrystals = (kx, glow, c1, c2) => {
    p(kx - 1, 21, 8, 9, glow);
    p(kx + 2, 22, 2, 8, c1);
    p(kx + 2, 22, 1, 3, '#ffffff');
    p(kx, 25, 2, 5, c2);
    p(kx + 4, 24, 2, 6, c2);
    p(kx + 1, 30, 4, 1, c1);
  };
  drawCrystals(mid + 30, 'rgba(56, 189, 248, 0.18)', '#38bdf8', '#0284c7');
  drawCrystals(mid + 82, 'rgba(45, 212, 191, 0.18)', '#2dd4bf', '#0d9488');
  drawCrystals(lw - 16, 'rgba(167, 139, 250, 0.18)', '#a78bfa', '#7c3aed');

  // Brass relic chest & perched Barn Owl
  const chx = mid + 56;
  p(chx, 25, 7, 5, '#7c4726');
  p(chx, 25, 7, 2, '#9a5a32');
  p(chx, 27, 7, 1, '#f59e0b');
  p(chx + 3, 27, 1, 2, '#fef08a');

  const ox = mid + 69;
  p(ox, 11, 3, 3, '#e2e8f0');
  p(ox + 1, 12, 1, 1, '#fbbf24');
  p(ox, 10, 1, 1, '#94a3b8');
  p(ox + 2, 10, 1, 1, '#94a3b8');

  // Center hearth pillar bridge
  p(mid - 2, 0, 4, lh, '#3b2418');
  p(mid - 1, 0, 2, lh, '#9c663b');
  p(mid - 1, 29, 2, 3, '#fbbf24');
}
"""


def build_html(compact: bool) -> str:
    extra_css = f"""
    {CSS_TEXT}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: {512 if compact else 1280}px;
      height: {288 if compact else 720}px;
      overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #141c28;
    }}
    .frame {{
      display: flex;
      flex-direction: column;
      width: 100%;
      height: 100%;
    }}
    .banner-wrap {{
      position: relative;
      width: 100%;
      height: {74 if compact else 184}px;
      flex: 0 0 auto;
      border-bottom: 2px solid #24160e;
      background: #111723;
    }}
    #vv-banner {{
      display: block;
      width: 100%;
      height: 100%;
      image-rendering: pixelated;
    }}
    .split {{
      flex: 1 1 auto;
      min-height: 0;
      display: grid;
      grid-template-columns: 1fr 1fr;
    }}
    .pane {{
      display: grid;
      grid-template-columns: {72 if compact else 180}px 1fr;
      background: var(--background-primary);
      color: var(--text-normal);
      min-height: 0;
      overflow: hidden;
      border-right: 2px solid #3b2418;
    }}
    .pane.theme-dark {{
      border-right: 0;
    }}
    .sidebar {{
      background: var(--background-secondary);
      border-right: 1px solid var(--background-modifier-border);
      padding: {6 if compact else 14}px {5 if compact else 12}px;
      font-size: {7.8 if compact else 13.5}px;
      line-height: 1.4;
      color: var(--text-muted);
    }}
    .mode-chip {{
      display: inline-block;
      margin-bottom: {4 if compact else 9}px;
      padding: {1 if compact else 3}px {4 if compact else 8}px;
      font-size: {6.8 if compact else 11}px;
      font-weight: 800;
      letter-spacing: 0.04em;
      background: var(--interactive-accent);
      color: var(--text-on-accent);
      box-shadow: 2px 2px 0 var(--vv-pixel-shadow);
    }}
    .sb-head {{
      font-weight: 800;
      font-size: {8.2 if compact else 14}px;
      color: var(--text-normal);
      margin-bottom: {4 if compact else 10}px;
      padding-bottom: {3 if compact else 6}px;
      border-bottom: 1px solid var(--background-modifier-border);
    }}
    .nav-file-title {{
      padding: {2 if compact else 5}px {4 if compact else 8}px;
      margin-bottom: {2 if compact else 4}px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .nav-file-title.is-active {{
      background: var(--background-modifier-active-hover);
      color: var(--text-normal);
      font-weight: 700;
    }}
    .editor {{
      padding: {7 if compact else 18}px {9 if compact else 26}px;
      font-size: {8.3 if compact else 14}px;
      line-height: {1.4 if compact else 1.6};
    }}
    .markdown-rendered h1 {{
      font-size: {12 if compact else 24}px;
      line-height: 1.2;
      color: var(--h1-color);
      margin-bottom: {4 if compact else 8}px;
      font-weight: 800;
    }}
    .markdown-rendered h2 {{
      font-size: {9.8 if compact else 18}px;
      line-height: 1.25;
      color: var(--h2-color);
      margin: {5 if compact else 12}px 0 {3 if compact else 6}px;
      font-weight: 700;
    }}
    .tags {{
      display: flex;
      gap: {4 if compact else 8}px;
      margin-bottom: {4 if compact else 10}px;
      flex-wrap: wrap;
    }}
    .tag {{
      font-size: {7.2 if compact else 12}px;
      padding: {1 if compact else 2}px {4 if compact else 9}px;
      color: var(--tag-color);
      background: var(--tag-background);
      border: 1px solid var(--tag-border-color);
      display: inline-block;
    }}
    .internal-link {{
      color: var(--link-color);
      text-decoration: underline;
      font-weight: 600;
    }}
    .markdown-rendered blockquote {{
      margin: {4 if compact else 10}px 0;
      padding: {3 if compact else 8}px {6 if compact else 12}px;
      font-size: {7.6 if compact else 13}px;
    }}
    .markdown-rendered hr {{
      margin: {5 if compact else 12}px 0;
    }}
    .task-list {{
      list-style: none;
      margin-top: {4 if compact else 8}px;
      font-size: {7.8 if compact else 13}px;
    }}
    .task-list li {{
      display: flex;
      align-items: center;
      gap: {4 if compact else 8}px;
      margin-bottom: {3 if compact else 6}px;
    }}
    {" .markdown-rendered input[type='checkbox'].task-list-item-checkbox { width: 10px; height: 10px; background-size: 8px 8px; } " if compact else ""}
    .markdown-rendered pre {{
      margin-top: {4 if compact else 10}px;
      padding: {4 if compact else 9}px {6 if compact else 12}px;
      background: var(--code-background);
      color: var(--code-normal);
      font-family: monospace;
      font-size: {7.4 if compact else 12.5}px;
    }}
    .markdown-rendered table {{
      width: 100%;
      margin-top: {5 if compact else 10}px;
      font-size: {7.6 if compact else 12.5}px;
    }}
    .markdown-rendered th,
    .markdown-rendered td {{
      padding: {2 if compact else 5}px {4 if compact else 9}px;
      text-align: left;
      border-bottom: 1px solid var(--background-modifier-border);
    }}
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <style>{extra_css}</style>
</head>
<body>
  <div class="frame">
    <div class="banner-wrap">
      <canvas id="vv-banner"></canvas>
    </div>
    <div class="split">
      <section class="pane theme-light">
        <aside class="sidebar">
          <div class="mode-chip">LIGHT · PARCHMENT</div>
          <div class="sb-head">HearthStudy</div>
          <div class="nav-file-title is-active">Daily Log</div>
          <div class="nav-file-title">Crop Guide</div>
          <div class="nav-file-title">Systems MOC</div>
          <div class="nav-file-title">Book Notes</div>
          <div class="nav-file-title">Archive</div>
        </aside>
        <article class="editor markdown-rendered">
          <h1>Field Notes</h1>
          <div class="tags">
            <span class="tag">#journal</span>
            <span class="tag">#homestead</span>
          </div>
          <p>Linked from <span class="internal-link">[[Systems MOC]]</span>.</p>
          <blockquote>Warm cedar ink on sunlit parchment built for calm focus.</blockquote>
          <h2>Today&apos;s Harvest</h2>
          <ul class="task-list">
            <li><input type="checkbox" class="task-list-item-checkbox" checked /><span>Outline study plan</span></li>
            <li><input type="checkbox" class="task-list-item-checkbox" /><span>Tend evening garden</span></li>
          </ul>
          <hr />
          <table>
            <thead><tr><th>Stratum</th><th>Notes</th></tr></thead>
            <tbody>
              <tr><td>Loam</td><td>14</td></tr>
              <tr><td>Moss</td><td>19</td></tr>
            </tbody>
          </table>
        </article>
      </section>

      <section class="pane theme-dark">
        <aside class="sidebar">
          <div class="mode-chip">DARK · CAVERN</div>
          <div class="sb-head">NightVault</div>
          <div class="nav-file-title">Cabin Map</div>
          <div class="nav-file-title is-active">Crystal Hub</div>
          <div class="nav-file-title">Spore Index</div>
          <div class="nav-file-title">Deep Lore</div>
          <div class="nav-file-title">Snippets</div>
        </aside>
        <article class="editor markdown-rendered">
          <h1>Crystal Sanctum</h1>
          <div class="tags">
            <span class="tag">#cavern</span>
            <span class="tag">#relics</span>
          </div>
          <p>Hub linked via <span class="internal-link">[[Spore Index]]</span>.</p>
          <blockquote>Slate depths with amber hearth lanterns &amp; crystal cues.</blockquote>
          <h2>Deep Veins</h2>
          <pre>streak: 14d · 6,240 words</pre>
          <hr />
          <table>
            <thead><tr><th>Chamber</th><th>Links</th></tr></thead>
            <tbody>
              <tr><td>Grotto III</td><td>32</td></tr>
              <tr><td>Sanctum IV</td><td>48</td></tr>
            </tbody>
          </table>
        </article>
      </section>
    </div>
  </div>
  <script>
    {DIORAMA_JS}
    drawPixelSplitBanner(
      document.getElementById('vv-banner'),
      {256 if compact else 320},
      {37 if compact else 46},
      {2 if compact else 4}
    );
  </script>
</body>
</html>"""


def main():
    OUT_HERO.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        p1 = browser.new_page(viewport={"width": 512, "height": 288}, device_scale_factor=1)
        p1.set_content(build_html(compact=True), wait_until="load")
        p1.screenshot(path=str(OUT_THUMB))
        p1.close()

        p2 = browser.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
        p2.set_content(build_html(compact=False), wait_until="load")
        p2.screenshot(path=str(OUT_HERO))
        p2.close()

        browser.close()

    assert Image.open(OUT_THUMB).size == (512, 288)
    assert Image.open(OUT_HERO).size == (1280, 720)
    print("Generated:", OUT_THUMB, Image.open(OUT_THUMB).size)
    print("Generated:", OUT_HERO, Image.open(OUT_HERO).size)


if __name__ == "__main__":
    main()
