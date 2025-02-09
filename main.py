import pytz
from datetime import datetime
from config import settings
from core.exceptions import PDFNotFoundError, APIError
from core.summary_providers import OpenAiProvider
from scrapers.porto_alegre import PortoAlegreScraper
from utils.file_io import save_summary
from utils.mkdocs_helper import update_index


def main():
    try:
        # Initialize dependencies
        summary_provider = OpenAiProvider(settings.Settings.OPENAI_API_KEY)
        tz = pytz.timezone(settings.Settings.TIMEZONE)

        # Configure and run scraper
        scraper = PortoAlegreScraper(summary_provider, tz)
        target_date = datetime.now(tz).date()
        summary = scraper.run(target_date)

        # Save results and update documentation
        save_summary(summary, "porto_alegre", target_date)
        update_index()

        print("Successfully processed Porto Alegre gazette")

    except PDFNotFoundError as e:
        print(f"⚠️  Warning: {str(e)}")
    except APIError as e:
        print(f"❌ Critical API error: {str(e)}")
        exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()