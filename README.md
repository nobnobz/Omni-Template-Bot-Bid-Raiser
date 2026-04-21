# Unified Media Experience (UME)

A curated **Omni + AIOStreams + AIOMetadata** setup with a minimal formatter, consistent regex icon tags, and a browser-based management tool.

This repo includes the files needed to rebuild or reuse my setup, while the **Omni Snapshot Manager** makes it much easier to edit, maintain, and update your configuration through a visual interface instead of raw JSON.

## Omni Snapshot Manager

You can manage and update your setup directly here:

**Omni Snapshot Manager:**  
https://nobnobz.github.io/omni-snapshot-editor/

The Snapshot Manager lets you:

- import your current **Omni Snapshot**
- edit **groups, subgroups, catalogs, layouts, and regex-related settings**
- update an existing setup with **Update from Template**
- review detected additions and changes before importing
- import only the parts you actually want
- export a cleaned-up final snapshot

It can also be added to your home screen as a **web app / PWA** for quicker access.

> **Important:** All downloads are also available directly inside the Snapshot Manager.  
> You can still use this GitHub repo for changelogs, documentation, and manual downloads.

---

## 💖 Support the Project
If this tool makes your Omni management easier, please consider supporting the continued development.

[<img src="https://cdn.prod.website-files.com/5c14e387dab576fe667689cf/670f5a02fcf48af59c591185_support_me_on_kofi_dark.png" width="230" alt="Support my work at Ko-fi">](https://ko-fi.com/botbidraiser)

---

## Screenshots

![screenshot-studio-1774735254212 2](https://github.com/user-attachments/assets/e5ac8528-ffa4-42c5-abb1-8dbc695a5c6f)
![screenshot-studio-1774735232835 2](https://github.com/user-attachments/assets/ceaae051-63c9-44d0-a0cd-055c5d04dc67)
![screenshot-studio-1774735201773 2](https://github.com/user-attachments/assets/73322fb9-d3fd-4652-861e-a2b1e368529f)
![screenshot-studio-1774737638023 2](https://github.com/user-attachments/assets/aaceed34-8a32-4a32-9241-0b2a87598dc6)


---

## What’s Included

You can find the following files in this repo and in the **Snapshot Manager** downloads section:

The repo also publishes an automatically generated `template-manifest.json` in the root. It is built from the existing template files, so adding a new matching template file updates the manifest without maintaining a separate URL mapping file.

The repo also includes an automated release-group sync for `Other/fusion-tags-ume.json`, `Other/fusion-tags-ume-colored.json`, and `Other/fusion-tags-ume-minimalistic.json` via `scripts/update_release_groups.py` (run daily in GitHub Actions).
It downloads upstream regexes, merges mapped Radarr/Sonarr/Web entries into REMUX/BLU-RAY/WEB T1-T3 buckets, applies tier conflict priority (`T1 > T2 > T3 > Unranked`), and rebuilds Unranked exclusion lists from the final deduplicated T1-T3 union.

- **Omni snapshot**  
  Restores my Omni setup including addons, catalog layout, groups, visuals, and structure.

- **AIOMetadata config**  
  Imports catalogs, metadata rules, and artwork sources.
  
 - **AIOStreams template**  
  Imports streaming addons, scraper settings, sorting, formatter, filters, etc.

- **Optional AIOStreams formatter template**  
  For users who only want the formatter and not the full setup.

---

## Setup Overview

### Components

- **Omni** → consumes both addons and displays everything with UI, groups, posters, and regex icons
- **AIOMetadata** → provides metadata catalogs and curated lists/collections
- **AIOStreams** → provides streams and applies sorting + formatting


### Formatter Principles

- **Omni regex tags/icons are the main media-info layer**  
  (Remux / Blu-ray / WEB, HDR / DV, audio formats, etc.)

- The **AIOStreams formatter focuses on compact stream info**, such as:
  - title
  - cached status
  - score badge
  - languages
  - runtime
  - size / bitrate
  - addons
  - notes / editions

---

## Formatter (Short Explanation)

The formatter was intentionally simplified to keep the stream list clean.

Most technical media info such as **Remux / HDR / DV / audio formats** is shown via **Omni regex tags/icons** instead of printing long tag lists in the stream name.

### What the formatter shows

**1) Title line with status icon**  
Next to the movie/show title you’ll see one of these icons:

- **(⤓)** → the stream is in your **Library**
- **(⧉)** → the stream is **Usenet**
- **(⌁)** → **Cached** (instantly playable)
- **(∅)** → **Uncached** (needs downloading / not instantly available)

**2) Language**  
If language metadata is available, it will be shown.

**3) Runtime**  
The formatter includes the runtime:
- movie runtime, or
- episode runtime for series (when available)

**4) Size & bitrate**  
The formatter includes **file size** and **bitrate** when available:
- size shown as smart bytes (e.g. `4.7 GB`)
- bitrate shown as smart bitrate (e.g. `12.3 Mbps`)

**5) Addons + score badge**  
Next to the addons there’s a compact badge that represents the regex scoring:

- **♛** = **5★** (highest scored streams)
- **⭑** = **4★**
- **✦** = **3★**
- **△** = **2★**
- **⊘** = **1★ or 0★** (lowest scored streams)

> If you’re using **UsenetStreamer**, health-checked NZBs show a checkmark (**✓**) next to the indexer name.

**6) Notes / editions / cuts**  
The formatter includes release notes such as:
- streaming services
- extended editions
- director’s cut
- theatrical cut
- anniversary edition

That’s it — everything else is handled by Omni’s regex icon tags.

<img width="1503" height="741" alt="image" src="https://github.com/user-attachments/assets/933f83ea-3d33-4b7e-92dc-fad0fd362f49" />

---

## How to Install

## Recommended approach

The easiest way to use and maintain this setup is through the **Omni Snapshot Manager**:

https://nobnobz.github.io/omni-snapshot-editor/

You can use it to:
- access all downloads
- edit snapshots visually
- update an existing setup from a newer template version
- export a cleaned-up final snapshot

If you prefer to do everything manually, follow the steps below.

---

### Requirements / Recommended instances

This setup currently works best with these instances:

**AIOStreams**
- https://aiostreamsfortheweebsstable.midnightignite.me/stremio/configure
- https://aiostreamsnightlyfortheweak.nhyira.dev/stremio/configure

**AIOMetadata**
- https://aiometadatafortheweebs.midnightignite.me/configure/
- https://aiometadata.fortheweak.cloud/configure/
  
---

### 1) Download the files

Download all required files either:

- directly from this repo, or
- through the **Snapshot Manager** downloads section

Main files:
- AIOStreams template
- AIOMetadata config
- Omni snapshot

---

### 2) Import the AIOStreams template

1. Open **AIOStreams**
2. Go to **Save & Install → Import → Import Template**
3. Import the AIOStreams template and follow the steps.

---

### 3) Create your AIOStreams setup

1. Go to **Save & Install**
2. Enter a password
3. Click **Create**

**Important**
- Save your **UUID** and password, because you’ll need them to edit your setup later.

---

### 4) Add AIOStreams to Omni

- Copy the **manifest URL** from AIOStreams
- Add it in **Omni → Addons**

---

### 5) Set up AIOMetadata

1. Open **AIOMetadata**
2. Import my config
3. Add your API keys  
   *(don’t forget your MDBList API key)*
4. Set a password
5. Save your **UUID**
6. Click **Save**
7. Copy the manifest URL and add it in **Omni → Addons**

---

### 6) Import the Omni snapshot

Copy the Omni snapshot `.json` file to:

`My Phone → Omni → Backups`

On macOS open the Finder, press Shift+Command+G and enter 

`~/Library/Containers/Omni/Data/Documents/Backups`

If this does not try to go to `/Users/YOUR_USERNAME/Library/Containers/win.stkc.omni/Data/Documents/Backups/`

---

### 7) Restore the snapshot in Omni

1. Restart **Omni**
2. Go to **Settings → Snapshot**
3. Select the snapshot you imported
4. Restore it

Done — everything should now be set up.

---

## Updating an Existing Setup

One of the main advantages of the **Snapshot Manager** is that you no longer have to rebuild your whole Omni setup whenever I release a new template version.

### Recommended update flow

1. Update **AIOMetadata** first, so the new catalogs are available
2. Import your **current Omni Snapshot** into the Snapshot Manager
3. Open **Catalog Manager**
4. Use **Update from Template**
5. Review detected additions or changes, such as:
   - new groups
   - new catalogs
   - updated subgroup content
   - image updates
6. Import only the changes you want
7. Reorder, rename, and personalize everything afterwards

This makes it much easier to keep your setup current while preserving your own structure and customization.

---

## Changelog

The full release history now lives in [CHANGELOG.md](./CHANGELOG.md).

---

### Managing the large number of catalogs

This setup includes a **lot of catalogs**. You can disable or reorder them here:

**Omni → Settings → Group Management → Main Groups**

That’s where you manage collections, actors, directors, genres, and more.

You can also manage this much more comfortably through the **Snapshot Manager**.

---

### My catalogs are empty

Make sure you have added your **MDBList API key** in AIOMetadata.  
Sometimes the catalogs need a few hours to fully load.

---

### Watchlist (Trakt Integration)

The Watchlist poster and group are **disabled by default**, because they require your personal Trakt watchlist.

To enable:

1. In **Omni → Settings → Trakt → My Lists**
   - Connect your Trakt account
   - Add your **Watchlist** as a catalog

2. Go to **Settings → Groups → Watchlist**
   - Add your newly created Trakt Watchlist catalog to the group

3. Go to **Discover**
   - Activate the **Watchlist** group

Once configured, the Watchlist poster and catalog will work as intended.

---

### Customize or disable regex tag colors

You can change tag styling, including colors, or disable specific tags here:

**Omni → Settings → Regex Patterns**

---

### Increase the max number of streams (AIOStreams)

By default, this template limits results to **15 streams**.

To increase it:

1. Open **AIOStreams → Filters**
2. Under **Excluded Stream Expressions**, find the global limit rule and change the number (or remove the rule)

Current rule:

- `/*Global Result Limit: 15*/slice(negate(merge(library(streams), cached(seadex(streams))), streams), 15)`

---

## Artwork

- **Actors / Directors:** https://postimg.cc/gallery/3kjchpC
- **Genres:** https://postimg.cc/gallery/VsT9R6V
- **Decades:** https://postimg.cc/gallery/v5hCxKd
- **Streaming Services & Trending / Latest:** https://postimg.cc/gallery/gXh7xgR

---

## Credits

- AIOStreams community templates and formatter / SEL inspiration
- Regex sources referenced in the changelog (**Vidhin, Tam, !Yuno**)
- Some artwork is used or inspired by **houndReaper**
- Everyone who helped me on Discord with testing, ideas, and setup work
