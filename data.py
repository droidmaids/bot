import json
from typing import List, Dict, Optional, Union


def get_films(file_path: str = "films.json", film_id: Optional[int] = None) -> Union[List[Dict], Dict]:
    with open(file_path, "r", encoding="utf-8") as fh:
        films = json.load(fh)

        if film_id != None and 0 <= film_id < len(films):
            return films[film_id]
        
        return films