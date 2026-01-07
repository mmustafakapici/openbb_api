"""
Data transformer service.

Transforms OpenBB data into mobile-optimized formats.
"""
from typing import Any, List, Optional
from datetime import datetime


class DataTransformer:
    """Transform data for mobile consumption."""

    @staticmethod
    def filter_fields(data: dict, fields: Optional[str]) -> dict:
        """
        Filter response fields based on comma-separated list.

        Args:
            data: Original data dict
            fields: Comma-separated field names

        Returns:
            Filtered dict
        """
        if not fields:
            return data

        field_list = [f.strip() for f in fields.split(",")]
        return {k: v for k, v in data.items() if k in field_list}

    @staticmethod
    def paginate_data(data: List[Any], page: int, limit: int) -> tuple:
        """
        Paginate data list.

        Args:
            data: List of items
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Tuple of (paginated_data, pagination_meta)
        """
        total = len(data)
        total_pages = (total + limit - 1) // limit
        start = (page - 1) * limit
        end = start + limit

        paginated = data[start:end]

        meta = {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }

        return paginated, meta

    @staticmethod
    def format_number(value: Any, decimals: int = 2) -> Optional[str]:
        """Format number for mobile display."""
        if value is None:
            return None

        try:
            num = float(value)
            if num >= 1_000_000_000:
                return f"{num / 1_000_000_000:.{decimals}f}B"
            elif num >= 1_000_000:
                return f"{num / 1_000_000:.{decimals}f}M"
            elif num >= 1_000:
                return f"{num / 1_000:.{decimals}f}K"
            else:
                return f"{num:.{decimals}f}"
        except (ValueError, TypeError):
            return None

    @staticmethod
    def format_percent(value: Any, decimals: int = 2) -> Optional[str]:
        """Format percentage for mobile display."""
        if value is None:
            return None

        try:
            num = float(value)
            return f"{num:.{decimals}f}%"
        except (ValueError, TypeError):
            return None

    @staticmethod
    def sanitize_for_mobile(data: dict) -> dict:
        """
        Sanitize dict for JSON serialization on mobile.

        Handles datetime, NaN, and other non-serializable types.
        """
        result = {}
        for key, value in data.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif value != value:  # NaN check
                result[key] = None
            elif value in (float('inf'), float('-inf')):
                result[key] = None
            else:
                result[key] = value
        return result


# Singleton instance
_data_transformer: Optional[DataTransformer] = None


def get_data_transformer() -> DataTransformer:
    """Get or create data transformer singleton."""
    global _data_transformer
    if _data_transformer is None:
        _data_transformer = DataTransformer()
    return _data_transformer
