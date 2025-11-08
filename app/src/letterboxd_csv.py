from dataclasses import dataclass, asdict
from typing import Optional

# Letterboxd diary CSV headers (exact, case-sensitive)
HEADERS = ["Date","Name","Year","Letterboxd URI","Rating","Rewatch","Tags","Review"]

@dataclass
class DiaryRow:
    Date: str
    Name: str
    Year: Optional[int] = None
    Letterboxd_URI: Optional[str] = None
    Rating: Optional[str] = None   # "0.5".."5" (step 0.5)
    Rewatch: str = ""              # "Yes" or ""
    Tags: str = ""
    Review: str = ""

    def as_csv_row(self) -> dict[str,str]:
        d = asdict(self)
        return {
            "Date": d["Date"],
            "Name": d["Name"],
            "Year": str(d["Year"]) if d["Year"] is not None else "",
            "Letterboxd URI": d["Letterboxd_URI"] or "",
            "Rating": d["Rating"] or "",
            "Rewatch": d["Rewatch"],
            "Tags": d["Tags"],
            "Review": d["Review"],
        }
