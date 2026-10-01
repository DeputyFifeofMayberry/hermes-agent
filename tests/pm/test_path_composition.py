"""Repeated tool activation must preserve PATH resolution in child shells."""

import os
from pathlib import Path
import subprocess

import pytest

from pm.package import compose_env


def test_repeated_composition_preserves_priority_without_path_growth(tmp_path):
    dependent, dependency, ambient = (str(tmp_path / name) for name in ("dependent", "dependency", "ambient"))
    base = {"PATH": os.pathsep.join([dependency, ambient]), "OWNER": "ambient"}
    diffs = [{"PATH": [dependency], "OWNER": "dependency"},
             {"PATH": [dependent], "OWNER": "dependent"}]

    first = compose_env(diffs, base=base)
    assert compose_env(diffs, base=first) == first
    assert first["PATH"].split(os.pathsep) == [dependent, dependency, ambient]
    assert first["OWNER"] == "dependent"
    assert base["PATH"] == os.pathsep.join([dependency, ambient])


@pytest.mark.platforms("windows")
def test_repeated_path_entries_do_not_hide_tools_from_windows_shell(tmp_path):
    (tmp_path / "hermes-path-probe.cmd").write_text("@echo MANAGED_PATH_OK\n", encoding="utf-8")
    directory = str(tmp_path)
    repeated = os.pathsep.join([directory] * (9000 // len(directory) + 1))
    env = compose_env([{"PATH": [directory]}], base=dict(os.environ, PATH=repeated))

    result = subprocess.run(
        [str(Path(os.environ["SystemRoot"]) / "System32/cmd.exe"),
         "/d", "/s", "/c", "hermes-path-probe.cmd"],
        env=env, capture_output=True, text=True, check=True,
    )
    assert "MANAGED_PATH_OK" in result.stdout
