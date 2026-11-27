"""Spuštění: python main.py — prostředí .venv se připraví automaticky."""

import os
from pathlib import Path
import subprocess
import sys
import venv


def main():
    script = Path(__file__).resolve()
    venv_dir = script.parent / ".venv"
    bin_dir = venv_dir / ("Scripts" if os.name == "nt" else "bin")
    python = bin_dir / ("python.exe" if os.name == "nt" else "python")

    if Path(sys.prefix).resolve() != venv_dir.resolve():
        if not python.exists():
            venv.EnvBuilder(with_pip=True).create(venv_dir)

        env = os.environ.copy()
        env["VIRTUAL_ENV"] = str(venv_dir)
        env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")
        env.pop("PYTHONHOME", None)
        raise SystemExit(subprocess.call(
            [str(python), str(script), *sys.argv[1:]], env=env
        ))

    # Sem patří vlastní kód a importy balíčků nainstalovaných ve .venv.
    print(f"Skript běží ve venv: {sys.prefix}")


if __name__ == "__main__":
    main()
