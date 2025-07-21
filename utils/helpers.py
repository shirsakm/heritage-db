# Utility functions and helpers

import logging
from typing import Any, List, Dict, Optional
from functools import wraps
from flask import request, jsonify

# Set up logging
logger = logging.getLogger(__name__)


def setup_logging(app) -> None:
    """
    Set up logging configuration for the application

    Args:
        app: Flask application instance
    """
    if not app.debug:
        # Production logging
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
        )
    else:
        # Development logging
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(name)s %(funcName)s:%(lineno)d %(message)s",
        )


def handle_errors(f):
    """
    Decorator for handling errors in route functions
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {e}")
            # In development, re-raise the error for debugging
            if logger.level == logging.DEBUG:
                raise
            # In production, return a generic error response
            return jsonify({"error": "An internal error occurred"}), 500

    return decorated_function


def get_request_params() -> Dict[str, Any]:
    """
    Extract and validate request parameters

    Returns:
        Dictionary of validated request parameters
    """
    return {
        "search_query": request.args.get("search", "").strip(),
        "selected_branches": request.args.getlist("branch"),
        "sort_by": request.args.get("sort_by"),
        "order": request.args.get("order", "desc"),
        "page": int(request.args.get("page", 1)),
        "per_page": int(request.args.get("per_page", 50)),
    }


def validate_batch(batch: str, available_batches: List[str]) -> bool:
    """
    Validate if the batch parameter is valid

    Args:
        batch: Batch year to validate
        available_batches: List of available batch years

    Returns:
        True if valid, False otherwise
    """
    return batch in available_batches


def sanitize_input(input_string: str, max_length: int = 100) -> str:
    """
    Sanitize user input to prevent XSS and other issues

    Args:
        input_string: Input string to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized string
    """
    if not input_string:
        return ""

    # Remove potentially dangerous characters
    sanitized = input_string.strip()[:max_length]

    # Basic XSS prevention
    sanitized = sanitized.replace("<", "&lt;").replace(">", "&gt;")

    return sanitized


def format_number(value: Any) -> str:
    """
    Format numeric values for display

    Args:
        value: Value to format

    Returns:
        Formatted string
    """
    try:
        num = float(value)
        if num == int(num):
            return str(int(num))
        return f"{num:.2f}"
    except (ValueError, TypeError):
        return str(value) if value is not None else "N/A"


class ResponseHelper:
    """Helper class for creating consistent API responses"""

    @staticmethod
    def success(data: Any, message: str = "Success") -> Dict[str, Any]:
        """Create a success response"""
        return {"status": "success", "message": message, "data": data}

    @staticmethod
    def error(message: str, error_code: str = "GENERIC_ERROR") -> Dict[str, Any]:
        """Create an error response"""
        return {"status": "error", "message": message, "error_code": error_code}

    @staticmethod
    def paginated(
        data: List[Any], page: int, per_page: int, total: int
    ) -> Dict[str, Any]:
        """Create a paginated response"""
        return {
            "status": "success",
            "data": data,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page,
            },
        }
