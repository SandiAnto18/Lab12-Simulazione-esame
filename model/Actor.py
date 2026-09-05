from dataclasses import dataclass
"""date per data di nascita"""
from datetime import date

@dataclass
class Actor:
    """definisco gli attributi della classe Actor"""
    ActorID: int
    Name: str
    date_of_birth: date
      #serve a identificare in modo univoco ogni attore nel grafo."""
    def __hash__(self):
        return hash(self.ActorID)
      #mostro l'output con il solo Name dell'attore"""
    def __str__(self):
        return f"{self.Name}"