import re
from pathlib import Path

MANIFEST_PATH = Path(__file__).resolve().parent.parent / "wp_audio_trigger" / "config.yaml"

def bump_patch(version: str) -> str:
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version.strip())
    if not m:
        # If not semver patch, fallback to minor bump like 0.1.12 -> 0.1.13 treating last part as patch
        parts = version.strip().split(".")
        if len(parts) >= 2:
            try:
                parts[-1] = str(int(parts[-1]) + 1)
                return ".".join(parts)
            except ValueError:
                return version
        return version
    major, minor, patch = map(int, m.groups())
    patch += 1
    return f"{major}.{minor}.{patch}"

def main():
    if not MANIFEST_PATH.exists():
        print(f"Manifest not found: {MANIFEST_PATH}")
        return 0
    text = MANIFEST_PATH.read_text(encoding="utf-8")
    # Find version: "x.y.z" and bump
    m = re.search(r"^version:\s*\"([^\"]+)\"\s*$", text, re.MULTILINE)
    if not m:
        print("No version field found to bump.")
        return 0
    current = m.group(1)
    new_version = bump_patch(current)
    if new_version == current:
        print(f"Version unchanged: {current}")
        return 0
    updated = re.sub(r"^version:\s*\"[^\"]+\"\s*$", f"version: \"{new_version}\"", text, flags=re.MULTILINE)
    MANIFEST_PATH.write_text(updated, encoding="utf-8")
    print(f"Bumped version: {current} -> {new_version}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
