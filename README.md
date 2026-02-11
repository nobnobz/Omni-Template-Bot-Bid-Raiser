# Omni Template Bot-Bid-Raiser
A curated Omni + AIOStreams + AIOMetadata setup with a minimal formatter and consistent regex icon tags. Includes ready-to-import templates, configs, and an Omni snapshot to restore the full UI in minutes.

## Screenshots
<img width="1456" height="827" alt="image" src="https://github.com/user-attachments/assets/3e6e7379-8da0-46cf-9baa-6b2d0a10d045" />
<img width="1459" height="839" alt="image" src="https://github.com/user-attachments/assets/47aa08a4-866b-42e7-95c7-6145e658169e" />
<img width="1465" height="825" alt="image" src="https://github.com/user-attachments/assets/9a449ca7-6434-406b-8b2e-50e40b5aed34" />
<img width="1422" height="602" alt="image" src="https://github.com/user-attachments/assets/a639422c-d31b-450b-a10d-dbe20cd82912" />
<img width="1503" height="741" alt="image" src="https://github.com/user-attachments/assets/933f83ea-3d33-4b7e-92dc-fad0fd362f49" />


## What’s Included

You can find the following **JSON files**:

- **AIOStreams template** (imports streaming addons, scraper, sorting, formatter, etc.)
- **AIOMetadata config** (imports catalogs, metadata rules)
- **Omni snapshot** (restores Omni setup including addons, catalogs layout, visuals)
- **Regex/icon configuration** used by Omni to display video/audio/source tags consistently
- **Optional: Formatter template** if you just want to use the formatter and not the whole setup

---

## Setup Overview

### Components
- **AIOStreams**: provides streams and applies sorting + formatting.
- **AIOMetadata**: provides metadata catalogs and curated lists/collections.
- **Omni**: consumes both addons and displays everything with your UI + regex icons.

### Formatter Principles
- **Omni regex tags/icons are the primary media-info surface** (Remux/Blu-ray/WEB, HDR/DV, audio formats, etc.)
- The **AIOStreams formatter focuses on**: title, cached status, score badge, languages, runtime, size/bitrate, addons, and “notes”.

---

## Formatter (Short Explanation)

The formatter was intentionally **simplified** to keep the stream list clean. Most technical media info (Remux/HDR/DV/audio) is shown via **Omni regex tags/icons** instead of printing long tag lists in the stream name.

### What the formatter shows

**1) Title line with status icon**  
Next to the movie/show title you’ll see one of these icons: 

- **(⤓)** → the stream is in your **Library**
- **(⧉)** → the stream is **Usenet**
- **(⌁)** → **Cached** (instantly playable)
- **(∅)** → **Uncached** (needs downloading / not instantly available)

**2) Language**
If language metadata is available it will be shown

**3) Runtime**  
The formatter includes the **runtime**:
- movie runtime, or
- episode runtime for series (when available)

**4) Size & bitrate**  
The formatter includes **file size** and **bitrate** (when available):  
- Size shown as smart bytes (e.g., `4.7 GB`)  
- Bitrate shown as smart bitrate (e.g., `12.3 Mbps`)

**2) Addons + score badge**  
Next to the Addons there’s a compact badge that represents the new regex scoring:

- **♛** = **5★**
- **⭑** = **4★**
- **✦** = **3★**
- **△** = **2★**
- **⊘** = **1★ or 0★**

**Note:** If you’re using UsenetStreamer, health-checked NZBs show a checkmark (✓) next to the indexer name.

**5) Notes (editions/cuts)**
The formatter includes release notes such as the Streaming Services, Extended, Director’s Cut, Theatrical Cut, Anniversary Edition, etc. (when available via stream.edition).

That’s it — everything else (video/audio features) is handled by Omni’s regex icon tags.

<img width="1503" height="741" alt="image" src="https://github.com/user-attachments/assets/933f83ea-3d33-4b7e-92dc-fad0fd362f49" />

---
## How to Install

### Requirements / Recommended instances
This setup currently works best with these instances:

**AIOStreams**
- https://aiostreamsfortheweebsstable.midnightignite.me/stremio/configure
- https://aiostreamsnightlyfortheweak.nhyira.dev/stremio/configure

**AIOMetadata**
- https://aiometadatafortheweebs.midnightignite.me/configure/
- https://aiometadatafortheweak.nhyira.dev/configure/

---

### 1) Download the files
Download all **four JSON files** from this repo:
- AIOStreams template
- AIOMetadata config
- Omni snapshot
- Omni regex patterns

---

### 2) Import the AIOStreams template
1. Open **AIOStreams**
2. Go to **Save & Install → Import → Import Template**
3. Import the AIOStreams template
4. Add your Debrid provider + TMDB + TVDB API keys under **Services** (if not already done during import)
5. Optional: Set your preferred language in **Filters**
6. Optional (for TorBox users): Enable the **TorBox Addon**

---

### 3) Create your AIOStreams setup
1. Go to **Save & Install**
2. Enter a password
3. Click **Create**

**Important**
- Save your **UUID** + password (you’ll need them to edit your setup later).

---

### 4) Add AIOStreams to Omni
- Copy the **manifest URL** from AIOStreams
- Add it in **Omni → Addons**

---

### 5) Set up AIOMetadata
1. Open **AIOMetadata**
2. Import my config
3. Add your API keys
4. Set a password
5. Save your **UUID**
6. Click **Save**
7. Copy the manifest URL and add it in **Omni → Addons**

---

### 6) Import Omni regex patterns (do this BEFORE restoring the snapshot)
1. Open **Omni**
2. Go to **Settings → Regex Patterns**
3. Import the regex JSON from one of these links:

**Link**
- https://raw.githubusercontent.com/nobnobz/Omni-Template-Bot-Bid-Raiser/main/omni-regex_02-06_11-25-28.omni.json

It is recommended to to this **before** restoring the snapshot, because the snapshot references the regex styling/colors.

---

### 7) Import the Omni snapshot
Copy the Omni snapshot `.json` file to:

`My Phone → Omni → Backups`

---

### 8) Restore the snapshot in Omni
1. Restart **Omni**
2. Go to **Settings → Snapshot**
3. Select the snapshot you imported
4. Restore it

Done — everything should now be set up.

## Changelog

<details open>
  <summary><strong>v1.5</strong></summary>

### Catalogs / UI
- Added new **Directors**.
- Added **Crunchyroll** catalog.
- Added a **Denzel Washington** catalog (requested).

### Regex / Tags (Omni)
- Updated Omni regex templates:
  - Added **fallback icons** for **Remux / Blu-ray / WEB-DL** when a stream doesn’t match tier 1–3.
  - Updated **Atmos** and **DV** tags.
  - Updated **DD+** logic: **DD+ now only shows if there is no Atmos tag**, to reduce tag clutter.

### Sorting / Filtering
- Optimized sorting and filtering so more **low-score results** get filtered out.

### AIOStreams Formatter
- Minimized the formatter further:
  - Removed the line that printed **release type** (Remux / Blu-ray / WEB-DL), since this is now covered via Omni fallback tags.
- Replaced some icon-spacing logic with **text-based spacing** for cleaner, more consistent formatting.

### Fixes
- Updated one **Apple TV** catalog (Pluribus was missing).
- Fixed some **empty actors**.

### Limits
- Increased max streams from **12 → 15**.

</details>

<details>
  <summary><strong>v1.4</strong></summary>

### UI / Catalogs
- Updated banner for **Crime**
- Added new genres: **Mindgame movies**, **Seasonal movies**, **Anime**, **K-Drama**
- Updated banners for **directors** and **actors** to look cleaner
- **Actors and directors are now separated**
- Updated actor catalogs to filter out low-quality entries
- Most actor catalogs now update automatically
- Added new collections: **Dune**, **The Godfather**, **John Wick**, **The Matrix**, **Rambo**, **Star Trek**, **Transformers**
- Updated **Star Wars** catalog to include shows
- Optimized sorting across most catalogs

### Regex / Sorting / Templates
- Updated to the newest regex set (Vidhin)
- Switched to the latest SEL template (Tam) and optimized it
- Updated regex set from !Yuno and re-themed colors
- Own color scheme:
  - Remux / Blu-ray / Web releases each have distinct colors
  - Gold color is used for **video tags**
  - White color is used for **audio tags**
- Regex coverage expanded significantly (more categories match now)
- Formatter optimized accordingly: video/audio tags are no longer printed in the formatter and are shown through Omni regex tags/icons instead

</details>

---
## Notes / Troubleshooting

### Managing the large number of catalogs
This setup includes **a lot of catalogs**. You can disable or reorder them here:

**Omni → Settings → Group Management → (scroll down) → Main Groups**

That’s where you manage **collections, actors, directors, genres**, etc.

---

### Customize (or disable) regex tag colors
You can change tag styling (including **colors**) or disable specific tags here:

**Omni → Settings → Regex Patterns**

---

### Increase the max number of streams (AIOStreams)
By default, this template limits results to **15 streams**.

To increase it:
1. Open **AIOStreams → Filters**
2. Under **EXCLUDED STREAM EXPRESSIONS**, find the global limit rule and change the number (or remove the rule)

Current rule:
```txt
/*Global Result Limit: 15*/slice(negate(merge(library(streams), cached(seadex(streams))), streams), 15)

## Artwork
**Actors/Directors:** https://postimg.cc/gallery/3kjchpC
**Genres:** https://postimg.cc/gallery/VsT9R6V
**Decades:** https://postimg.cc/gallery/v5hCxKd
**Streaming Services & Trending/Latest:** https://postimg.cc/gallery/gXh7xgR

## Credits
- AIOStreams community templates and formatter/SEL inspiration
- Regex sources referenced in the changelog (Vidhin, Tam, !Yuno)
- Some of the Artwork is used or inspired from houndReaper
- Everyone who helped me on Discord setting this up

---
