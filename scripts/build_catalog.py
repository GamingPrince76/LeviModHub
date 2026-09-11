import json
from pathlib import Path
from urllib.parse import urlparse


root = Path(__file__).resolve().parents[1]
mods_root = root / "mods"
required_text = ("id", "name", "author", "description")
allowed_download_types = {"direct", "browser", "ad"}
allowed_direct_extensions = {".levipack", ".zip", ".so"}


def require_text(data, key, source):
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{source}: {key} is required")
    return value.strip()


def require_https(value, field, source):
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"{source}: {field} must be an HTTPS URL")
    return value


def load_mod(source):
    data = json.loads(source.read_text(encoding="utf-8"))
    for key in required_text:
        data[key] = require_text(data, key, source)
    if data["id"] != source.parent.name:
        raise ValueError(f"{source}: id must match its folder name")

    icon_url = data.get("icon_url")
    local_icon = source.parent / "icon.png"
    if isinstance(icon_url, str) and icon_url.strip():
        data["icon_url"] = require_https(icon_url.strip(), "icon_url", source)
    elif local_icon.is_file():
        data["icon_url"] = (
            "https://raw.githubusercontent.com/QYCottage/LeviModHub/main/"
            f"mods/{data['id']}/icon.png"
        )
    else:
        data.pop("icon_url", None)

    homepage_url = data.get("homepage_url", "")
    if homepage_url:
        data["homepage_url"] = require_https(homepage_url, "homepage_url", source)

    tags = data.get("tags", [])
    if not isinstance(tags, list) or any(not isinstance(tag, str) or not tag.strip() for tag in tags):
        raise ValueError(f"{source}: tags must be a list of text values")
    data["tags"] = [tag.strip() for tag in tags]

    releases = data.get("releases")
    if not isinstance(releases, list) or not releases:
        raise ValueError(f"{source}: add at least one release")
    for release in releases:
        version = require_text(release, "version", source)
        release["version"] = version
        versions = release.get("minecraft_versions")
        if not isinstance(versions, list) or not versions:
            raise ValueError(f"{source}: every release needs minecraft_versions")
        if any(not isinstance(item, str) or not item.strip() for item in versions):
            raise ValueError(f"{source}: minecraft_versions must contain text values")
        release["minecraft_versions"] = [item.strip() for item in versions]
        download_type = require_text(release, "download_type", source).lower()
        if download_type not in allowed_download_types:
            raise ValueError(f"{source}: download_type must be direct, browser, or ad")
        release["download_type"] = download_type
        download_url = require_https(require_text(release, "download_url", source), "download_url", source)
        release["download_url"] = download_url
        if download_type == "direct" and Path(urlparse(download_url).path).suffix.lower() not in allowed_direct_extensions:
            raise ValueError(f"{source}: direct downloads must end in .levipack, .zip, or .so")
        release["published_at"] = require_text(release, "published_at", source)

    data["releases"].sort(key=lambda release: release["published_at"], reverse=True)
    return data


mods = [load_mod(source) for source in sorted(mods_root.glob("*/mod.json"))]
ids = [mod["id"] for mod in mods]
if len(ids) != len(set(ids)):
    raise ValueError("Duplicate mod id")
mods.sort(key=lambda mod: mod["name"].casefold())
output = root / "dist"
output.mkdir(exist_ok=True)
(output / "catalog.json").write_text(
    json.dumps({"schema_version": 1, "mods": mods}, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
