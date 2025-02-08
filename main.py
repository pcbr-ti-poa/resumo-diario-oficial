import os
from scrapers.PortoAlegreScraper import PortoAlegreScraper
from scrapers.BaseScraper import NoPdfFoundError, DeepSeekAPIError

if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")
    scraper = PortoAlegreScraper(api_key)
    try:
        success = scraper.run()
        print("Successfully processed Porto Alegre gazette")
    except NoPdfFoundError as e:
        print(f"⚠️  Warning: {str(e)}")
        exit(0)
    except DeepSeekAPIError as e:
        print(f"❌ Critical API error: {str(e)}")
        exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        exit(1)
