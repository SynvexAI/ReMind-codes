    # config.py
    import os
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent.parent
    UPLOAD_FOLDER = BASE_DIR / "all_uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    DEFAULT_LANGUAGE = 'ru'
    CORS_ORIGINS = "*"

    # API Keys
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "default_gemini_key") #Default Values for tests
    