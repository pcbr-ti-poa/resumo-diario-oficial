class ScraperException(Exception):
    """Base exception for scraper-related errors"""
    pass

class PDFNotFoundError(ScraperException):
    """Raised when no PDF is found for the target date"""
    pass

class APIError(ScraperException):
    """Raised for API communication failures"""
    pass

class PDFProcessingError(ScraperException):
    """Raised during PDF content processing failures"""
    pass