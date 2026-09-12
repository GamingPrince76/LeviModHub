# LeviModHub

LeviModHub is the external mod catalog used by LeviLauncher on Android.

Mods can still use the old manual catalog format, but GitHub-hosted mods can now use the automatic release system. With the automatic system, a mod only needs to be accepted into LeviModHub once. After that, new releases are picked up from the mod's own GitHub repository.

## Adding a mod with automatic updates

First, add a `levimod.json` file to the root of your mod repository.

A working example can be found here:

[QYCottage/BedrockTools - levimod.json](https://github.com/QYCottage/BedrockTools/blob/main/levimod.json)

Example:

```json
{
  "schema_version": 1,
  "id": "your-mod-id",
  "version": "1.0.0",
  "minecraft_versions": [
    "1.26.45.1"
  ],
  "info": {
    "name": "Your Mod",
    "author": "Your Name",
    "description": "A short description of your mod.",
    "homepage_url": "https://github.com/you/your-mod",
    "icon": "assets/icon.png",
    "tags": [
      "Utility"
    ]
  },
  "release_assets": {
    "include": [
      "*.levipack",
      "*.so"
    ],
    "labels": {
      "YourMod.levipack": "LeviPack",
      "libYourMod.so": "Native library"
    }
  }
}
```

Then fork LeviModHub and create:

```text
mods/your-mod-id/mod.json
```

Example:

```json
{
  "id": "your-mod-id",
  "provider": "github",
  "repository": "you/your-mod",
  "metadata_path": "levimod.json",
  "include_prereleases": false,
  "max_releases": 20,
  "enabled": true
}
```

The folder name and `id` must match. Use lowercase letters, numbers, dots, dashes, or underscores for the ID.

Open a pull request after adding the entry. This is normally the only LeviModHub pull request needed for the mod.

## Publishing updates

For future updates, everything is done from the mod repository.

1. Update the version and supported Minecraft versions in `levimod.json`.
2. Commit the changes.
3. Create a matching Git tag and GitHub Release.
4. Upload the `.levipack`, `.so`, or `.zip` file to the GitHub Release.

For example, if `levimod.json` contains:

```json
"version": "1.5.0"
```

create the tag:

```text
v1.5.0
```

LeviModHub checks approved repositories automatically and updates the catalog when a new release is found. There is no need to open another LeviModHub pull request for normal version updates.

The `levimod.json` file must be committed before the release tag is created. This lets each release keep its own Minecraft version information.

## Minecraft versions

List the Minecraft versions supported by that release:

```json
"minecraft_versions": [
  "1.26.45.1"
]
```

Multiple versions can be listed:

```json
"minecraft_versions": [
  "1.26.45.1",
  "1.26.50.2"
]
```

`X` can be used for a known compatible version range:

```json
"minecraft_versions": [
  "1.26.5X.X"
]
```

`>=` can be used when a mod supports one Minecraft version and every newer version:

```json
"minecraft_versions": [
  ">=1.26.45.1"
]
```

This matches `1.26.45.1`, `1.26.46.3`, `1.26.50.1`, `1.27.0`, and newer versions.

## Release files

By default, LeviModHub can use these files from GitHub Releases:

- `.levipack`
- `.so`
- `.zip`

If a release contains more than one supported file, newer LeviLauncher versions can let the user choose which one to install.

`release_assets` is optional. It can be used to choose which files should appear or give them better names:

```json
"release_assets": {
  "include": [
    "*.levipack",
    "*.so"
  ],
  "exclude": [
    "*debug*"
  ],
  "labels": {
    "YourMod.levipack": "LeviPack",
    "libYourMod.so": "Native library"
  }
}
```

GitHub-based entries use files attached to the approved repository's GitHub Releases. External or paid download links are not accepted through `levimod.json`.

## Existing mods

The old manual `mod.json` format is still supported. Existing mods do not need to migrate immediately.

Developers can move to the automatic GitHub system whenever they are ready. Once migrated, future release updates can be handled completely from their own repository.

## Notes

- Draft GitHub Releases are ignored.
- Prereleases are ignored unless `include_prereleases` is enabled in LeviModHub.
- `max_releases` controls how many recent GitHub Releases are checked and kept in the catalog.
- The mod version in `levimod.json` must match the GitHub release tag.
