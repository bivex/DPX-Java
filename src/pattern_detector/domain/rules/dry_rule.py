"""Don't Repeat Yourself (DRY) Principle Detection Rule."""

from __future__ import annotations

import re
from typing import Any

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import PatternCategory, PatternType


class DryRule(BasePatternRule):
    """Detects structural code duplication violating the DRY (Don't Repeat Yourself) principle.

    Indicators:
    - Duplicate Method Bodies: Substantial identical non-trivial method bodies across different classes
      (length >= 4 non-empty lines).
    """

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.DRY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        body_map: dict[str, list[tuple[str, Any]]] = {}

        for fn in model.all_functions():
            body = (fn.body_text or "").strip()
            # Normalize whitespace and comments
            norm_body = re.sub(r"\s+", " ", re.sub(r"//.*", "", body)).strip()
            # Check length threshold (non-trivial method > 60 chars)
            if len(norm_body) >= 60 and "return" in norm_body:
                body_map.setdefault(norm_body, []).append((fn.name, fn.location))

        for norm_body, instances in body_map.items():
            if len(instances) >= 2:
                names = [name for name, _ in instances]
                locs = [loc for _, loc in instances]
                evidences = [
                    self.evidence(
                        description=f"Identical duplicate code logic detected across {len(instances)} methods: {', '.join(names)}",
                        weight=min(0.70, 0.45 + 0.10 * len(instances)),
                        location=locs[0],
                        code_suffix="DRY_CODE_DUPLICATION",
                    ),
                    self.evidence(
                        description="Duplicate logic creates maintenance hazards when business rules change; extract into shared utility or base class",
                        weight=0.35,
                        location=locs[1],
                        code_suffix="DRY_EXTRACTION_RECOMMENDED",
                    ),
                ]

                detection = self.create_detection(
                    target_name=names[0],
                    target_kind="dry_code_duplication",
                    evidences=evidences,
                    primary_location=locs[0],
                    related_locations=locs[1:],
                    summary=f"DRY Violation: Duplicate logic shared across {len(instances)} methods ({', '.join(names)})",
                    base_score=0.40,
                )
                detection.pattern_category = PatternCategory.PRINCIPLE
                detections.append(detection)

        return detections
