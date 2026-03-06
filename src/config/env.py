import environ
import os
from pathlib import Path


env = environ.Env()
ROOT_DIR = Path(__file__).resolve().parents[2]
BASE_DIR = Path(__file__).resolve().parents[1]

ENV_FILE = ROOT_DIR / '.env'

if ENV_FILE.exists():
    environ.Env.read_env(ENV_FILE)
