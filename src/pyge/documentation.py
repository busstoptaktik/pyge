"""
Abstract base class for documentation elements, applicable to all register elements
"""

from abc import ABC

# This abstract base class defines the bare minimum to implement the
# action items recommended in comments CA-3, CA-4, CA-5, and CA-10
# from the 2024 ISO-19111 systematic review


class Documentation(ABC):
    """Blueprint for a bare minimum documentation metadata collection"""

    @property
    def item_name(self) -> str | None:
        """The name according to this register"""
        return None

    @property
    def brief(self) -> str | None:
        """One-line description of the item"""
        return None

    @property
    def description(self) -> str | None:
        """Long-form human readable description of the item"""
        return None

    @property
    def citation(self) -> str | None:
        """Clear text literature reference"""
        return None

    @property
    def general_citation(self) -> str | None:
        """Literature cross-reference to the information source table"""
        return None

    @property
    def authority(self) -> str | None:
        """The authority in charge of or publishing the item"""
        return None

    @property
    def crossref(self) -> list[str]:
        """Other names (in other registers) for the item"""
        return []
