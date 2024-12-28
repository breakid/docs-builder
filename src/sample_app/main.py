"""A sample application to demonstrate automatic code documentation."""

# Standard Libraries
from dataclasses import dataclass


@dataclass
class Context:
    """Stores contextual data about an object."""

    def __post_init__(self, **kwargs: str) -> None:
        """Normalizes and sanitizes attribute data."""

    def fetch(self) -> None:
        """Fetches data to populate attributes."""


@dataclass
class WebMetadata:
    """Defines a data class that stores OpenGraph metadata for a web page."""

    title: str
    url: str
    description: str
    image: str
