# Japanese Learning Subtitles Repository

This is the Kodi addon repository for Japanese Learning Subtitles. The repository is hosted using GitHub Pages and can be added to Kodi using the URL: `https://xpitfire.github.io/kodi-jap-subs`

## Repository Contents

- Japanese Learning Subtitles Addon (service.subtitles.jplearn)
  - Real-time Japanese subtitle generation
  - Romaji pronunciation
  - Word-by-word translations

## Installation

1. The repository is already created at `https://github.com/Xpitfire/kodi-jap-subs`
2. Enable GitHub Pages in repository settings:
   - Go to Settings → Pages
   - Set source to "main" branch
   - Set folder to / (root)
   - Save changes

## Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Xpitfire/kodi-jap-subs.git
   cd kodi-jap-subs
   ```

2. Add all the repository files:
   ```bash
   # Copy all provided files to their respective locations
   ```

3. Generate the repository files:
   ```bash
   python generate_repository.py
   ```

4. Push to GitHub:
   ```bash
   git add .
   git commit -m "Repository setup"
   git push
   ```

## Updating the Repository

When updating the addon:

1. Create a new zip file of the addon:
   ```bash
   zip -r service.subtitles.jplearn/service.subtitles.jplearn-1.0.0.zip service.subtitles.jplearn/
   ```

2. Update the version number in addon.xml
3. Run generate_repository.py to update addons.xml and addons.xml.md5
4. Push changes to GitHub

## License

MIT License - See LICENSE file for details