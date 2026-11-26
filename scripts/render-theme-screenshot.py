#!/usr/bin/env python3
"""
Renders an exact 512x288 (16:9) Obsidian theme preview screenshot for VaultVale Hearthwood
showing Light (Hearthwood Parchment) and Dark (Subterranean Cavern Slate) side by side.
"""
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CSS_TEXT = (ROOT / "theme.css").read_text(encoding="utf-8")
OUT_PNG = ROOT / "screenshot.png"

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <style>
    {CSS_TEXT}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: 512px;
      height: 288px;
      overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    .split {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      width: 512px;
      height: 288px;
    }}
    .pane {{
      display: grid;
      grid-template-columns: 78px 1fr;
      background: var(--background-primary);
      color: var(--text-normal);
      height: 288px;
      overflow: hidden;
      border-right: 1px solid var(--background-modifier-border);
    }}
    .pane.theme-dark {{
      border-right: 0;
    }}
    .sidebar {{
      background: var(--background-secondary);
      border-right: 1px solid var(--background-modifier-border);
      padding: 8px 6px;
      font-size: 8.5px;
      line-height: 1.45;
      color: var(--text-muted);
    }}
    .sb-head {{
      font-weight: 700;
      font-size: 9px;
      color: var(--text-normal);
      margin-bottom: 6px;
      letter-spacing: 0.02em;
    }}
    .sb-item {{
      padding: 2px 4px;
      border-radius: 3px;
      margin-bottom: 2px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .sb-item.is-active {{
      background: var(--background-modifier-active-hover);
      color: var(--text-normal);
      font-weight: 600;
    }}
    .editor {{
      padding: 10px 12px;
      font-size: 9px;
      line-height: 1.5;
    }}
    .mode-pill {{
      display: inline-block;
      font-size: 7.5px;
      font-weight: 700;
      padding: 1px 5px;
      border-radius: 3px;
      background: var(--interactive-accent);
      color: var(--text-on-accent);
      margin-bottom: 5px;
      letter-spacing: 0.03em;
    }}
    h1 {{
      font-size: 13px;
      line-height: 1.2;
      color: var(--h1-color);
      margin-bottom: 4px;
    }}
    h2 {{
      font-size: 10px;
      color: var(--h2-color);
      margin: 6px 0 3px;
    }}
    .tags {{
      display: flex;
      gap: 4px;
      margin-bottom: 6px;
    }}
    .tag {{
      font-size: 7.5px;
      padding: 1px 5px;
      border-radius: var(--tag-radius);
      color: var(--tag-color);
      background: var(--tag-background);
      border: 1px solid var(--tag-border-color);
    }}
    .link {{
      color: var(--link-color);
      text-decoration: underline;
    }}
    .markdown-rendered blockquote {{
      margin: 5px 0;
      padding: 4px 7px;
      border-left: 3px solid var(--blockquote-border-color);
      background: var(--blockquote-background-color);
      font-size: 8.2px;
      color: var(--text-normal);
    }}
    .markdown-rendered table {{
      width: 100%;
      margin-top: 6px;
      font-size: 8px;
      border: 1px solid var(--background-modifier-border);
    }}
    .markdown-rendered th,
    .markdown-rendered td {{
      padding: 2px 5px;
      text-align: left;
      border-bottom: 1px solid var(--background-modifier-border);
    }}
    .task-list {{
      list-style: none;
      margin-top: 5px;
      font-size: 8.2px;
    }}
    .task-list li {{
      display: flex;
      align-items: center;
      gap: 4px;
      margin-bottom: 2px;
    }}
    .chk {{
      width: 8px;
      height: 8px;
      border-radius: 2px;
      border: 1px solid var(--interactive-accent);
      display: inline-block;
    }}
    .chk.done {{
      background: var(--interactive-accent);
    }}
    pre {{
      margin-top: 5px;
      padding: 4px 6px;
      border-radius: 4px;
      background: var(--code-background);
      color: var(--code-normal);
      font-family: ui-monospace, monospace;
      font-size: 7.5px;
    }}
  </style>
</head>
<body>
  <div class="split">
    <section class="pane theme-light">
      <aside class="sidebar">
        <div class="sb-head">HearthStudy</div>
        <div class="sb-item is-active">Daily Log</div>
        <div class="sb-item">Field Notes</div>
        <div class="sb-item">Systems MOC</div>
        <div class="sb-item">Reading 2026</div>
        <div class="sb-item">Archive</div>
      </aside>
      <article class="editor markdown-rendered">
        <span class="mode-pill">HEARTHWOOD LIGHT</span>
        <h1>Field Notes · Autumn</h1>
        <div class="tags">
          <span class="tag">#journal</span>
          <span class="tag">#botany</span>
        </div>
        <p>Linked from <span class="link">[[Systems MOC]]</span> for daily review.</p>
        <blockquote>Warm parchment contrast built for calm long-form study.</blockquote>
        <ul class="task-list">
          <li><span class="chk done"></span><span>Review morning highlights</span></li>
          <li><span class="chk"></span><span>Index geology strata</span></li>
        </ul>
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
        <div class="sb-head">NightVault</div>
        <div class="sb-item">Surface Cabin</div>
        <div class="sb-item is-active">Crystal Grotto</div>
        <div class="sb-item">Spore Atlas</div>
        <div class="sb-item">Sanctum Index</div>
        <div class="sb-item">Snippets</div>
      </aside>
      <article class="editor markdown-rendered">
        <span class="mode-pill">CAVERN SLATE DARK</span>
        <h1>Subterranean Index</h1>
        <div class="tags">
          <span class="tag">#cavern</span>
          <span class="tag">#research</span>
        </div>
        <p>Core hub linked via <span class="link">[[Obsidian Sanctum]]</span>.</p>
        <blockquote>Deep slate elevation with lantern amber &amp; crystal cyan cues.</blockquote>
        <pre>streak: 14 days · 6,240 words</pre>
        <table>
          <thead><tr><th>Vein</th><th>Backlinks</th></tr></thead>
          <tbody>
            <tr><td>Grotto</td><td>32</td></tr>
            <tr><td>Sanctum</td><td>48</td></tr>
          </tbody>
        </table>
      </article>
    </section>
  </div>
</body>
</html>
"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 512, "height": 288}, device_scale_factor=1)
        page.set_content(HTML, wait_until="load")
        page.screenshot(path=str(OUT_PNG))
        browser.close()
    img = Image.open(OUT_PNG)
    assert img.size == (512, 288), f"Expected 512x288, got {img.size}"
    print("Generated exact theme preview:", OUT_PNG, img.size)


if __name__ == "__main__":
    main()
