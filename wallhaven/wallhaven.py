from plugins.base_plugin.base_plugin import BasePlugin
from utils.http_client import get_http_session
import logging
import random

logger = logging.getLogger(__name__)

WALLHAVEN_API_URL = "https://wallhaven.cc/api/v1/search"

class Wallhaven(BasePlugin):
    def generate_image(self, settings, device_config):
        logger.info("=== Wallhaven Plugin: Starting image generation ===")

        query      = settings.get('query', '')
        tags       = settings.get('tags', '')
        categories = settings.get('categories', '111')
        sorting    = settings.get('sorting', 'random')
        color      = settings.get('color', '')
        ratio      = settings.get('ratio', 'landscape')

        # Load API key from .env (set via API Keys page in web UI)
        api_key = device_config.load_env_key("WALLHAVEN_API_KEY")

        # Build purity string from checkboxes (e.g. "110" = SFW + Sketchy)
        sfw     = '1' if settings.get('purity_sfw') == '1' else '0'
        sketchy = '1' if settings.get('purity_sketchy') == '1' else '0'
        nsfw    = '1' if settings.get('purity_nsfw') == '1' else '0'
        purity  = sfw + sketchy + nsfw

        # Default to SFW if nothing selected
        if purity == '000':
            purity = '100'

        # NSFW requires an API key
        if nsfw == '1' and not api_key:
            raise RuntimeError("NSFW content requires a Wallhaven API key set in the API Keys page.")

        # Build combined query string — tags use #tagname syntax in Wallhaven
        query_parts = []
        if query:
            query_parts.append(query)
        if tags:
            for tag in [t.strip() for t in tags.split(',') if t.strip()]:
                query_parts.append(f"#{tag}")
        combined_query = ' '.join(query_parts)

        logger.info(f"Purity: {purity} | Categories: {categories} | Sorting: {sorting} | Ratio: {ratio} | Query: '{combined_query}'")

        params = {
            'sorting': sorting,
            'categories': categories,
            'purity': purity,
            'per_page': 24,
        }
        if combined_query:
            params['q'] = combined_query
        if color:
            params['colors'] = color
        if api_key:
            params['apikey'] = api_key
        if ratio and ratio != 'any':
            params['ratios'] = ratio

        try:
            session = get_http_session()

            # Fetch up to ~100 results across multiple pages, then pick randomly
            all_results = []
            for page in range(1, 5):  # pages 1–4 = up to 96 results (24 per page max)
                paged_params = dict(params, page=page)
                response = session.get(WALLHAVEN_API_URL, params=paged_params)
                response.raise_for_status()
                data = response.json()
                page_results = data.get('data', [])
                all_results.extend(page_results)
                # Stop early if we got fewer than a full page (no more results)
                if len(page_results) < 24:
                    break

            results = all_results
            if not results:
                raise RuntimeError("No wallpapers found for the given search parameters.")

            logger.info(f"Found {len(results)} wallpapers across up to 4 pages")
            selected = random.choice(results)
            image_url = selected['path']
            logger.info(f"Selected wallpaper: {image_url}")

        except RuntimeError:
            raise
        except Exception as e:
            logger.error(f"Wallhaven API error: {e}")
            raise RuntimeError("Failed to fetch wallpaper from Wallhaven, please check logs.")

        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        image = self.image_loader.from_url(image_url, dimensions, timeout_ms=40000)
        if not image:
            raise RuntimeError("Failed to load image, please check logs.")

        logger.info("=== Wallhaven Plugin: Image generation complete ===")
        return image
