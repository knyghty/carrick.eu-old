"""gunicorn configuration."""

import multiprocessing
import os


bind = f"0.0.0.0:{os.getenv('PORT', '443')}"
workers = multiprocessing.cpu_count() * 2 + 1
