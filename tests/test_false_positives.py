"""Tests for verifying low false positive rate on ordinary, non-pattern Java code."""

from pattern_detector.adapters.outbound.antlr.java_parser_adapter import JavaAntlrParserAdapter
from pattern_detector.domain.rules import get_default_rules
from pattern_detector.domain.services.pattern_detector import PatternDetectorService
from pattern_detector.domain.value_objects import ConfidenceLevel, PatternType


def _scan_snippet(code_map: dict[str, str]):
    adapter = JavaAntlrParserAdapter()
    model = adapter.parse_sources(code_map)
    detector = PatternDetectorService(rules=get_default_rules())
    return detector.detect_all(model)


def test_plain_pure_math_and_string_utilities_have_zero_detections() -> None:
    code = """
    package com.example.utils;

    public class MathUtils {
        public static int add(int a, int b) {
            return a + b;
        }

        public static int multiply(int x, int y) {
            return x * y;
        }

        public static long factorial(int n) {
            if (n <= 1) return 1;
            return n * factorial(n - 1);
        }
    }
    """
    report = _scan_snippet({"MathUtils.java": code})

    # Pure standard utilities must not trigger any design patterns
    assert report.total_detections_count == 0


def test_plain_pojo_records_without_interfaces_not_flagged_as_lifecycle_or_strategy() -> None:
    code = """
    package com.example.models;

    public class PointDto {
        private int x;
        private int y;

        public PointDto(int x, int y) {
            this.x = x;
            this.y = y;
        }

        public int getX() { return x; }
        public int getY() { return y; }
    }
    """
    report = _scan_snippet({"PointDto.java": code})

    # Plain POJO without interfaces must not trigger Lifecycle/Strategy
    invalid_detections = [
        d for d in report.detections
        if d.pattern_type in (PatternType.LIFECYCLE_COMPONENT, PatternType.STRATEGY, PatternType.ADAPTER)
    ]
    assert len(invalid_detections) == 0


def test_string_helpers_with_make_or_create_name_not_flagged_as_factory() -> None:
    code = """
    package com.example.helpers;

    public class StringHelpers {
        public static String makeUppercase(String s) {
            return s.toUpperCase();
        }

        public static String createSlug(String title) {
            return title.toLowerCase().replace(" ", "-");
        }
    }
    """
    report = _scan_snippet({"StringHelpers.java": code})

    # Functions returning pure strings without record/class instantiations must not be factory methods
    factory_detections = [
        d for d in report.detections
        if d.pattern_type == PatternType.FACTORY_METHOD and d.confidence.level in (ConfidenceLevel.HIGH, ConfidenceLevel.VERY_HIGH)
    ]
    assert len(factory_detections) == 0
