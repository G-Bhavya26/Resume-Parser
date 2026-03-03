import json
import os
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

class SkillNormalizer:
    def __init__(self, taxonomy_path: str = "app/pipeline/taxonomy.json"):
        """Loads and indexes the skill taxonomy for fast O(1) synonym lookups."""
        self.taxonomy_path = taxonomy_path
        self._synonym_to_canonical: Dict[str, str] = {}
        self._canonical_to_metadata: Dict[str, dict] = {}
        
        self.load_taxonomy()

    def load_taxonomy(self):
        """Builds the internal lookup dictionaries."""
        if not os.path.exists(self.taxonomy_path):
             return # Skip if not created yet (e.g. testing)
             
        with open(self.taxonomy_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        def index_categories(categories):
             for cat_name, cat_data in categories.items():
                 # Handle direct skills like Python
                 if isinstance(cat_data, dict) and "aliases" in cat_data:
                     canonical = cat_name
                     self._canonical_to_metadata[canonical] = {
                         "type": "exact",
                     }
                     
                     # Map the canonical name itself
                     self._synonym_to_canonical[canonical.lower()] = canonical
                     
                     # Map all aliases to canonical
                     for alias in cat_data.get("aliases", []):
                         self._synonym_to_canonical[alias.lower()] = canonical
                         
                 # Handle nested children like JS -> React
                 if isinstance(cat_data, dict) and "children" in cat_data:
                      index_categories(cat_data["children"])
                      
                 # Handle categories with no properties, just lists of children
                 if isinstance(cat_data, dict) and not "aliases" in cat_data and not "children" in cat_data:
                      index_categories(cat_data)
        
        index_categories(data)
        
    def normalize(self, raw_skill: str) -> Tuple[str, bool]:
        """
        Normalizes a raw skill string to its canonical form.
        Returns (Normalized_Skill, Is_Known_In_Taxonomy).
        """
        clean_skill = raw_skill.strip()
        canonical = self._synonym_to_canonical.get(clean_skill.lower())
        
        if canonical:
             return canonical, True
        return clean_skill, False
