import json
from typing import List, Dict, Optional, Union


def get_films(file_path: str = "films.json", film_id: Optional[int] = None) -> Union[List[Dict], Dict]:
    with open(file_path, "r", encoding="utf-8") as fh:
        films = json.load(fh)

        if film_id is not None and 0 <= film_id < len(films):
            return films[film_id]
        
        return films
    
def add_film(film_data: Dict, file_path: str = "films.json") -> None:
    films = get_films()
    films.append(film_data)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(films, file, ensure_ascii=False, indent=2)