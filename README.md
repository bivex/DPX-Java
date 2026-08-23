# ☕ DPX-Java: Pattern Scanner & Detector for Java

> **Hexagonal Architecture (Ports & Adapters) + Domain-Driven Design (DDD)** static analysis and software design pattern detection engine for **Java (Java 8 / 11 / 17 / 21+)** powered by **ANTLR4** grammar parsing.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?style=flat&logo=python)](https://www.python.org/)
[![Java](https://img.shields.io/badge/Java-8%20--%2021%2B-orange.svg?style=flat&logo=java)](https://openjdk.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Hexagonal%20%2B%20DDD-brightgreen.svg?style=flat)]()
[![ANTLR](https://img.shields.io/badge/Parser-ANTLR%204.13.2-red.svg?style=flat)](https://www.antlr.org/)
[![Tests](https://img.shields.io/badge/Tests-29%20passed%20(100%25)-success.svg?style=flat)]()
[![Code Style](https://img.shields.io/badge/Linter-Ruff%20%26%20Mypy%20Strict-black.svg?style=flat)]()
[![Patterns](https://img.shields.io/badge/Supported%20Patterns-25%20Rules%20(All%2023%20GoF%20%2B%20Architectural)-orange.svg?style=flat)]()

---

## 🏛 Architecture Overview

The system strictly follows **Domain-Driven Design (DDD)** and **Hexagonal Architecture (Ports & Adapters)**. The domain layer has **zero knowledge** of ANTLR, grammar tokens, AST implementation details, filesystem, or CLI frameworks.

```text
                    ┌────────────────────────────────────────────────────────┐
                    │                    Driving Adapters                    │
                    │                                                        │
                    │   Typer + Rich CLI         /       Python SDK API      │
                    └───────────────────────────┬────────────────────────────┘
                                                │
                                                ▼
                    ┌────────────────────────────────────────────────────────┐
                    │                   Application Layer                    │
                    │                                                        │
                    │     ScanningService (Pipeline Coordinator & Use Cases) │
                    └───────────────────────────┬────────────────────────────┘
                                                │
                                      ┌─────────▼─────────┐
                                      │    DOMAIN CORE    │
                                      │                   │
                                      │  CodeModel        │
                                      │  25 PatternRules  │
                                      │  Confidence Model │
                                      │  Evidence Trail   │
                                      │  Dependency Graph │
                                      └─────────┬─────────┘
                                                │
                    ┌───────────────────────────▼────────────────────────────┐
                    │                      Ports / SPI                       │
                    │                                                        │
                    │   Inbound:  ScannerPort, DetectorPort, ScanOptions     │
                    │   Outbound: ParserPort, SourceProviderPort,            │
                    │             ResultRepositoryPort, ReportFormatterPort  │
                    └───────────────────────────┬────────────────────────────┘
                                                │
                    ┌───────────────────────────▼────────────────────────────┐
                    │                    Driven Adapters                     │
                    │                                                        │
                    │   • ANTLR4 Java Parser (JavaLexer.g4 / JavaParser.g4)  │
                    │   • FileSystem Source Provider (.java recursive)       │
                    │   • Interactive HTML Dashboard Formatter & Repository  │
                    │   • GitHub-Flavored Markdown Formatter & Repository    │
                    │   • JSON Result Repository                             │
                    │   • Rich Console Terminal Formatter                    │
                    └────────────────────────────────────────────────────────┘
```

---

## 📐 Supported Design Patterns (All 23 GoF + 2 Architectural Rules)

| # | Pattern Type | Category | Detection Strategy & Java OOP Idioms |
|---|---|---|---|
| 1 | **Singleton** | Creational | `private static final ... INSTANCE = new ...();`, `getInstance()` accessor, or enum singletons. |
| 2 | **Factory Method** | Creational | Factory creator classes or methods (`createButton`, `buildWidget`, `makeRequest`) returning interface instances. |
| 3 | **Abstract Factory** | Creational | Factory interfaces (`GUIFactory`) declaring families of product creation methods implemented by concrete factory classes. |
| 4 | **Builder** | Creational | Fluent step methods (`withHost`, `setPort`, `withSsl`) returning `this` / `Builder` and terminal `build()`. |
| 5 | **Prototype** | Creational | `implements Cloneable`, `clone()` methods, or copy constructors producing variants from prototype instances. |
| 6 | **Adapter** | Structural | Wrapper classes implementing a target interface and holding an adaptee reference. |
| 7 | **Decorator** | Structural | Classes implementing an interface and wrapping another instance of the same interface (`super` / delegation). |
| 8 | **Facade** | Structural | High-level service facade classes coordinating and simplifying access to multiple subsystem dependencies. |
| 9 | **Composite** | Structural | Component interface implemented by both Leaf elements and Composite classes containing `List<Component>`. |
| 10 | **Bridge** | Structural | Abstraction classes holding injected backend driver interfaces (`DatabaseDriver`, `RendererDriver`). |
| 11 | **Proxy** | Structural | Surrogate classes implementing a target interface controlling access / caching / logging, or dynamic proxies. |
| 12 | **Flyweight** | Structural | Object pools with `Map<Key, Value> cache` sharing fine-grained immutable instances. |
| 13 | **Observer** | Behavioral | Listener/Observer interfaces (`EventListener`, `Observer`), subscription methods (`addListener`), and event notifications. |
| 14 | **Strategy** | Behavioral | Strategy interfaces with 2+ interchangeable concrete class implementations. |
| 15 | **Chain of Responsibility** | Behavioral | Handler pipelines with `setNext(Handler next)` / `next.handle(request)` sequential delegation. |
| 16 | **Template Method** | Behavioral | Abstract classes with template execution methods delegating to abstract/protected step hooks. |
| 17 | **Command** | Behavioral | `Command` interface (`execute()`, `undo()`) with concrete command action classes. |
| 18 | **State** | Behavioral | State interface with concrete state classes and Context delegating state transitions. |
| 19 | **Iterator** | Behavioral | Custom classes implementing `java.util.Iterator<T>` or `java.lang.Iterable<T>`. |
| 20 | **Mediator** | Behavioral | Centralized mediator / event broker classes (`EventBroker`, `Mediator`) decoupling component communication. |
| 21 | **Memento** | Behavioral | State snapshot classes (`Memento`) with `saveStateToMemento()` and `restoreState()`. |
| 22 | **Visitor** | Behavioral | Visitor interface with `visit(ElementA a)`, `visit(ElementB b)` and `Element.accept(Visitor v)`. |
| 23 | **Interpreter** | Behavioral | Grammar expression interfaces (`Expression`) with `interpret(Context ctx)` for AST tree evaluation. |
| 24 | **Lifecycle Component** | Architectural | System lifecycle contracts (`Lifecycle` / `SmartLifecycle` with `start()` and `stop()`). |
| 25 | **Circular Dependency** | Architectural | Static package analysis detecting cyclic dependencies (`package A ➔ package B ➔ package A`). |

---

## 💻 CLI Usage Guide

```bash
# 1. Scan a Java project directory
uv run pattern-detector scan path/to/java/project

# 2. Export to interactive color-coded HTML dashboard
uv run pattern-detector scan path/to/java/project --html dashboard.html
open dashboard.html

# 3. Filter by confidence threshold or pattern
uv run pattern-detector scan path/to/java/project --min-confidence 0.70 --pattern composite

# 4. View registered rules catalog
uv run pattern-detector rules

# 5. Run test suite
uv run pytest -v
```

---

## 🧪 Quality & Tests

```bash
uv run pytest --cov=pattern_detector -v
uv run ruff check .
uv run mypy src/pattern_detector
```

* **Test Suite:** `29 / 29 PASSED` (100% pass rate).
* **Linter:** `ruff` (0 errors).
* **Static Typing:** strict `mypy` compliant.
