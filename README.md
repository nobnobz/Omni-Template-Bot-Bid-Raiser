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
<img width="1503" height="741" alt="image" src="https://github.com/user-attachments/assets/933f83ea-3d33-4b7e-92dc-fad0fd362f49" />

---

## What’s Included

You can find the following files in this repo and in the **Snapshot Manager** downloads section:

The repo also publishes an automatically generated `template-manifest.json` in the root. It is built from the existing template files, so adding a new matching template file updates the manifest without maintaining a separate URL mapping file.

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
- https://aiometadatafortheweak.nhyira.dev/configure/

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

<details open>
  <summary><strong>v2.2</strong></summary>

### Added Collections
- Are You Afraid of the Dark?
- American Pie
- Bad Boys
- Bourne Collection
- Candyman
- Expendables
- Die Hard
- Now You See Me
- Karate Kid
- Police Academy
- Resident Evil

### Added Genre
- Adventure

### Fixed
- Fixed broken catalogs
- General bug fixes and improvements

</details>

<details open>
  <summary><strong>v2.1</strong></summary>

### Collections
- Added **A Nightmare On Elm Street**
- Added **A Quiet Place**
- Added **The Exorcist**
- Added **Blair Witch**
- Added **Chucky**
- Added **Dexter**
- Added **Final Destination**
- Added **Friday the 13th**
- Added **Ghostbusters**
- Added **Halloween**
- Added **Gremlins**
- Added **The Shining**
- Added **The Purge**
- Added **The Conjuring Universe**
- Added **Terrifier**
- Added **Saw**
- Added **Psycho**
- Added **It**
- Added **Happy Death Day**
- Added **Paranormal Activity**
- Added **Quarantine**
- Added **Hannibal Lecter**
- Added **xXx**

### Actors
- Added **Chuck Norris**

### Streaming Services
- Added **AMC+**
- Added **BritBox**
- Added **MagellanTV**
- Added **STARZ**
- Added **Curiosity Stream**
- Added **discovery+**
- Added **MUBI**
- Added **Netflix Kids**
- Added **The Criterion Channel**

</details>

<details open>
  <summary><strong>v2.0</strong></summary>

### Snapshot Manager / Compatibility
- Full compatibility with the **Omni Snapshot Manager**
- Setup can now be maintained and updated much more easily through the browser-based visual editor
- All downloads are also available directly inside the Snapshot Manager

### Collections
- Added **Rocky**
- Added **Scream**
- Added **Back to the Future**

### Actors
- Added **Arnold Schwarzenegger**
- Added **Christian Bale**
- Added **Clint Eastwood**
- Added **Jackie Chan**
- Added **Sylvester Stallone**

### Directors
- Added **Brian De Palma**

### Streaming Services
- Added **Shudder**

### Genres
- Added **Musical**
- Added **History**
- Added **War**

### Cleanup
- Cleaned up the JSON
- Improved overall structure and maintainability

</details>

<details open>
  <summary><strong>v1.7.1</strong></summary>

### UI / Posters
- Refined the **Awards posters** to better match the overall design language and improve visual consistency.
- Added a dedicated **Watchlist poster** (disabled by default).

### Catalogs
- Added a new **Spike Lee** catalog.
- Fixed and cleaned up several existing catalogs (minor structure and consistency adjustments).

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

</details>

<details open>
  <summary><strong>v1.7</strong></summary>

### Catalogs
- Added new award/festival catalogs:
  - **Academy Awards**
  - **Oscars 2026 nominees**
  - **Golden Globes**
  - **Emmys**
  - **Cannes Film Festival**
- Minor updates to some existing catalogs

### Addons
- Added **Meteor** addon

### Search / UX
- Fixed an issue where **People search** didn’t work

### AIOStreams (SEL / Sorting)
- Updated **excluded ESE**

### AIOMetadata (Metadata / Artwork)
- Optimized **metadata** and **artwork providers** for improved reliability and results

</details>

<details open>
  <summary><strong>v1.6.2</strong></summary>

### Catalogs
- Added a new **Timothée Chalamet** catalog

### AIOStreams (SEL / Sorting)
- Updated **Tam’s SEL** to the newest version
- Updated SELs to use **synced link-based sources** where compatible with this setup, so scoring stays up-to-date automatically

</details>

<details open>
  <summary><strong>v1.6.1</strong></summary>

### Anime
- Small improvements for anime handling
- Cleaned up the formatter so there are **no double badges for anime** anymore

### Omni Regex / Tags
- Added **WEB T4** regex pattern + icon
- Added **WEB T5** regex pattern + icon
- Added a regex pattern + icon for **SeaDex releases**

### Catalogs
- Updated the **Apple TV Shows** catalog
- Added back the **Top Shows & Movies of the Week** below the continue watching bar

</details>

<details open>
  <summary><strong>v1.6</strong></summary>

### Artwork / UI
- Reworked the **Decades** posters and improved several **Genre** posters
- If you prefer older or alternative versions, you can grab them here:
  - **Decades:** https://postimg.cc/gallery/v5hCxKd
  - **Genres:** https://postimg.cc/gallery/VsT9R6V

### Catalogs
- Added a new **Alien Collection** catalog
- Fixed a few **missing catalogs**

### AIOStreams (SEL / Sorting)
- Updated AIOStreams to use **Vidhin SEL links**, so scores should update automatically when he changes them
- Optimized **sound codec scoring** for **Apple TV**

### Omni Regex / Tags
- Updated HDR logic: **HDR10+ is only shown when DV is not present**  
- If your device/player doesn’t support **DV**, switch in Omni to **HDR patterns for non-DV devices** in **Omni → Settings → Regex**
- Updated 4K detection so the **4K badge no longer shows** when the release name also contains **1080p**

</details>

<details open>
  <summary><strong>v1.5.1</strong></summary>

### Catalogs / UI
- Added a new **Bollywood** catalog

### Regex / Tags (Omni)
- Updated HDR regex logic to avoid duplicate / lower-tier HDR labels

### Scoring / Sorting
- Tweaked **SEL scoring for Atmos** and optimized it further for **Apple TV**

</details>

<details open>
  <summary><strong>v1.5</strong></summary>

### Catalogs / UI
- Added new **Directors**
- Added **Crunchyroll** catalog
- Added a **Denzel Washington** catalog

### Regex / Tags (Omni)
- Updated Omni regex templates
- Added **fallback icons** for **Remux / Blu-ray / WEB-DL**
- Updated **Atmos** and **DV** tags
- Updated **DD+** logic so **DD+ only shows if there is no Atmos tag**

### Sorting / Filtering
- Optimized sorting and filtering so more **low-score results** get filtered out

### AIOStreams Formatter
- Simplified the formatter further and removed the printed release type line, since that info is covered via Omni regex tags

### Fixes
- Updated one **Apple TV** catalog
- Fixed some **empty actors**

### Limits
- Increased max streams from **12 → 15**

</details>

---

## Notes / Troubleshooting

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
