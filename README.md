# Omni-Template-Bot-Bid-Raiser
A curated Omni + AIOStreams + AIOMetadata setup with with minimal formatter. Includes full templates, configs &amp; snapshot for an easy import. The goal is to provide a clean and easy to use Omni UI.

## Screenshots
<img width="1456" height="827" alt="image" src="https://github.com/user-attachments/assets/3e6e7379-8da0-46cf-9baa-6b2d0a10d045" />
<img width="1459" height="839" alt="image" src="https://github.com/user-attachments/assets/47aa08a4-866b-42e7-95c7-6145e658169e" />
<img width="1460" height="831" alt="image" src="https://github.com/user-attachments/assets/c45fb4fd-d452-436e-a8a5-7046e33f465c" />
<img width="1422" height="602" alt="image" src="https://github.com/user-attachments/assets/a639422c-d31b-450b-a10d-dbe20cd82912" />
<img width="823" height="654" alt="image" src="https://github.com/user-attachments/assets/c0a15a22-db78-49f3-9477-c73003575197" />



## What’s Included

You can find **four JSON files**:

- **AIOStreams template** (imports streaming addons, scraper, sorting, formatter, etc.)
- **AIOMetadata config** (imports catalogs, metadata rules)
- **Omni snapshot** (restores Omni setup including addons, catalogs layout, visuals)
- **Regex/icon configuration** used by Omni to display video/audio/source tags consistently

---

## Setup Overview

### Components
- **AIOStreams**: provides streams and applies sorting + formatting.
- **AIOMetadata**: provides metadata catalogs and curated lists/collections.
- **Omni**: consumes both addons and displays everything with your UI + regex icons.

### Formatter Principles
- **Omni regex tags/icons are the primary media-info surface** (Remux/Blu-ray/WEB, HDR/DV, codecs, audio formats, etc.)
- The **AIOStreams formatter focuses on**: title, cached status, score badge, release type, languages, runtime, size/bitrate, provider, and “notes”.

---

## Formatter (Short Explanation)

The formatter was intentionally **simplified** to keep the stream list clean. Most technical media info (HDR/DV/codecs/audio) is shown via **Omni regex tags/icons** instead of printing long tag lists in the stream name.

### What the formatter shows

**1) Title line with status icon**  
Next to the movie/show title you’ll see one of these icons: 

- **(⤓)** → the stream is in your **Library**
- **(⧉)** → the stream is **Usenet**
- **(⌁)** → **Cached** (instantly playable)
- **(∅)** → **Uncached** (needs downloading / not instantly available)

**2) Quality + score badge**  
Next to the release type (e.g. **Remux / Blu-ray / WEB-DL / WEBRip**) there’s a compact badge that represents the new regex scoring capabilities:

- **♛** = **5★**
- **⭑** = **4★**
- **✦** = **3★**
- **△** = **2★**
- **⊘** = **1★ or 0★**

**3) Runtime**  
The formatter includes the **runtime**:
- movie runtime, or
- episode runtime for series (when available)

**4) Size & bitrate**  
The formatter includes **file size** and **bitrate** (when available):  
- Size shown as smart bytes (e.g., `4.7 GB`)  
- Bitrate shown as smart bitrate (e.g., `12.3 Mbps`)

**5) Notes (editions/cuts)**
The formatter includes release notes such as Extended, Director’s Cut, Theatrical Cut, Anniversary Edition, etc. (when available via stream.edition).

That’s it — everything else (video/audio features) is handled by Omni’s regex icon tags.

### Optional: Old Formatter
If you prefer seeing **audio/video tags directly in the stream title** (instead of relying only on Omni regex icons), I also provide my **old formatter**.

<img width="283" height="192" alt="image" src="https://github.com/user-attachments/assets/fca06c35-0528-4fe7-9c6c-6147aa3e0cd9" />

You can import it in **AIOStreams → Formatter → Import**.

Note: This will show more technical details in the stream name and may duplicate information already shown via Omni regex tags/icons.

---

## How to Install

### 1) Download the config files
Download all four `.json` files provided in this repo.

### 2) Import the AIOStreams template
1. Open **AIOStreams**
2. Go to **Save & Install → Import → Import Template**
3. Import the AIOStreams template  
4. Add your Debrid provider details and API keys under **Services** (only if you didn’t already add them during the template import)
5. Optional: If you want to add another language than English go to Filters and add your preferred language
6. Optional: If your are using TorBox enable the TB Search Addon in AIOStreams

**Important:** At the moment you must use an **AIOStreams Nightly** instance for this template to work.  
Use either of these:

- https://aiostreamsnightlyfortheweak.nhyira.dev/stremio/configure  
- https://aiostreamsfortheweebs.midnightignite.me/stremio/configure  

### 3) Create your AIOStreams setup
1. Go to **Save & Install**
2. Enter a password
3. Click **Create**

Important:
- Save your **UUID** and the password you entered.
- You’ll need them later to make changes in AIOStreams.

### 4) Add AIOStreams to Omni
- Copy the **manifest URL** from AIOStreams
- Add it in **Omni → Addons**

### 5) Set up AIOMetadata
1. Open **AIOMetadata**
2. Import my config file
3. Add your API keys
4. Set a password
5. Save your **UUID** (needed for future edits)
6. Click **Save**
7. Copy the manifest URL and add it in **Omni → Addons**

### 6) Import Omni Regex Patterns (Important — do this BEFORE restoring the snapshot)
Before importing/restoring the Omni snapshot, you must add my regex patterns link in Omni:

1. Open **Omni**
2. Go to **Settings → Regex Patterns**
3. Paste/import this link:

https://raw.githubusercontent.com/nobnobz/Omni-Template-Bot-Bid-Raiser/refs/heads/main/omni-regex_02-06_11-25-28.omni.json
OR
https://files.catbox.moe/x611rs.json

This must be done **before** restoring the snapshot, because the snapshot will apply the regex styling and colors inside Omni.

### 7) Import the Omni snapshot
Copy the Omni snapshot `.json` file to:

`My Phone → Omni → Backups`

(use your phone’s file explorer)

### 8) Restore the snapshot in Omni
1. Restart **Omni**
2. Go to **Settings → Snapshot**
3. Select the snapshot you just imported
4. Restore it

Done. Everything should now be set up.

---

## Changelog

### 1.3 → 1.4

**UI / Catalogs**
- Updated banner for **Crime**
- Added new genres: **Mindgame movies**, **Seasonal movies**, **Anime**, **K-Drama**
- Updated banners for **directors** and **actors** to look cleaner
- **Actors and directors are now separated**
- Updated actor catalogs to filter out low-quality entries
- Most actor catalogs now update automatically
- Added new collections: **Dune**, **The Godfather**, **John Wick**, **The Matrix**, **Rambo**, **Star Trek**, **Transformers**
- Updated **Star Wars** catalog to include shows
- Optimized sorting across most catalogs

**Regex / Sorting / Templates**
- Updated to the newest regex set (Vidhin)
- Switched to the latest SEL template (Tam) and optimized it
- Updated regex set from !Yuno and re-themed colors
- Own color scheme:
  - Remux / Blu-ray / Web releases each have distinct colors
  - Gold color is used for **video tags**
  - White color is used for **audio tags**
- Regex coverage expanded significantly (more categories match now)
- Formatter optimized accordingly: video/audio tags are no longer printed in the formatter and are shown through Omni regex tags/icons instead

---

## Notes / Troubleshooting

### Manage the large number of catalogs
Because this setup includes **a lot of catalogs**, you can disable or rearrange parts of it in:

**Omni → Settings → Group Management → (scroll all the way down) → Main Groups**

There you can **disable** or **reorder** collections, actors, genres, etc.

### Customize or disable regex tag colors
You can change the look of the tags (including **colors**) or disable specific tags in:

**Omni → Settings → Regex Patterns**

This is where you can adjust the regex styling to your preference.

### Stream limits in **AIOStreams** are set to **12 streams**. 
If you want more streams go to AIOStreams, Filters and delete or edit "/*Global Result Limit: 12*/slice(negate(merge(library(streams), cached(seadex(streams))), streams), 12)" under "EXCLUDED STREAM EXPRESSIONS" 

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
