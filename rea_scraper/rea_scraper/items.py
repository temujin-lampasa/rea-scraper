# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from typing import List
from dataclasses import dataclass, fields
from rea_scraper.settings import CSV_SEP, LIST_SEP

@dataclass
class RealEstateListing:
    id: str
    title: str
    product: str
    daysActive: str
    hasTour: bool
    pdpUrl: str
    tenureType: str
    highlights: List[str]
    agencies: List[str]
    # Attributes
    area: str
    propertyTypes: List[str]
    carSpaces: str
    # Address
    state: str
    streetAddress: str
    postcode: str
    suburb: str
    suburbAddress: str
    # Details
    price: str
    # Sort
    searchCategory: str


    def __post_init__(self) -> None:
        """Clean field values.
        - join list of strings
        - strip csv separator
        """
        for field in fields(self):
            field_value = getattr(self, field.name)

            if isinstance(field_value, list):
                if len(field_value) == 0:
                    setattr(self, field.name, None)
                field_list_sep_removed = [string.replace(LIST_SEP, "") for string in field_value]
                field_csv_sep_removed = [string.replace(CSV_SEP, "") for string in field_list_sep_removed]
                setattr(
                    self, field.name,
                    LIST_SEP.join(field_csv_sep_removed)
                )
            if isinstance(field_value, str):
                setattr(self, field.name, field_value.replace(CSV_SEP, ""))

