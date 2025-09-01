# Minimal Regex-based Named Entity Recognizer

from typing import Dict, List, Optional, Any
import re
import json

try:
    import yaml
except Exception:
    yaml = None

class RegexNER:
    """A small, deterministic regex-based NER.

    Patterns can be provided as a dict {ENTITY_TYPE: [pattern1, pattern2, ...]}
    or loaded from a YAML/JSON file with the same structure.
    """

    def __init__(self, patterns: Optional[Dict[str, List[str]]] = None, patterns_file: Optional[str] = None, flags: int = 0):
        if patterns_file is not None:
            patterns = self._load_patterns_file(patterns_file)
        self.flags = flags
        self.patterns = patterns or {}
        self._compiled = self._compile_patterns(self.patterns)

    def _load_patterns_file(self, path: str) -> Dict[str, List[str]]:
        if path.lower().endswith('.json'):
            with open(path, 'r', encoding='utf-8') as fh:
                return json.load(fh)
        else:
            if yaml is None:
                raise RuntimeError('pyyaml is required to load YAML pattern files. Install with: pip install pyyaml')
            with open(path, 'r', encoding='utf-8') as fh:
                return yaml.safe_load(fh) or {}

    def _compile_patterns(self, patterns: Dict[str, List[str]]):
        compiled = []  # list of tuples (entity_type, pattern_text, compiled_regex)
        for ent_type, pats in patterns.items():
            if isinstance(pats, str):
                pats = [pats]
            for p in pats:
                try:
                    cre = re.compile(p, self.flags)
                    compiled.append((ent_type, p, cre))
                except re.error:
                    # Skip invalid patterns but continue
                    continue
        return compiled

    def find_entities(self, text: str) -> List[Dict[str, Any]]:
        """Return list of matches: {type, text, start, end, pattern}

        Note: This implementation does not attempt to resolve overlapping matches.
        """
        results = []
        for ent_type, pat_text, cre in self._compiled:
            for m in cre.finditer(text):
                results.append({
                    'type': ent_type,
                    'text': m.group(0),
                    'start': m.start(),
                    'end': m.end(),
                    'pattern': pat_text
                })
        # Optionally, sort by start position
        results.sort(key=lambda x: x['start'])
        return results

    def add_pattern(self, entity_type: str, pattern: str):
        self.patterns.setdefault(entity_type, []).append(pattern)
        try:
            cre = re.compile(pattern, self.flags)
            self._compiled.append((entity_type, pattern, cre))
        except re.error:
            raise

    def save_patterns(self, path: str):
        if path.lower().endswith('.json'):
            with open(path, 'w', encoding='utf-8') as fh:
                json.dump(self.patterns, fh, indent=2)
        else:
            if yaml is None:
                raise RuntimeError('pyyaml is required to save YAML pattern files. Install with: pip install pyyaml')
            with open(path, 'w', encoding='utf-8') as fh:
                yaml.safe_dump(self.patterns, fh)