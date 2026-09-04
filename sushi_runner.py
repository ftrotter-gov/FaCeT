#!/usr/bin/env python3
"""Locate (or install) SUSHI and use it to compile generated FSH.

`SUSHI <https://fshschool.org/docs/sushi/>`_ is the reference FHIR Shorthand
compiler.  It is distributed on npm as ``fsh-sushi``.  This module is a thin
helper used by ``test_facet_to_fsh_sushi.py`` to:

1. find a ``sushi`` executable (or install one with ``npm install -g fsh-sushi``),
2. assemble a throwaway minimal FSH project around the generated ``.fsh`` files, and
3. run SUSHI over it and report the errors and warnings it found.

SUSHI needs the FHIR R4 core package.  The first run downloads it into
``~/.fhir/packages`` and can take a few minutes; later runs are ~10 seconds.

Usage::

    python sushi_runner.py --out-dir /tmp/facet-fsh   # compile and report
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# The npm package that provides the ``sushi`` executable.
NPM_PACKAGE = "fsh-sushi"

# SUSHI needs a sushi-config.yaml. ``FSHOnly`` skips IG scaffolding, which is
# all we need to prove the FSH itself compiles. Keep this minimal: any unused
# IG-only property (id, name, ...) makes SUSHI emit a warning.
MINIMAL_SUSHI_CONFIG = """canonical: http://example.org/facet-compile-check
status: draft
version: 0.1.0
fhirVersion: 4.0.1
FSHOnly: true
"""

# Matches the SUSHI results banner, e.g. "0 Errors       1 Warning".
RESULT_RE = re.compile(r"(\d+)\s+Errors?\s+(\d+)\s+Warnings?", re.IGNORECASE)

# First run downloads FHIR packages, so allow a generous timeout.
DEFAULT_TIMEOUT = 900

# The FaCeT files this project generates. Only these are compiled: the NDH IG's
# other FSH files depend on packages (us-core and friends) that are unrelated to
# FaCeT, and pulling them in would report failures this repo cannot act on.
FACET_FSH_NAMES = ("facet_credentials.fsh", "facet_org_credential.fsh")


class SushiNotAvailable(RuntimeError):
    """Raised when SUSHI is not installed and could not be installed."""


def find_sushi() -> str | None:
    """Return the path to the ``sushi`` executable, or None if not found."""
    return shutil.which("sushi")


def install_sushi() -> str | None:
    """Attempt to install SUSHI globally with npm; return its path or None."""
    npm = shutil.which("npm")
    if npm is None:
        return None
    try:
        subprocess.run(
            [npm, "install", "-g", NPM_PACKAGE],
            check=True,
            capture_output=True,
            text=True,
            timeout=DEFAULT_TIMEOUT,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
    return find_sushi()


def ensure_sushi(auto_install: bool = True) -> str:
    """Return a usable ``sushi`` path, installing it if necessary."""
    sushi = find_sushi()
    if sushi:
        return sushi
    if auto_install:
        sushi = install_sushi()
        if sushi:
            return sushi
    raise SushiNotAvailable(
        f"sushi not found and could not be installed. Install it with: npm install -g {NPM_PACKAGE}"
    )



class SushiResult:
    """The outcome of a SUSHI run."""

    def __init__(self, returncode: int, output: str, project_dir: str) -> None:
        self.returncode = returncode
        self.output = output
        self.project_dir = project_dir

    @property
    def errors(self) -> int:
        """Number of errors reported in the SUSHI results banner."""
        match = RESULT_RE.search(self.output)
        return int(match.group(1)) if match else (0 if self.returncode == 0 else -1)

    @property
    def warnings(self) -> int:
        """Number of warnings reported in the SUSHI results banner."""
        match = RESULT_RE.search(self.output)
        return int(match.group(2)) if match else -1

    @property
    def ok(self) -> bool:
        """True when SUSHI compiled the FSH without errors."""
        return self.returncode == 0 and self.errors == 0

    def error_lines(self) -> list[str]:
        """Return the ``error`` lines SUSHI printed, for test failure messages."""
        return [
            line for line in self.output.splitlines() if line.lower().startswith("error")
        ]

    def resource_dir(self) -> str:
        """Directory holding the JSON resources SUSHI exported."""
        return os.path.join(self.project_dir, "fsh-generated", "resources")

    def exported_resources(self) -> list[str]:
        """Names of the JSON files SUSHI produced."""
        directory = self.resource_dir()
        if not os.path.isdir(directory):
            return []
        return sorted(n for n in os.listdir(directory) if n.endswith(".json"))

    def summary(self) -> str:
        """A short human-readable summary, used in assertion messages."""
        lines = [
            f"sushi exit={self.returncode} errors={self.errors} warnings={self.warnings}"
        ]
        lines.extend(self.error_lines()[:20])
        return "\n".join(lines)


def run_sushi(
    fsh_files: list[str],
    project_dir: str,
    sushi: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> SushiResult:
    """Compile ``fsh_files`` with SUSHI inside a minimal project at ``project_dir``.

    The files are copied into ``{project_dir}/input/fsh`` alongside a minimal
    ``sushi-config.yaml`` so the FSH is validated on its own, independent of any
    particular implementation guide.
    """
    sushi = sushi or ensure_sushi()

    fsh_dir = os.path.join(project_dir, "input", "fsh")
    os.makedirs(fsh_dir, exist_ok=True)
    for path in fsh_files:
        shutil.copy(path, os.path.join(fsh_dir, os.path.basename(path)))

    config_path = os.path.join(project_dir, "sushi-config.yaml")
    with open(config_path, "w", encoding="utf-8") as handle:
        handle.write(MINIMAL_SUSHI_CONFIG)

    completed = subprocess.run(
        [sushi, "."],
        cwd=project_dir,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    output = completed.stdout + completed.stderr
    return SushiResult(completed.returncode, output, project_dir)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compile FaCeT FSH files with SUSHI to verify they are valid.",
    )
    parser.add_argument(
        "--out-dir",
        required=True,
        help="Directory containing the generated .fsh files to compile.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="Seconds to allow SUSHI to run (default: %(default)s).",
    )
    parser.add_argument(
        "--no-install",
        action="store_true",
        help="Fail instead of trying to install SUSHI when it is missing.",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help=(
            "FSH file names inside --out-dir to compile "
            f"(default: {' '.join(FACET_FSH_NAMES)})."
        ),
    )
    args = parser.parse_args(argv)

    try:
        sushi = ensure_sushi(auto_install=not args.no_install)
    except SushiNotAvailable as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"using sushi: {sushi}")

    names = args.files or list(FACET_FSH_NAMES)
    fsh_files = [os.path.join(args.out_dir, name) for name in names]
    missing = [path for path in fsh_files if not os.path.exists(path)]
    if missing:
        for path in missing:
            print(f"error: no such FSH file: {path}", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory() as tmp:
        result = run_sushi(fsh_files, tmp, sushi=sushi, timeout=args.timeout)
        print(result.summary())
        for name in result.exported_resources():
            print(f"  exported {name}")

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
