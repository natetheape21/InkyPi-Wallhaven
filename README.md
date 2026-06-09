# InkyPi-Wallhaven

A [Wallhaven](https://wallhaven.cc) wallpaper plugin for [InkyPi](https://github.com/fatihak/InkyPi) — pulls random high-quality wallpapers from Wallhaven based on your search parameters and displays them on your e-ink screen.

## Features

- Search wallpapers by keyword, tags, category, and color
- Sorting options: Random, Relevance, Top List, Most Favorited, Date Added
- Orientation filter — landscape-only by default to prevent cropping on horizontal displays
- Color mode — display in full color, grayscale, or dithered black & white
- Content filtering: SFW, Sketchy, and NSFW (NSFW requires a free API key)
- Picks randomly from the top 96 results for higher quality images
- Works great in a playlist for automatic wallpaper rotation

## Installation

Run the following command on your Raspberry Pi:

```bash
inkypi plugin install wallhaven https://github.com/natetheape21/InkyPi-Wallhaven
```

Then restart InkyPi:

```bash
sudo systemctl restart inkypi
```

The **Wallhaven** plugin will appear in the InkyPi web UI.

## Settings

| Setting | Description |
|---|---|
| **Search Query** | Keywords to search for (e.g. `nature`, `space`, `cyberpunk`) |
| **Tags** | Comma-separated Wallhaven tags (e.g. `anime, landscape`) — combined with search query |
| **Sorting** | How to sort results — Random, Relevance, Top List, Favorites, Date Added |
| **Orientation Filter** | Landscape Only, Portrait Only, or Any — landscape is default to prevent cropping |
| **Categories** | General, Anime, People — or any combination |
| **Content Filter** | SFW, Sketchy, NSFW (checkboxes, mix and match) |
| **Color Mode** | Color (default), Grayscale, or Black & White (dithered) |
| **Color Filter** | Filter by dominant color |

## API Key (Optional)

An API key is only required for **NSFW** content.

1. Create a free account at [wallhaven.cc](https://wallhaven.cc)
2. Go to [Account Settings](https://wallhaven.cc/settings/account) and generate an API key
3. In the InkyPi web UI, go to **API Keys** and add:
   - Key: `WALLHAVEN_API_KEY`
   - Value: your API key

SFW and Sketchy content works without an API key.

## Usage

1. In the InkyPi web UI, click **Add Plugin** and select **Wallhaven**
2. Set your search parameters
3. Click **Update Now** to test
4. Add to a playlist with a refresh interval for automatic rotation

## Compatibility

- Tested on Raspberry Pi Zero W with Waveshare 7.3" E-Ink Spectra 6 display (800×480)
- Should work with any InkyPi-supported display

## License

MIT License — see [LICENSE](LICENSE) for details.
