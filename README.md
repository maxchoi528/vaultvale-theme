# VaultVale Hearthwood — Cozy Parchment & Subterranean Slate Theme for Obsidian

A clean, high-contrast Obsidian theme crafted by **HearthCraft Lab** to pair seamlessly with the **VaultVale** pixel homestead & subterranean cavern plugin.

- **Light Mode (Hearthwood Parchment)**: Warm cedar ink (`#291b12`) on comfortable sunlit parchment (`#f6efe2`) with sage accents and honey-oak bevel hairlines.
- **Dark Mode (Subterranean Cavern Slate)**: Parchment-tinted text (`#eee4d2`) on calm deep slate (`#161e2b`) with lantern amber and crystal cyan highlights.
- **Zero External Assets**: Pure CSS variables, tabular numerals in tables, zero remote font requests, and readable typography for long writing sessions.

## Installation

### From Obsidian Community Themes
1. Open **Settings -> Appearance -> Themes -> Manage**.
2. Search for **VaultVale Hearthwood**.
3. Click **Install and use**.

### Manual Installation
1. Download `manifest.json` and `theme.css` from the [latest GitHub release](https://github.com/maxchoi528/vaultvale-theme/releases/latest).
2. Create the folder `<your-vault>/.obsidian/themes/VaultVale Hearthwood/` and place both files inside it.
3. Reload themes in **Settings -> Appearance -> Themes** and select **VaultVale Hearthwood**.

## Usage & Customization

- Switch between **Light** (**Hearthwood Parchment**) and **Dark** (**Subterranean Cavern Slate**) under **Settings -> Appearance -> Base color scheme**.
- To customize accent or reading colors via an Obsidian CSS snippet (**Settings -> Appearance -> CSS snippets**), override theme variables cleanly:

```css
.theme-light {
  --interactive-accent: #3d6f36;
  --file-line-width: 48rem;
}

.theme-dark {
  --interactive-accent: #f2aa48;
  --background-primary: #161e2b;
}
```

## Companion Plugin

Pair this theme with the **[VaultVale Community Plugin](https://vaultvale.pages.dev/)** to turn your daily notes, tasks, and folder backlinks into a living 16-bit homestead and explorable subterranean cavern.

- Website & Interactive Sandbox: [https://vaultvale.pages.dev/](https://vaultvale.pages.dev/)
- Optional Pro Upgrade: [VaultVale Pro on Gumroad](https://yujun57.gumroad.com/l/vaultvale-pro-lifetime)

[MIT License](LICENSE)
