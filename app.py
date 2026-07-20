from __future__ import annotations

import csv
import io
import ipaddress
import json
import os
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel, Field, field_validator

APP_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("APP_DB", APP_DIR / "infoblox_av.db"))
TARGET_DOMAIN = os.getenv("TARGET_DOMAIN", "itsav.calpoly.edu").strip(".")
DEFAULT_NETWORK = os.getenv("DEFAULT_NETWORK", "10.40.64.0/18")
SOURCE_DOMAINS = tuple(d.strip().lower() for d