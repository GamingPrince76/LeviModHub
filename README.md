# LeviModHub

LeviModHub is the mod list used by LeviLauncher.

## Add a mod

1. Fork this repository.
2. Create `mods/your-mod-id/mod.json`.
3. Optionally add a square `icon.png` in the same folder, or use an HTTPS `icon_url`.
4. Open a pull request.

Use lowercase letters, numbers, dots, dashes, or underscores for the folder name and `id`. The folder name and `id` must match.

```json
{
  "id": "your-mod-id",
  "name": "Your Mod",
  "author": "Your Name",
  "description": "A short explanation of what the mod does.",
  "homepage_url": "https://github.com/you/your-mod",
  "tags": ["Utility", "HUD"],
  "releases": [
    {
      "version": "1.0.0",
      "minecraft_versions": ["1.26.45.1", "1.26.5X.X"],
      "download_type": "direct",
      "download_url": "https://github.com/you/your-mod/releases/download/v1.0.0/YourMod.levipack",
      "published_at": "2026-09-10T12:00:00Z"
    }
  ]
}
```

Add `icon_url` if the icon is hosted elsewhere:

```json
"icon_url": "https://example.com/your-mod.png"
```

If neither `icon.png` nor `icon_url` is provided, LeviLauncher uses its own logo.

## Minecraft versions

List every Minecraft version supported by a release. Exact versions are safest:

```json
"minecraft_versions": ["1.26.45.1", "1.26.50.2"]
```

Use `X` when the same build is known to work across a hotfix family:

```json
"minecraft_versions": ["1.26.5X.X"]
```

`1.26.5X.X` matches versions from `1.26.50.0` through `1.26.59.X`. An `X` inside a number matches one digit, while an `X` used as the whole section matches any numeric value.

When Minecraft updates and the mod needs a new build, add a new item at the top of `releases`. Keep old releases so players using older Minecraft versions can still install the correct one.

## Downloads

Use `direct` for a direct `.levipack`, `.zip`, or `.so` link. LeviLauncher downloads and imports it inside the app.

Use `browser` when the developer needs people to visit a download page:

```json
"download_type": "browser",
"download_url": "https://your-site.example/download"
```

Use `ad` when the download page is supported by ads:

```json
"download_type": "ad",
"download_url": "https://your-link.example/download"
```

The launcher labels the download type and explains the steps before opening an external page. After downloading, the player returns to the Mods page and taps **Scan**. Scan checks the main Downloads folder for `.levipack` and `.so` files.

## What happens after a pull request

The catalog check reads every `mods/*/mod.json` file and rejects missing fields, invalid links, or invalid download types. After a pull request is merged, GitHub Actions generates the catalog and publishes it through GitHub Pages. The generated catalog is not stored in the repository.

LeviLauncher fetches `https://qycottage.github.io/LeviModHub/catalog.json` when the External Mods page opens.
