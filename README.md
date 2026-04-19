<div align="center">

# What's On Series & Films 
## Stream and Cinema Guide <br> Home Assistant Integration

..........   <img src="brands/logo@2x.png" width="550"/>

![Version](https://img.shields.io/badge/version-1.5.24-blue?style=for-the-badge)
![HA](https://img.shields.io/badge/Home%20Assistant-2024.1+-orange?style=for-the-badge&logo=home-assistant)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python)
![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5?style=for-the-badge&logo=homeassistantcommunitystore&logoColor=white)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Donate-yellow?style=for-the-badge&logo=buymeacoffee)](https://www.buymeacoffee.com/janfajessen)
[![Patreon](https://img.shields.io/badge/Patreon-Support-red?style=for-the-badge&logo=patreon)](https://www.patreon.com/janfajessen)
<!--[![Ko-Fi](https://img.shields.io/badge/Ko--Fi-Support-teal?style=for-the-badge&logo=ko-fi)](https://ko-fi.com/janfajessen)
[![GitHub Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-Support-pink?style=for-the-badge&logo=githubsponsors)](https://github.com/sponsors/janfajessen)


[![PayPal](https://img.shields.io/badge/PayPal-Donate-blue?style=for-the-badge&logo=paypal)](https://paypal.me/janfajessen)-->


<sub>
Qué hacen en streaming y en el cine - ما الذي يعرض في البث المباشر والسينما - Nə var streaming və kinoda - Što rade na streaming-u i u kinu - Какво правят в стрийминг и кино - Što rade na streaming-u i u kinu - Què fan en streaming i al cinema - Co dělají na streamování a v kině - Hvad laver de på streaming og i biografen - Was machen sie beim Streaming und im Kino - Τι κάνουν στο streaming και στον κινηματογράφο - Qué hacen en streaming y en el cine - Quoi qu'ils font en streaming et au cinéma - Que fan en streaming e no cine - מה הם עושים בסטרימינג ובקולנוע - स्ट्रीमिंग और सिनेमा में क्या करते हैं - Mit csinálnak a streamingben és a moziban - Zer egiten dute streaming-ean eta zinean - در استریم و سینما چه کار می‌کنند - Mitä he tekevät suoratoistossa ja elokuvissa - Apa yang mereka lakukan di streaming dan bioskop - Cosa fanno in streaming e al cinema - Что делают в стриминге и кино - Co robią w streamingu i kinie - O que eles fazem no streaming e no cinema - Ce fac în streaming și la cinema - Що роблять у стрімінгу та кіно - Vad gör de på streaming och bio - Dizilerde ve filmlerde ne yapıyorlar - 流媒体和电影院在放什么
</sub>

</div>

## 🍿 Never miss a premiere, a new season, or a cinema release

> **Highly recommended companion:**
> 📺 [What's On TV — EPG TV Guide](https://github.com/janfajessen/What-s-On-TV---EPG-TV-Guide) — live TV guide for Home Assistant. Use both together for complete entertainment coverage: live TV + streaming + cinema.

---

## 💡 Ideas — what to search and discover

### 📺 Track your favourite series (TVmaze)

* **Can't keep up with release dates?** Add `"The Bear"`, `"Severance"`, `"Andor"` or `"Silo"` — the *Next Episode* sensor tells you exactly how many days until the next episode airs
* **Following a long-running show?** Track `"Grey's Anatomy"`, `"NCIS"` or `"Neighbours"` — the *Status* sensor tells you if it's still running or has been cancelled
* **Into anime?** Add `"Attack on Titan"`, `"Jujutsu Kaisen"` or `"One Piece"` — get notified the moment a new episode is confirmed on Crunchyroll
* **Documentary fan?** Search `"Planet Earth"`, `"Our Planet"` or `"100 Foot Wave"` — TVmaze covers docs too, and the previous/next episode sensors work identically
* **Watching a show from another country?** Add `"Dark"` (Germany), `"Money Heist"` (Spain), `"Squid Game"` (Korea) — TVmaze is global, no region restriction
* **Not sure if a show is coming back?** The *Status* sensor returns `Running`, `Ended`, `To Be Determined` or `In Development` — no more Googling "is X cancelled?"
* **Want a bedtime reminder?** If your favourite show airs at 22:00 and you tend to forget, use the *airtime* attribute in an automation to push a reminder 15 minutes before

### 🎬 Discover new content on streaming (TMDB)

* **New to Netflix this week?** The `new_movies_on_netflix` and `new_series_docs_on_netflix` sensors update every 6 hours with fresh titles including ratings and overviews
* **HBO/Max watcher?** Set up `[ES] New Series & Docs on Max` and get a weekly Telegram summary of everything that dropped
* **Subscribe to multiple platforms?** Configure ES, PL, HR or any country separately — each entry tracks its own regional catalogue
* **Kids content?** Add Disney+ and filter by genre_id `16` (Animation) or `10762` (Kids) in your automations
* **Cinephile on a budget?** Add MUBI — it rotates a curated selection of art-house films weekly, and the sensor tells you exactly what arrived
* **Don't want to miss a specific actor?** Use the `overview` attribute in a template sensor to search for a name across all new releases

### 🏟️ Cinema — what's playing near you (TMDB)

* **Weekend plans?** The `cinema_now_playing` sensor shows all films currently in cinemas in your country, not specificaly in your region,  with ratings and overviews
* **Planning ahead?** `cinema_upcoming` shows confirmed releases for the coming weeks — useful for buying tickets early
* **Living in a small country like Andorra?** The integration automatically falls back to global release data when regional data isn't available, and marks items with `region_fallback: true` so your card can display a note
* **Automate your Friday routine:** trigger an automation every Friday evening that sends you a formatted list of new cinema releases via Telegram — your personal weekly film bulletin

> **Tip — combine with What's On TV:** if a film is premiering on a streaming platform and you also track the same channel in What's On TV, you can cross-reference the two integrations in a template to surface "airing tonight AND newly on Netflix" content.

---

## 🔑 How to get a free TMDB API key

The TMDB API key is **free** and takes about 2 minutes to get:

1. Go to <a href="https://www.themoviedb.org/" target="_blank">themoviedb.org</a> 
2. Fill in username, email and password → verify your email
3. Log in and go to **Settings** (click your avatar, top right) → **API**
4. Click **Create** → choose **Developer** (personal use)
5. Fill in the form:
   - *Type of use:* **Personal**
   - *Application name:* anything (e.g. `Home Assistant`)
   - *Application URL:* `http://localhost` (personal use, any URL works)
   - *Application summary:* `Personal Home Assistant integration`
6. Accept the terms → click **Submit**
7. Your **API Key (v3 auth)** appears immediately on the API page — copy it

> The key looks like: `a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4`
> Paste it into the integration config flow when prompted.

---

## Features

* **TVmaze** — track unlimited TV series and documentaries worldwide (no API key needed)
  * Next episode: title, season, number, airdate, airtime, days until air
  * Previous episode: title, season, number, airdate
  * Series status: Running / Ended / To Be Determined / In Development
  * Network or streaming channel with schedule
  * Show poster as a `camera` entity (fetched live from TVmaze CDN)
* **TMDB Streaming** — weekly new movies and series/docs per platform per country
  * Platform logo URL included in every sensor (`logo_url` attribute)
  * Configurable per country — add ES, PL, HR as separate entries
  * Platforms fetched **live from TMDB** for your country — always up to date
* **TMDB Cinema** — films currently in cinemas and upcoming releases
  * Regional data when available; automatic global fallback for small markets
  * `region_fallback` flag for Lovelace cards to display a disclaimer
* **Multi-country** — add as many entries as you need, one per country
* **Language-aware** — titles and overviews returned in the configured language (pl-PL, hr-HR, es-ES…)
* **Diagnostics** — download a full JSON report from the HA UI (API key redacted)

---

## Installation

### Via HACS (recommended)

1. Open HACS → **Integrations** → ⋮ → **Custom repositories**
2. Add `https://github.com/janfajessen/whatson_series_films` — category **Integration**
3. Search for **What's On Series & Films** and install
4. Restart Home Assistant
<img src="brands/icon@2x.png" width="100"/>


### Manual

Copy the `custom_components/whatson_series_films/` folder to your `config/custom_components/` directory and restart.

---

## Configuration

Go to **Settings → Devices & Services → Add Integration → What's On Series & Films**.

**Step 1 — TMDB:** enter your free [TMDB API key](https://www.themoviedb.org/settings/api), your country code (e.g. `ES`, `PL`, `HR`, `AD`) and optionally a language override (auto-detected from country if left blank).

**Step 2 — Platforms:** the integration fetches all streaming platforms available in your country live from TMDB and shows them as a list. Select the ones you subscribe to.

**Step 3 — Series & Docs:** type a name to search TVmaze. Pick from the results. Toggle "Add another" to keep adding. Leave blank to skip.

You can add **multiple entries** for different countries simultaneously.

---

## Entities

### TVmaze — per tracked show (no country prefix, global)

| Entity | State | Key attributes |
|---|---|---|
| `sensor.whatson_series_films_<show>_next_episode` | Episode title | `season`, `episode_number`, `airdate`, `airtime`, `days_until_air`, `summary` |
| `sensor.whatson_series_films_<show>_previous_episode` | Episode title | `season`, `episode_number`, `airdate`, `summary` |
| `sensor.whatson_series_films_<show>_status` | Running / Ended / … | `premiered`, `ended`, `genres`, `rating`, `language` |
| `sensor.whatson_series_films_<show>_network` | Network name | `web_channel`, `schedule_days`, `schedule_time` |
| `camera.whatson_series_films_<show>_poster` | — | Live poster image from TVmaze CDN |

### TMDB Streaming — per platform per country

| Entity | State | Key attributes |
|---|---|---|
| `sensor.whatson_series_films_<cc>_new_movies_on_<platform>` | Count | `movies` list, `logo_url` |
| `sensor.whatson_series_films_<cc>_new_series_docs_on_<platform>` | Count | `shows` list, `logo_url` |

### TMDB Cinema — per country

| Entity | State | Key attributes |
|---|---|---|
| `sensor.whatson_series_films_<cc>_cinema_now_playing` | Count | `movies` list, `region_fallback` |
| `sensor.whatson_series_films_<cc>_cinema_upcoming` | Count | `movies` list, `region_fallback` |

Each item in any `movies` / `shows` list contains:
`title` · `release_date` · `vote_average` · `poster_url` · `overview` · `genre_ids` · `tmdb_id`

**Examples** (`<cc>` = country code, `<platform>` = slugified platform name):
```
sensor.whatson_series_films_breaking_bad_next_episode
sensor.whatson_series_films_es_new_movies_on_netflix
sensor.whatson_series_films_es_cinema_now_playing
sensor.whatson_series_films_pl_new_movies_on_player_pl
sensor.whatson_series_films_pl_cinema_upcoming
sensor.whatson_series_films_hr_new_series_docs_on_hbo_max
camera.whatson_series_films_the_bear_poster
```

---

## Automations & Scripts

### 🔔 Weekly streaming digest — every Friday via Telegram

```yaml
alias: "WS&F — Weekly streaming digest"
trigger:
  - platform: time
    at: "19:00:00"
    variables:
      weekday: "{{ now().weekday() }}"
condition:
  - condition: template
    value_template: "{{ now().weekday() == 4 }}"  # Friday
action:
  - action: notify.telegram_jan
    data:
      message: >
        🎬 *New this week on Netflix ES*
        {% set movies = state_attr('sensor.whatson_series_films_es_new_movies_on_netflix', 'movies') %}
        {% if movies %}
          {% for m in movies[:5] %}
          • {{ m.title }} ({{ m.release_date[:4] }}) ⭐ {{ m.vote_average }}
          {% endfor %}
        {% else %}
          No new movies found.
        {% endif %}

        📺 *New series & docs*
        {% set shows = state_attr('sensor.whatson_series_films_es_new_series_docs_on_netflix', 'shows') %}
        {% if shows %}
          {% for s in shows[:5] %}
          • {{ s.title }} ⭐ {{ s.vote_average }}
          {% endfor %}
        {% else %}
          No new titles found.
        {% endif %}
```

### 🎭 Next episode reminder — day before airdate

```yaml
alias: "WS&F — Remind me the day before The Bear airs"
trigger:
  - platform: template
    value_template: >
      {{ state_attr('sensor.whatson_series_films_the_bear_next_episode', 'days_until_air') == 1 }}
action:
  - action: notify.telegram_jan
    data:
      message: >
        📺 Tomorrow: *The Bear*
        S{{ state_attr('sensor.whatson_series_films_the_bear_next_episode', 'season') }}
        E{{ state_attr('sensor.whatson_series_films_the_bear_next_episode', 'episode_number') }}
        — {{ states('sensor.whatson_series_films_the_bear_next_episode') }}
        🕐 {{ state_attr('sensor.whatson_series_films_the_bear_next_episode', 'airtime') }}
        📡 {{ states('sensor.whatson_series_films_the_bear_network') }}
```

### 🏟️ Friday cinema bulletin — what's in cinemas this weekend

```yaml
alias: "WS&F — Weekend cinema bulletin"
trigger:
  - platform: time
    at: "10:00:00"
condition:
  - condition: template
    value_template: "{{ now().weekday() == 4 }}"  # Friday
action:
  - action: notify.telegram_jan
    data:
      message: >
        🍿 *In cinemas this weekend*
        {% set films = state_attr('sensor.whatson_series_films_es_cinema_now_playing', 'movies') %}
        {% if films %}
          {% for f in films | sort(attribute='vote_average', reverse=True) | list[:8] %}
          {{ loop.index }}. {{ f.title }} ⭐ {{ f.vote_average }}
          {% endfor %}
        {% else %}
          No regional data available.
        {% endif %}

        🎬 *Coming soon*
        {% set upcoming = state_attr('sensor.whatson_series_films_es_cinema_upcoming', 'movies') %}
        {% if upcoming %}
          {% for f in upcoming[:5] %}
          • {{ f.title }} — {{ f.release_date }}
          {% endfor %}
        {% else %}
          No upcoming data.
        {% endif %}
```

### 📢 New season alert — when a show goes from "Ended" back to "Running"

```yaml
alias: "WS&F — Alert when show status changes to Running"
trigger:
  - platform: state
    entity_id: sensor.whatson_series_films_house_of_the_dragon_status
    to: "Running"
action:
  - action: notify.telegram_jan
    data:
      message: >
        🎉 *{{ state_attr('sensor.whatson_series_films_house_of_the_dragon_status', 'tvmaze_url') | regex_findall('shows/\d+/([^/]+)') | first | replace('-', ' ') | title }}*
        is back! Status changed to Running.
        Next episode: {{ states('sensor.whatson_series_films_house_of_the_dragon_next_episode') }}
```

### 🔍 Script — search new releases by minimum rating

```yaml
alias: "WS&F — Top rated new on streaming this week"
sequence:
  - action: notify.telegram_jan
    data:
      message: >
        ⭐ *New this week with rating ≥ 7.5*
        {% set platforms = [
          'sensor.whatson_series_films_es_new_movies_on_netflix',
          'sensor.whatson_series_films_es_new_movies_on_disney',
          'sensor.whatson_series_films_es_new_movies_on_max_hbo'
        ] %}
        {% set min_rating = 7.5 %}
        {% set results = namespace(items=[]) %}
        {% for p in platforms %}
          {% set movies = state_attr(p, 'movies') %}
          {% if movies %}
            {% for m in movies %}
              {% if m.vote_average >= min_rating %}
                {% set results.items = results.items + [m.title ~ ' ⭐' ~ m.vote_average] %}
              {% endif %}
            {% endfor %}
          {% endif %}
        {% endfor %}
        {% if results.items %}
          {% for item in results.items | unique | sort %}
          • {{ item }}
          {% endfor %}
        {% else %}
          Nothing above {{ min_rating }} this week.
        {% endif %}
```

### 📺 LED matrix — show next episode countdown

```yaml
alias: "WS&F — Update LED matrix with next episode countdown"
trigger:
  - platform: state
    entity_id: sensor.whatson_series_films_the_bear_next_episode
action:
  - variables:
      days: "{{ state_attr('sensor.whatson_series_films_the_bear_next_episode', 'days_until_air') }}"
      episode: "{{ states('sensor.whatson_series_films_the_bear_next_episode') }}"
  - action: rest_command.wled_text
    data:
      text: >
        {% if days == 0 %}TODAY: {{ episode }}
        {% elif days == 1 %}TOMORROW: {{ episode }}
        {% else %}{{ days }}d: {{ episode }}
        {% endif %}
```

---

## Reconfiguration (Options ⚙)

Click the gear icon on the integration card at any time to:
- **Add** a new series or documentary (TVmaze search)
- **Remove** an existing series
- **Change streaming platforms** (re-fetches live list from TMDB)
- **Update** TMDB key, country or language

The integration reloads automatically after every change.

---

## Diagnostics

**Settings → Devices & Services → What's On Series & Films → ⋮ → Download diagnostics**

Downloads a JSON with coordinator status, entity counts, cinema fallback flags and logo fetch results. TMDB API key is automatically redacted.

---

## Platform logos

All streaming sensor attributes include a `logo_url` with the official platform logo from TMDB CDN (`https://image.tmdb.org/t/p/original/...`). Use directly in Lovelace cards.

---

## Update intervals

| Source | Interval |
|---|---|
| TVmaze (show data) | Every 1 hour |
| TMDB (streaming + cinema + logos) | Every 24 hours |

TMDB streaming queries cover the last 14 days so content added mid-week is never missed between restarts.

---

## Supported languages (auto-detected from country)

The integration automatically maps your country code to the correct TMDB language — titles and overviews will be returned in the local language. You can override this in step 1 of the config flow.

| Region | Example countries | Language |
|---|---|---|
| Spain / LATAM | ES, MX, AR, CO, CL | es-ES / es-MX / … |
| Poland | PL | pl-PL |
| Croatia | HR | hr-HR |
| Russia | RU | ru-RU |
| Andorra | AD | ca-AD (Catalan) |
| France | FR | fr-FR |
| Germany | DE | de-DE |
| Italy | IT | it-IT |
| Japan | JP | ja-JP |
| Korea | KR | ko-KR |
| … | 49 countries mapped | … |

---

## Requirements

* Home Assistant 2026.x
* Python 3.12+
* Free TMDB API key: [themoviedb.org/settings/api](https://www.themoviedb.org/settings/api) (optional — TVmaze features work without it)

---

## Companion integration

| Integration | What it adds |
|---|---|
| 📺 [What's On TV — EPG TV Guide](https://github.com/janfajessen/What-s-On-TV---EPG-TV-Guide) | Live TV guide — current and upcoming programmes on broadcast channels. Combine with this integration for complete entertainment coverage. |

---

<div align="center">
<sub>
Qué hacen en streaming y en el cine - ما الذي يعرض في البث المباشر والسينما - Nə var streaming və kinoda - Što rade na streaming-u i u kinu - Какво правят в стрийминг и кино - Što rade na streaming-u i u kinu - Què fan en streaming i al cinema - Co dělají na streamování a v kině - Hvad laver de på streaming og i biografen - Was machen sie beim Streaming und im Kino - Τι κάνουν στο streaming και στον κινηματογράφο - Qué hacen en streaming y en el cine - Quoi qu'ils font en streaming et au cinéma - Que fan en streaming e no cine - מה הם עושים בסטרימינג ובקולנוע - स्ट्रीमिंग और सिनेमा में क्या करते हैं - Mit csinálnak a streamingben és a moziban - Zer egiten dute streaming-ean eta zinean - در استریم و سینما چه کار می‌کنند - Mitä he tekevät suoratoistossa ja elokuvissa - Apa yang mereka lakukan di streaming dan bioskop - Cosa fanno in streaming e al cinema - Что делают в стриминге и кино - Co robią w streamingu i kinie - O que eles fazem no streaming e no cinema - Ce fac în streaming și la cinema - Що роблять у стрімінгу та кіно - Vad gör de på streaming och bio - Dizilerde ve filmlerde ne yapıyorlar - 流媒体和电影院在放什么
</sub>

---

<img src="brands/icon@2x.png" width="100"/>
</div>

## 🚀 Usage

### Minimal (auto-discover everything)
```yaml
type: custom:whatson-series-films-card
```

### With options
```yaml
type: custom:whatson-series-films-card
title: "What's On"
theme: dark        # dark | light
accent: "#e8872a"  # any hex color
```

### Specific sensors only
```yaml
type: custom:whatson-series-films-card
entities:
  - sensor.whatson_series_films_es_cinema_now_playing
  - sensor.whatson_series_films_es_new_movies_on_netflix_standard_with_ads
  - sensor.whatson_series_films_lupin_status
```

---

## ⚙️ Configuration options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `title` | string | *(auto from HA language)* | Card title |
| `theme` | `dark`\|`light` | `dark` | Color theme |
| `accent` | string | `#e8872a` | Accent color (HEX or `R,G,B`) |
| `entities` | list | *(auto-discover)* | Specific sensors to display |

---

## 🔧 Automations & Scripts

### Notify when a new movie appears in theaters
```yaml
alias: "What's On — New cinema release"
trigger:
  - platform: template
    value_template: >
      {{ state_attr('sensor.whatson_series_films_es_cinema_now_playing', 'movies')
         | selectattr('release_date', 'ge', now().strftime('%Y-%m-%d'))
         | list | count > 0 }}
action:
  - service: notify.telegram_jan
    data:
      message: >
        🎬 New in theaters today:
        {% for m in state_attr('sensor.whatson_series_films_es_cinema_now_playing', 'movies')
           if m.release_date == now().strftime('%Y-%m-%d') %}
        • {{ m.title }} {% if m.vote_average > 0 %}(⭐{{ m.vote_average }}){% endif %}
        {% endfor %}
```

### Notify when a followed series has a new episode
```yaml
alias: "What's On — New episode available"
trigger:
  - platform: state
    entity_id: sensor.whatson_series_films_lupin_next_episode
    from: "No upcoming episode"
action:
  - service: notify.telegram_jan
    data:
      message: >
        📺 New episode of **Lupin**!
        {{ states('sensor.whatson_series_films_lupin_next_episode') }}
```

### Send weekly streaming highlights to Telegram with poster
```yaml
alias: "What's On — Weekly highlights"
trigger:
  - platform: time
    at: "09:00:00"
  - platform: template
    value_template: "{{ now().weekday() == 4 }}"  # Friday
action:
  - variables:
      movies: "{{ state_attr('sensor.whatson_series_films_es_new_movies_on_netflix_standard_with_ads', 'movies') }}"
  - service: telegram_bot.send_message
    data:
      target:
        - "{{ states('input_text.telegram_chat_jan') }}"
      message: >
        🎬 *New on Netflix this week:*
        {% for m in movies[:5] %}
        • {{ m.title }}{% if m.vote_average > 0 %} ⭐{{ m.vote_average }}{% endif %}
        {% endfor %}
```

### Display now-playing count as a sensor badge
```yaml
template:
  - sensor:
      - name: "Cinema now playing count"
        state: >
          {{ state_attr('sensor.whatson_series_films_es_cinema_now_playing', 'movies') | count }}
        icon: mdi:ticket-confirmation-outline
```

---

<div align="center">
  <img src="brands/logo@2x.png" width="150"/>
</div>

## 🗺️ Available countries


### 🎬 Cinema (TMDB Now Playing / Upcoming)



<table border="0" cellspacing="0" cellpadding="6" width="100%">
<tr>
<td width="20%" align="left"><sub>🇪🇸 España / Espanya / Espainia</sub></td>
<td width="20%" align="left"><sub>🇦🇩 Andorra</sub></td>
<td width="20%" align="left"><sub>🇦🇱 Shqipëria *</sub></td>
<td width="20%" align="left"><sub>🇦🇷 Argentina</sub></td>
<td width="20%" align="left"><sub>🇦🇲 Հայաստան *</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇦🇺 Australia</sub></td>
<td width="20%" align="left"><sub>🇦🇹 Österreich</sub></td>
<td width="20%" align="left"><sub>🇦🇼 Aruba *</sub></td>
<td width="20%" align="left"><sub>🇸🇦 المملكة العربية السعودية</sub></td>
<td width="20%" align="left"><sub>🇧🇾 Беларусь *</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇧🇪 België / Belgique / Belgien</sub></td>
<td width="20%" align="left"><sub>🇧🇴 Bolivia *</sub></td>
<td width="20%" align="left"><sub>🇧🇦 Bosna i Hercegovina / Босна и Херцеговина *</sub></td>
<td width="20%" align="left"><sub>🇧🇷 Brasil</sub></td>
<td width="20%" align="left"><sub>🇧🇬 България *</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇨🇦 Canada</sub></td>
<td width="20%" align="left"><sub>🏝️ Caribbean *</sub></td>
<td width="20%" align="left"><sub>🇨🇱 Chile</sub></td>
<td width="20%" align="left"><sub>🇨🇳 中国 *</sub></td>
<td width="20%" align="left"><sub>🇨🇴 Colombia</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇨🇷 Costa Rica *</sub></td>
<td width="20%" align="left"><sub>🇨🇮 Côte d'Ivoire *</sub></td>
<td width="20%" align="left"><sub>🇭🇷 Hrvatska *</sub></td>
<td width="20%" align="left"><sub>🇨🇿 Česká republika</sub></td>
<td width="20%" align="left"><sub>🇨🇾 Κύπρος / Kıbrıs *</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇩🇰 Danmark</sub></td>
<td width="20%" align="left"><sub>🇩🇴 Rep. Dominicana *</sub></td>
<td width="20%" align="left"><sub>🇪🇨 Ecuador *</sub></td>
<td width="20%" align="left"><sub>🇪🇬 مصر *</sub></td>
<td width="20%" align="left"><sub>🇸🇻 El Salvador *</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇪🇪 Eesti *</sub></td>
<td width="20%" align="left"><sub>🇫🇴 Færøerne / Føroyar *</sub></td>
<td width="20%" align="left"><sub>🇫🇮 Suomi / Finland</sub></td>
<td width="20%" align="left"><sub>🇫🇷 France</sub></td>
<td width="20%" align="left"><sub>🇬🇪 საქართველო *</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇩🇪 Deutschland</sub></td>
<td width="20%" align="left"><sub>🇬🇭 Ghana *</sub></td>
<td width="20%" align="left"><sub>🇬🇷 Ελλάδα</sub></td>
<td width="20%" align="left"><sub>🇬🇹 Guatemala *</sub></td>
<td width="20%" align="left"><sub>🇭🇳 Honduras *</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇭🇰 Hong Kong / 香港</sub></td>
<td width="20%" align="left"><sub>🇭🇺 Magyarország</sub></td>
<td width="20%" align="left"><sub>🇮🇪 Ireland / Éire</sub></td>
<td width="20%" align="left"><sub>🇮🇸 Ísland *</sub></td>
<td width="20%" align="left"><sub>🇮🇳 Bharat भारत</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇮🇩 Indonesia</sub></td>
<td width="20%" align="left"><sub>🇮🇱 יִשְׂרָאֵל</sub></td>
<td width="20%" align="left"><sub>🇮🇹 Italia</sub></td>
<td width="20%" align="left"><sub>🇯🇲 Jamaica *</sub></td>
<td width="20%" align="left"><sub>🇯🇵 日本</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇰🇿 Қазақстан *</sub></td>
<td width="20%" align="left"><sub>🇰🇪 Kenya *</sub></td>
<td width="20%" align="left"><sub>🇱🇻 Latvija *</sub></td>
<td width="20%" align="left"><sub>🇱🇧 لبنان *</sub></td>
<td width="20%" align="left"><sub>🇱🇮 Liechtenstein *</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇱🇾 Libya / ليبيا *</sub></td>
<td width="20%" align="left"><sub>🇱🇹 Lietuva *</sub></td>
<td width="20%" align="left"><sub>🇱🇺 Lëtzebuerg / Luxembourg / Luxemburg *</sub></td>
<td width="20%" align="left"><sub>🇲🇴 Macao / 澳門 *</sub></td>
<td width="20%" align="left"><sub>🇲🇬 Madagasikara *</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇲🇼 Malawi *</sub></td>
<td width="20%" align="left"><sub>🇲🇾 Bahasa Melayu *</sub></td>
<td width="20%" align="left"><sub>🇲🇹 Malta *</sub></td>
<td width="20%" align="left"><sub>🇲🇺 Mauritius *</sub></td>
<td width="20%" align="left"><sub>🇲🇽 México</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇲🇰 Северна Македонија *</sub></td>
<td width="20%" align="left"><sub>🇲🇳 Монгол *</sub></td>
<td width="20%" align="left"><sub>🇲🇪 Crna Gora / Črna Гора *</sub></td>
<td width="20%" align="left"><sub>🇲🇦 المغرب *</sub></td>
<td width="20%" align="left"><sub>🇲🇨 Monaco / Mónegue *</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇲🇿 Moçambique *</sub></td>
<td width="20%" align="left"><sub>🇳🇦 Namibia *</sub></td>
<td width="20%" align="left"><sub>🇳🇱 Nederland</sub></td>
<td width="20%" align="left"><sub>🇳🇨 Nouvelle-Calédonie *</sub></td>
<td width="20%" align="left"><sub>🇳🇿 New Zealand / Aotearoa</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇳🇮 Nicaragua *</sub></td>
<td width="20%" align="left"><sub>🇳🇬 Nigeria *</sub></td>
<td width="20%" align="left"><sub>🇳🇴 Norge / Noreg</sub></td>
<td width="20%" align="left"><sub>🇵🇰 Pakistan *</sub></td>
<td width="20%" align="left"><sub>🇵🇦 Panamá *</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇵🇾 Paraguay *</sub></td>
<td width="20%" align="left"><sub>🇵🇪 Perú *</sub></td>
<td width="20%" align="left"><sub>🇵🇭 Pilipinas *</sub></td>
<td width="20%" align="left"><sub>🇵🇱 Polska</sub></td>
<td width="20%" align="left"><sub>🇵🇸 فلسطين *</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇵🇹 Portugal</sub></td>
<td width="20%" align="left"><sub>🇵🇷 Puerto Rico *</sub></td>
<td width="20%" align="left"><sub>🇶🇦 قطر *</sub></td>
<td width="20%" align="left"><sub>🇷🇴 România</sub></td>
<td width="20%" align="left"><sub>🇷🇺 Россия</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇷🇸 Gora / Црна Гора *</sub></td>
<td width="20%" align="left"><sub>🇸🇲 San Marino *</sub></td>
<td width="20%" align="left"><sub>🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland *</sub></td>
<td width="20%" align="left"><sub>🇸🇬 Singapore / 新加坡 / சிங்கப்பூர் / Singapura</sub></td>
<td width="20%" align="left"><sub>🇸🇰 Slovensko *</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇸🇮 Slovenija *</sub></td>
<td width="20%" align="left"><sub>🇿🇦 South Africa *</sub></td>
<td width="20%" align="left"><sub>🇰🇷 대한민국</sub></td>
<td width="20%" align="left"><sub>🇸🇪 Sverige</sub></td>
<td width="20%" align="left"><sub>🇨🇭 Schweiz / Suisse / Svizzera / Svizra</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇹🇼 Taiwan / 臺灣</sub></td>
<td width="20%" align="left"><sub>🇹🇭 ประเทศไทย</sub></td>
<td width="20%" align="left"><sub>🇹🇷 Türkiye</sub></td>
<td width="20%" align="left"><sub>🇺🇬 Uganda *</sub></td>
<td width="20%" align="left"><sub>🇺🇦 Украïна *</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇦🇪 Al-Imarat *</sub></td>
<td width="20%" align="left"><sub>🇬🇧 United Kingdom / Cymru / Alba</sub></td>
<td width="20%" align="left"><sub>🇺🇸 United States</sub></td>
<td width="20%" align="left"><sub>🇺🇾 Uruguay *</sub></td>
<td width="20%" align="left"><sub>🇺🇿 Oʻzbekiston *</sub></td>
</tr>
<tr>
<td width="20%" align="left"><sub>🇻🇦 Città del Vaticano *</sub></td>
<td width="20%" align="left"><sub>🇻🇪 Venezuela</sub></td>
<td width="20%" align="left"><sub>🇻🇳 Việt Nam *</sub></td>
<td width="20%" align="left"><sub>🇿🇲 Zambia *</sub></td>
<td width="20%" align="left"><sub>🇿🇼 Zimbabwe *</sub></td>
</tr>
</table>...
* 🌍 Only worldwide platforms




### 📡 Streaming platforms availability

Availability varies by country. The most common platforms supported:

| Platform | Main countries |
|----------|---------------|
| Netflix | 🌍 Worldwide (190+ countries) |
| Amazon Prime Video | 🌍 Worldwide (200+ countries) |
| Disney+ | 🇺🇸🇬🇧🇪🇸🇫🇷🇩🇪🇮🇹🇦🇺🇨🇦🇯🇵 + more |
| HBO Max / Max | 🇺🇸🇬🇧🇪🇸🇵🇹🇳🇱🇸🇪🇩🇰🇳🇴🇫🇮 + more |
| Apple TV+ | 🌍 Worldwide |
| Hulu | 🇺🇸 |
| Peacock | 🇺🇸 |
| Paramount+ | 🇺🇸🇬🇧🇪🇸🇫🇷🇩🇪🇮🇹🇦🇺🇨🇦 + more |
| Movistar+ | 🇪🇸 |
|3Cat | 🇪🇸 <sub>(Catalunya)</sub> |
| RTVE Play | 🇪🇸 |
| Atresplayer | 🇪🇸 |

---
<div align="center">

<img src="https://github.com/janfajessen/What-s-On-TV-Search-and-Notify-Card/blob/b3645cf0af684bdde893675cb4c80660424873ba/home_assistant_logo.png" alt="Home Assistant" width="60">

<br>

  
</div>
---

## 📄 License

MIT License — © janfajessen


