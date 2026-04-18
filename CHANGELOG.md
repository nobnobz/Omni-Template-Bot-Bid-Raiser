# Changelog

<details open>
  <summary><strong>v3.0</strong></summary>

UME v3.0 is the largest UME update so far.

The release rebuilds, cleans up, expands, and restructures the setup from the ground up.

One of the biggest changes in v3.0 is that all catalogs were fully redone and now come directly from me. They were built with MDBList and created with the goal of delivering the best possible quality. The main advantage is that I can now maintain and improve them directly going forward, which should help prevent catalogs from becoming outdated, broken, or poorly maintained.

Most catalogs now update automatically. Since I exceeded the 300 MDBList limit, some collections are now linked to the official Trakt lists instead.

### New Main Sections

#### Awards
A new Awards section was added with:
- Academy Awards
- Academy Awards: Best Picture
- Primetime Emmy Awards
- Golden Globe Awards
- BAFTA Film Awards
- Cannes Film Festival Awards
- Venice Film Festival Awards
- Berlin International Film Festival Awards

#### Studios
A new Studios section was added with 20 studio collections, including:
- Warner Bros. Pictures
- Universal Pictures
- Paramount Pictures
- A24
- Metro-Goldwyn-Mayer
- 20th Century Studios
- Columbia Pictures
- Walt Disney Animation Studio
- DreamWorks Animation
- Pixar Animation Studios
- Illumination
- Marvel Studios
- Lucasfilm
- New Line Cinema
- Miramax
- Searchlight Pictures
- Touchstone Pictures
- TriStar Pictures
- Lionsgate
- Studio Ghibli

#### Lists
The Lists category is completely new and highlights popular curated movie lists, including many of the most popular ones from Letterboxd.

Added:
- Metacritic's Must See
- Certified Fresh Releases
- 1001 Movies You Must See Before You Die
- Movies Everyone Should Watch Once in Their Lifetime
- Letterboxd's Top 500
- 100 Best Movies of the 21st Century
- Mindgame Movies
- The Billion-Dollar Club
- Echoes of Reality
- Movies That Will Make You Say WTF
- Movies That Leave You Changed
- For When You Need to Feel Something
- I Read the Book First: Tales of the Heart
- Disney+ Live Action Movies
- Letterboxd's Top 250 Horror
- The World of Attenborough

### Collections got a huge update
The Collections section received a major expansion with many new collections added and updated covers.

#### New collections include
- The Naked Gun
- Scary Movie
- The Hangover
- Men in Black
- Top Gun
- Jumanji
- Despicable Me
- Ice Age
- Madagascar
- Kung Fu Panda
- Sing
- Frozen
- The Lion King
- The Ring
- Silent Hill
- Insidious
- Johnny English
- Herbie
- The Last Airbender
- Planet of the Apes
- Deadpool
- Iron Man
- Guardians of the Galaxy
- The Avengers
- Mad Max

and many more.

### Discover changes
The Discover section was expanded from 5 to 7 entries.

#### Added
- Airing Soon
- Upcoming

### Genre / list cleanup
- Mindgame moved from Genres to Lists
- Seasonal catalog was removed

### Directors / Actors / Genres updates
#### Directors
- Greta Gerwig was added

#### Actors
Added:
- Jake Gyllenhaal
- Seth Rogen

#### Genres
Added:
- Stand-Up Comedy

### Regex / ranked icon overhaul
The regex system received a major upgrade in v3.0.

#### Ranked icons fully remade
- The regex ranked icons were completely redone and updated
- Visual consistency and overall quality were improved
- Improved regex patterns

#### Anime tier support expanded
Regex was updated to support the newer anime ranking structure:
- BluRay tiers up to T8
- WEBDL tiers up to T6

</details>

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
