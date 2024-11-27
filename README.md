# Bell Media Downloader
### Allows you to search and download content from Crave and Noovo.


## Usage: `bell-media.py` [crave, noovo] help, connect, search, list, info, download [download options]

## Ways to Represent Seasons and Episodes:
- `noovo download "occupation double" s01e01`
- `crave download "occupation double/S01E01"` (NOT WORKING)
- `crave download "occupation double"` (Downloads entire series)
- `noovo download "occupation double" s01e01-s01e04` (Downloads all episodes from S1E1 to S1E4)
- `crave download "occupation double" s01` (Downloads entire season)
- `crave download "occupation double" s1-s3` (Downloads all episodes from season 1 to 3)
- `noovo download "occupation double" s1-s3e2` (Downloads all episodes from season 1 to season 3 episode 2)
- `crave download "occupation double e01"` (Downloads all episode 1 in a series) (NOT WORKING)

## Streaming Service Arguments:
- **noovo**
  Use Noovo
- **crave**
  Use Crave

## Positional Arguments:
- **help**
  Show this help message and exit

- **connect**  
  Connect using your Bell Media credentials (You need to enter your credentials in the `settings.json` file)
  
- **search**  
  Search for a show using its name (e.g., `search "occupation double"`). This will give back a list of shows that match the pattern

- **list**  
  Lists all the episodes available for a show using its name or its "url name" (e.g., `list occupation` OR `list occupation-double-mexique`)

- **info**  
  Gives all the information about a show using its name or its "url name" (e.g., `info occupation`)

- **download**  
  Download a show using its name or its "url name" (See the representation of the download commands)

## Download Options:
- `-r`  **Resolution** (e.g., `-r 1080` or `-r 720`)
- `-q`  **Quiet mode** (Don't display output in the terminal about what the program is doing.)
- `-ad` **Audiodescription** (Also downloads the audiodescription audio tracks)
- `-l`  **Latest Episode** (Downloads the latest episode that was available)
- `-s`  **Subtitles** (Downloads subtitles)