"""gunicorn configuration."""

import os


bind = f"0.0.0.0:{os.getenv('PORT', '443')}"
