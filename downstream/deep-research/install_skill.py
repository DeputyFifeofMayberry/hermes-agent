"""Install a complete, pinned research skill with native Windows instructions."""

import argparse
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def install(archive, destination, python, profile_home, include_development_files=False):
    pin = json.loads((HERE / "upstream.json").read_text(encoding="utf-8"))
    if digest(archive.read_bytes()) != pin["archive_sha256"]:
        raise ValueError("Upstream archive hash differs from the reviewed pin")
    receipt = destination / "downstream-install.json"
    if destination.exists():
        saved = json.loads(receipt.read_text(encoding="utf-8"))
        if saved["commit"] != pin["commit"] or saved["adaptation"] != pin["adaptation"]:
            raise ValueError("Installed revision differs; preserve it before upgrading")
        for relative, expected in saved["files"].items():
            if digest((destination / relative).read_bytes()) != expected:
                raise ValueError(f"Local edit preserved: {relative}")
        print(f"Already installed and verified: {destination}")
        return

    prefix = f"hermes-deep-research-{pin['commit']}/"
    files = {}
    with zipfile.ZipFile(archive) as bundle:
        for entry in bundle.infolist():
            if entry.is_dir():
                continue
            if not entry.filename.startswith(prefix):
                raise ValueError("Unexpected archive root")
            relative = entry.filename[len(prefix):]
            parts = PurePosixPath(relative)
            if parts.is_absolute() or ".." in parts.parts or "\\" in relative:
                raise ValueError("Unsafe archive path")
            files[relative] = bundle.read(entry)
    for required in ("SKILL.md", "LICENSE", "scripts/research_state.py", "scripts/document_gate.py",
                     "references/source-review.md", "templates/report.md", "tests/test_research_state.py"):
        if required not in files:
            raise ValueError(f"Incomplete skill package: {required}")

    text = files["SKILL.md"].decode("utf-8")
    lines = text.splitlines()
    lines[2] = "description: Research questions in depth with verified sources."
    lines.insert(3, "author: Gyu-bot; Windows integration by DeputyFifeofMayberry")
    text = "\n".join(lines) + "\n"
    text = text.replace("# Hermes Deep Research\n", "# Hermes Deep Research\n\n"
                        "On Windows, read [references/windows.md](references/windows.md) first. "
                        "Its PowerShell invocation and cleanup limits override the Bash examples below.\n", 1)
    text = text.replace("For Wave 1, include Korean and English by default when useful,",
                        "For Wave 1, use English by default and include other languages when useful,")
    files["SKILL.md"] = text.encode("utf-8")

    # The original cleanup tests require POSIX directory descriptors and symlinks.
    # Run them on POSIX; Windows has its own refusal/preservation contract below.
    test = files["tests/test_research_state.py"].decode("utf-8")
    for name in ("is_dry_run_by_default_and_preserves_durable_files", "refuses_active_or_unsafe_runs",
                 "refuses_tmp_symlink_swap_after_snapshot", "refuses_real_child_directory_replacement",
                 "refuses_real_tmp_replacement_before_descriptor_binding",
                 "refuses_real_run_replacement_before_descriptor_binding"):
        test = test.replace(f"    def test_cleanup_{name}",
                            '    @unittest.skipUnless(os.name == "posix", "POSIX cleanup descriptors")\n'
                            f"    def test_cleanup_{name}")
    test = test.replace('{"HOME": temporary}, clear=True',
                        '{"HOME": temporary, "USERPROFILE": temporary}, clear=True')
    files["tests/test_research_state.py"] = test.encode("utf-8")
    for source, target in (("windows.md", "references/windows.md"),
                           ("research.ps1", "scripts/research.ps1"),
                           ("test_windows.py", "tests/test_windows.py")):
        files[target] = (HERE / source).read_bytes()
    if not include_development_files:
        files = {name: data for name, data in files.items()
                 if not name.startswith("tests/") and name not in ("README.md", "README.ko.md", ".gitignore")}
    files["windows-runtime.json"] = (json.dumps({"python": str(python.resolve()),
                                                 "profile_home": str(profile_home.resolve())}, indent=2)
                                      + "\n").encode("utf-8")
    destination.mkdir(parents=True)
    for relative, data in files.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    saved = {**pin, "files": {name: digest(data) for name, data in files.items()}}
    receipt.write_text(json.dumps(saved, indent=2) + "\n", encoding="utf-8")
    print(f"Installed complete skill: {destination}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("archive", "destination", "python", "profile-home"):
        parser.add_argument("--" + name, required=True, type=Path)
    parser.add_argument("--include-development-files", action="store_true",
                        help="Include upstream tests and development docs in a disposable verification package")
    args = parser.parse_args()
    install(args.archive, args.destination, args.python, args.profile_home, args.include_development_files)
