"""Constants for the What's On Series & Films integration."""
from __future__ import annotations

from datetime import timedelta

DOMAIN = "whatson_series_films"
NAME   = "What's On Series & Films"

# ── Config entry keys ────────────────────────────────────────────────────────
CONF_TMDB_API_KEY  = "tmdb_api_key"
CONF_COUNTRY       = "country"
CONF_LANGUAGE      = "language"
CONF_PLATFORMS     = "platforms"    # list[str] — provider names
CONF_PROVIDER_MAP  = "provider_map" # dict[str, int] — name → TMDB provider ID
CONF_SHOWS         = "shows"        # list[{"id": int, "name": str}]

# ── API base URLs ────────────────────────────────────────────────────────────
TVMAZE_BASE_URL     = "https://api.tvmaze.com"
TMDB_BASE_URL       = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
TMDB_IMAGE_ORIG_URL = "https://image.tmdb.org/t/p/original"

# ── Update intervals ─────────────────────────────────────────────────────────
SCAN_INTERVAL_TVMAZE = timedelta(hours=1)
SCAN_INTERVAL_TMDB   = timedelta(hours=6)

# ── Results limits ───────────────────────────────────────────────────────────
TMDB_MAX_RESULTS          = 50
TMDB_MAX_CINEMA_RESULTS   = 50
TVMAZE_MAX_SEARCH_RESULTS = 15

# ── Lookback window for "new on platform" queries ────────────────────────────
TMDB_LOOKBACK_DAYS = 21

# ── Country → TMDB language code ─────────────────────────────────────────────
# Used to localise titles and overviews in TMDB responses.
# TMDB format: "{iso_639_1}-{iso_3166_1}"
COUNTRY_TO_LANGUAGE: dict[str, str] = {
    # Americas
    "US": "en-US", "CA": "en-CA", "MX": "es-MX",
    "AR": "es-AR", "CO": "es-CO", "CL": "es-CL", "PE": "es-PE",
    "VE": "es-VE", "EC": "es-EC", "UY": "es-UY", "PY": "es-PY",
    "BR": "pt-BR",
    # Europe — West
    "GB": "en-GB", "IE": "en-IE",
    "ES": "es-ES", "FR": "fr-FR", "DE": "de-DE", "AT": "de-AT",
    "CH": "de-CH", "IT": "it-IT", "PT": "pt-PT",
    "NL": "nl-NL", "BE": "nl-BE", "LU": "fr-LU",
    # Europe — North
    "SE": "sv-SE", "NO": "nb-NO", "DK": "da-DK", "FI": "fi-FI",
    "IS": "is-IS",
    # Europe — East & Balkans
    "PL": "pl-PL", "CZ": "cs-CZ", "SK": "sk-SK",
    "HU": "hu-HU", "RO": "ro-RO", "BG": "bg-BG",
    "HR": "hr-HR", "SI": "sl-SI", "RS": "sr-RS",
    "BA": "bs-BA", "MK": "mk-MK", "AL": "sq-AL",
    "GR": "el-GR", "CY": "el-CY",
    # Baltics
    "EE": "et-EE", "LV": "lv-LV", "LT": "lt-LT",
    # Former Soviet
    "RU": "ru-RU", "UA": "uk-UA", "BY": "be-BY",
    "KZ": "ru-KZ", "GE": "ka-GE", "AM": "hy-AM", "AZ": "az-AZ",
    # Middle East & Africa
    "TR": "tr-TR", "IL": "he-IL", "SA": "ar-SA", "AE": "ar-AE",
    "EG": "ar-EG", "MA": "ar-MA", "ZA": "en-ZA", "NG": "en-NG",
    "KE": "en-KE",
    # Asia — East
    "JP": "ja-JP", "KR": "ko-KR", "CN": "zh-CN", "TW": "zh-TW",
    "HK": "zh-HK",
    # Asia — South & Southeast
    "IN": "hi-IN", "PK": "ur-PK", "BD": "bn-BD",
    "TH": "th-TH", "VN": "vi-VN", "ID": "id-ID", "MY": "ms-MY",
    "PH": "tl-PH", "SG": "en-SG",
    # Oceania
    "AU": "en-AU", "NZ": "en-NZ",
    # Small / special
    "AD": "ca-AD",  # Andorra — Catalan; TMDB may fall back to es-ES
}
DEFAULT_LANGUAGE = "en-US"

# ── Fallback provider IDs ─────────────────────────────────────────────────────
# Used ONLY if the live TMDB provider fetch fails during setup.
# The config flow always tries to fetch providers dynamically first.
STREAMING_PLATFORMS_FALLBACK: dict[str, int] = {
    "Netflix": 8, "Amazon Prime Video": 9, "Disney+": 337,
    "Max (HBO)": 384, "Apple TV+": 350, "Paramount+": 531,
    "Hulu": 15, "Peacock": 386, "Crunchyroll": 283, "Mubi": 11,
}
