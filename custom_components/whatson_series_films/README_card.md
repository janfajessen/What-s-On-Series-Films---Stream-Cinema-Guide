# 📺 What's On TV — Series & Films Card

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![HA Version](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-blue.svg)](https://www.home-assistant.io/)
[![Card Version](https://img.shields.io/badge/Card-v1.2.0-green.svg)](https://github.com/janfajessen/whatson-series-films-card)

A Lovelace card for the [What's On TV](https://github.com/janfajessen/whatsontv) Home Assistant integration. Shows movies in theaters, new releases on streaming platforms, and tracks your followed TV series via TVmaze — all in one beautiful scrollable card.

![Card Preview](preview.png)

---

## ✨ Features

- 🎬 **Cinema** — Now playing & upcoming releases in your country
- 📡 **Streaming platforms** — New movies and series/docs grouped by platform (Netflix, Amazon, Disney+, etc.)
- 📺 **TVmaze Following** — Track your series with poster, channel, rating, last/next episode
- 🌍 **49 languages** — Auto-detects your HA language
- 🎨 **Fully customizable** — Dark/light theme, 8 accent color presets + custom HEX/RGB
- ⚙️ **Visual editor** — Add/remove specific sensors, no YAML needed
- 🖱️ **Smooth horizontal scroll** — Mouse wheel and touch support
- 💡 **Auto-discovery** — Finds all `sensor.whatson_*` sensors automatically

---

## 📦 Installation

### Via HACS (recommended)
1. Open HACS → Frontend → **+ Explore & Download Repositories**
2. Search for **What's On TV Series & Films Card**
3. Download and restart HA

### Manual
1. Copy `whatson-series-films-card.js` to `/config/www/`
2. Go to **Settings → Dashboards → Resources**
3. Add `/local/whatson-series-films-card.js` as **JavaScript Module**
4. Copy `whatson_tv_icon.png` to `/config/www/`

---

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

## 🗺️ Available countries

The What's On TV integration supports the following countries for cinema and streaming platforms. Use the 2-letter country code in your integration configuration.

### 🎬 Cinema (TMDB Now Playing / Upcoming)

| Flag | Country | Code |
|------|---------|------|
| 🇦🇩 | Andorra | `AD` |
| 🇦🇷 | Argentina | `AR` |
| 🇦🇺 | Australia | `AU` |
| 🇦🇹 | Austria | `AT` |
| 🇧🇪 | Belgium | `BE` |
| 🇧🇷 | Brazil | `BR` |
| 🇨🇦 | Canada | `CA` |
| 🇨🇱 | Chile | `CL` |
| 🇨🇴 | Colombia | `CO` |
| 🇨🇿 | Czech Republic | `CZ` |
| 🇩🇰 | Denmark | `DK` |
| 🇫🇮 | Finland | `FI` |
| 🇫🇷 | France | `FR` |
| 🇩🇪 | Germany | `DE` |
| 🇬🇷 | Greece | `GR` |
| 🇭🇰 | Hong Kong | `HK` |
| 🇭🇺 | Hungary | `HU` |
| 🇮🇳 | India | `IN` |
| 🇮🇩 | Indonesia | `ID` |
| 🇮🇪 | Ireland | `IE` |
| 🇮🇱 | Israel | `IL` |
| 🇮🇹 | Italy | `IT` |
| 🇯🇵 | Japan | `JP` |
| 🇲🇽 | Mexico | `MX` |
| 🇳🇱 | Netherlands | `NL` |
| 🇳🇿 | New Zealand | `NZ` |
| 🇳🇴 | Norway | `NO` |
| 🇵🇱 | Poland | `PL` |
| 🇵🇹 | Portugal | `PT` |
| 🇷🇴 | Romania | `RO` |
| 🇷🇺 | Russia | `RU` |
| 🇸🇦 | Saudi Arabia | `SA` |
| 🇸🇬 | Singapore | `SG` |
| 🇰🇷 | South Korea | `KR` |
| 🇪🇸 | Spain | `ES` |
| 🇸🇪 | Sweden | `SE` |
| 🇨🇭 | Switzerland | `CH` |
| 🇹🇼 | Taiwan | `TW` |
| 🇹🇭 | Thailand | `TH` |
| 🇹🇷 | Turkey | `TR` |
| 🇬🇧 | United Kingdom | `GB` |
| 🇺🇸 | United States | `US` |
| 🇻🇪 | Venezuela | `VE` |

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

## 📋 Requirements

- Home Assistant 2024.1+
- [What's On TV integration](https://github.com/janfajessen/whatsontv) installed
- TMDB API key (free at [themoviedb.org](https://www.themoviedb.org/settings/api))
- TVmaze API key (optional, for series tracking)

---

## 🤝 Related cards

- [What's On TV EPG Card](https://github.com/janfajessen/What-s-On-TV-EPG-TV-Guide-Card) — Full TV guide / EPG
- [What's On TV Notify Card](https://github.com/janfajessen/whatsontv-notify-card) — Search & notifications

---

## 📄 License

MIT License — © janfajessen
