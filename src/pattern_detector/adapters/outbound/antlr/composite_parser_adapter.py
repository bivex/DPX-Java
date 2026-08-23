"""Multi-language composite parser adapter supporting Java and Clojure."""

from __future__ import annotations

from pattern_detector.adapters.outbound.antlr.clojure_parser_adapter import ClojureAntlrParserAdapter
from pattern_detector.adapters.outbound.antlr.java_parser_adapter import JavaAntlrParserAdapter
from pattern_detector.domain.code_model import CodeModel, NamespaceModel
from pattern_detector.ports.outbound import ParserPort


class CompositeAntlrParserAdapter(ParserPort):
    """Automatically delegates parsing to the appropriate language parser based on file extension."""

    def __init__(self) -> None:
        self.java_parser = JavaAntlrParserAdapter()
        self.clojure_parser = ClojureAntlrParserAdapter()

    def parse_source(self, source_code: str, file_path: str = "") -> NamespaceModel:
        if file_path.endswith(".java"):
            return self.java_parser.parse_source(source_code, file_path=file_path)
        return self.clojure_parser.parse_source(source_code, file_path=file_path)

    def parse_sources(self, sources: dict[str, str]) -> CodeModel:
        model = CodeModel()
        for file_path, source_code in sources.items():
            ns = self.parse_source(source_code, file_path=file_path)
            model.add_namespace(ns)
        return model
