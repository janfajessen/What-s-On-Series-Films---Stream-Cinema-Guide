# What's On Series & Films

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![HA Version](https://img.shields.io/badge/Home%20Assistant-2026.x-blue)](https://www.home-assistant.io/)

A Home Assistant integration combining three data sources in one:

| Feature | Source | API key? |
|---|---|---|
| Per-show sensors (next episode, status, network, poster) | [TVmaze](https://www.tvmaze.com/api) | No — free |
| Weekly new movies & shows per streaming platform | [TMDB](https://www.themoviedb.org/settings/api) | Yes — free |
| Films currently in cinemas + upcoming cinema releases | TMDB (same key) | Yes — free |

---

## Features

### TVmaze — per tracked show

| Entity | State | Key attributes |
|---|---|---|
| `sensor.<show>_next_episode` | Episode title | season, episode_number, airdate, airtime, days_until_air |
| `sensor.<show>_previous_episode` | Episode title | season, episode_number, airdate |
| `sensor.<show>_status` | Running / Ended / In Development… | premiered, ended, genres, rating |
| `sensor.<show>_network` | Network or streaming channel | network_country, web_channel, schedule_days |
| `camera.<show>_poster` | — | High-resolution poster from TVmaze CDN |

### TMDB Streaming — per configured platform

| Entity | State | Key attributes |
|---|---|---|
| `sensor.new_movies_on_<platform>` | Count of new movies | `movies` list, `logo_url` |
| `sensor.new_shows_on_<platform>` | Count of new titles | `shows` list, `logo_url` |

Each list item: `title`, `release_date`, `vote_average`, `poster_url`, `overview`, `genre_ids`, `tmdb_id`.

The `logo_url` attribute is the official platform logo URL from TMDB, ready to use in Lovelace cards.

### TMDB Cinema

| Entity | State | Key attributes |
|---|---|---|
| `sensor.cinema_now_playing` | Count of films in cinemas | `movies` list, `region_fallback` |
| `sensor.cinema_upcoming` | Count of upcoming films | `movies` list, `region_fallback` |

**What does "cinema" mean?** All films currently showing (or coming soon) in **all cinemas in your selected country**, based on distributor release data submitted to TMDB.

**Small country note (e.g. Andorra AD):** Distributors don't always submit regional data for very small markets. When that happens the integration falls back to global release data and sets `region_fallback: true` on each item so your Lovelace card can display a notice.

---

## Installation

### Via HACS
1. HACS → Integrations → Custom repositories → add `https://github.com/janfajessen/whatson_series_films` as Integration
2. Install and restart Home Assistant

### Manual
Copy `custom_components/whatson_series_films/` into `<config>/custom_components/` and restart.

---

## Configuration

**Settings → Devices & Services → Add Integration → What's On Series & Films**

### Step 1 — TMDB + streaming
- **TMDB API key** (optional): free at [themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)
- **Country code**: ISO 3166-1 alpha-2 (e.g. ES, US, GB, AD)
- **Streaming platforms**: select one or more

### Step 2 — Track TV shows
- Type a show name → results appear as a dropdown → pick the correct one
- Toggle "Add another show" to add more
- Leave empty to skip

> **TV show search only:** there is no manual movie search. Movies appear automatically via the streaming new-releases sensors and the cinema sensors.

### Options (reconfiguration)
Click the gear icon on the integration card to add/remove shows or update TMDB settings.

---

## Platform logos

The `logo_url` attribute on every streaming sensor contains the official TMDB logo URL for that platform. Use it directly in Lovelace cards.

| Platform | TMDB Provider ID |
|---|---|
| Netflix | 8 |
| Amazon Prime Video | 9 |
| Disney+ | 337 |
| Max (HBO) | 384 |
| Apple TV+ | 350 |
| Hulu | 15 |
| Paramount+ | 531 |
| Peacock | 386 |
| Crunchyroll | 283 |
| Mubi | 11 |
| SkyShowtime | 1773 |
| Movistar Plus+ | 149 |

---

## Diagnostics

Settings → Devices & Services → What's On Series & Films → ⋮ → Download diagnostics
Downloads a JSON with coordinator status, entity counts and fallback flags. API key is redacted automatically.

---

## Update intervals

| Source | Interval |
|---|---|
| TVmaze | Every 1 hour |
| TMDB (streaming + cinema) | Every 6 hours |

---

## License

MIT
