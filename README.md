# ☕ DPX-Java: Pattern Scanner & Software Architecture Analyzer for Java

> **Hexagonal Architecture (Ports & Adapters) + Domain-Driven Design (DDD)** static analysis and software design pattern detection engine for **Java (Java 8 / 11 / 17 / 21+)** powered by **ANTLR4** grammar parsing.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?style=flat&logo=python)](https://www.python.org/)
[![Java](https://img.shields.io/badge/Java-8%20--%2021%2B-orange.svg?style=flat&logo=java)](https://openjdk.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Hexagonal%20%2B%20DDD-brightgreen.svg?style=flat)]()
[![ANTLR](https://img.shields.io/badge/Parser-ANTLR%204.13.2-red.svg?style=flat)](https://www.antlr.org/)
[![Tests](https://img.shields.io/badge/Tests-39%20passed%20(100%25)-success.svg?style=flat)]()
[![Code Style](https://img.shields.io/badge/Linter-Ruff%20%26%20Mypy%20Strict-black.svg?style=flat)]()
[![Rules](https://img.shields.io/badge/Supported%20Rules-35%20(23%20GoF%20%2B%2010%20SOLID%2FPrinciples%20%2B%202%20Arch)-orange.svg?style=flat)]()

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
                                      │  35 AnalysisRules │
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

## 📐 Supported Rules Catalog (35 Rules)

### 1. SOLID & Clean Code Principles (10 Rules)
| # | Principle | Category | Detection Strategy & Heuristics |
|---|---|---|---|
| 1 | **Single Responsibility (SRP)** | Principle | Detects God Object anti-patterns mixing multiple disparate concerns (>10 methods, high field counts, combining DB + HTTP + business logic). |
| 2 | **Open/Closed (OCP)** | Principle | Identifies fragile `instanceof` / `switch(type)` cascades vs praises polymorphic interface extension points. |
| 3 | **Liskov Substitution (LSP)** | Principle | Detects derived classes breaking parent contracts (e.g. throwing `UnsupportedOperationException`). |
| 4 | **Interface Segregation (ISP)** | Principle | Flags Fat Interfaces (>8 methods) and praises fine-grained Role Interfaces (1-3 cohesive methods). |
| 5 | **Dependency Inversion (DIP)** | Principle | Verifies constructor/field interface injection vs hardcoded `new ConcreteClass()` instantiations. |
| 6 | **Composition Over Inheritance** | Principle | Flags deep inheritance trees (depth $\ge$ 3) and recommends composition/delegation. |
| 7 | **Law of Demeter (LoD)** | Principle | Detects train-wreck chained calls (`a.getB().getC().getD().run()`) causing tight structural coupling. |
| 8 | **High Cohesion & Low Coupling** | Principle | Evaluates package fan-out efferent coupling metrics to enforce modularity. |
| 9 | **Keep It Simple, Stupid (KISS)** | Principle | Detects high cyclomatic complexity and methods with long parameter lists ($\ge$ 6 parameters). |
| 10 | **Don't Repeat Yourself (DRY)** | Principle | Detects identical and near-duplicate non-trivial method bodies across classes. |

### 2. Gang of Four (GoF) Patterns (23 Rules)
| # | Pattern Type | Category | Detection Strategy & Java OOP Idioms |
|---|---|---|---|
| 11 | **Singleton** | Creational | `private static final ... INSTANCE = new ...();`, `getInstance()` accessor. |
| 12 | **Factory Method** | Creational | Factory creator classes or methods (`createButton`, `buildWidget`, `makeRequest`). |
| 13 | **Abstract Factory** | Creational | Factory interfaces (`GUIFactory`) declaring families of product creation methods. |
| 14 | **Builder** | Creational | Fluent step methods (`withHost`, `setPort`, `withSsl`) returning `this` / `Builder` and terminal `build()`. |
| 15 | **Prototype** | Creational | `implements Cloneable`, `clone()` methods, or copy constructors producing variants. |
| 16 | **Adapter** | Structural | Wrapper classes implementing a target interface and holding an adaptee reference. |
| 17 | **Decorator** | Structural | Classes implementing an interface and wrapping another instance of the same interface. |
| 18 | **Facade** | Structural | Service facade classes coordinating access to multiple subsystem dependencies. |
| 19 | **Composite** | Structural | Component interface implemented by Leaf elements and Composite container classes with `List<Component>`. |
| 20 | **Bridge** | Structural | Abstraction classes holding injected backend driver interfaces (`DatabaseDriver`). |
| 21 | **Proxy** | Structural | Surrogate classes controlling access / caching / logging, or dynamic proxies. |
| 22 | **Flyweight** | Structural | Object pools with `Map<Key, Value> cache` sharing fine-grained immutable instances. |
| 23 | **Observer** | Behavioral | Listener/Observer interfaces (`EventListener`), subscription methods, and event dispatching. |
| 24 | **Strategy** | Behavioral | Strategy interfaces with 2+ interchangeable concrete class implementations. |
| 25 | **Chain of Responsibility** | Behavioral | Handler pipelines with `setNext(Handler next)` / `next.handle(request)` delegation. |
| 26 | **Template Method** | Behavioral | Abstract classes with template execution methods delegating to abstract/protected step hooks. |
| 27 | **Command** | Behavioral | `Command` interface (`execute()`, `undo()`) with concrete command action classes. |
| 28 | **State** | Behavioral | State interface with concrete state classes and Context delegating state transitions. |
| 29 | **Iterator** | Behavioral | Custom classes implementing `java.util.Iterator<T>` or `java.lang.Iterable<T>`. |
| 30 | **Mediator** | Behavioral | Centralized mediator / event broker classes (`EventBroker`) decoupling components. |
| 31 | **Memento** | Behavioral | State snapshot classes (`Memento`) with `saveStateToMemento()` and `restoreState()`. |
| 32 | **Visitor** | Behavioral | Visitor interface with `visit(ElementA a)`, `visit(ElementB b)` and `Element.accept(Visitor v)`. |
| 33 | **Interpreter** | Behavioral | Grammar expression interfaces (`Expression`) with `interpret(Context ctx)`. |

### 3. Architectural Rules (2 Rules)
| # | Pattern Type | Category | Detection Strategy |
|---|---|---|---|
| 34 | **Lifecycle Component** | Architectural | Deterministic component lifecycles (`start()`, `stop()`). |
| 35 | **Circular Dependency** | Architectural | Package graph analysis detecting cyclic dependencies (`pkg A ➔ pkg B ➔ pkg A`). |

---

## 💻 CLI Usage Guide

```bash
# 1. Scan a Java project directory
uv run pattern-detector scan path/to/java/project

# 2. Export to interactive color-coded HTML dashboard
uv run pattern-detector scan path/to/java/project --html reports/dashboard.html
open reports/dashboard.html

# 3. Filter by confidence threshold or pattern
uv run pattern-detector scan path/to/java/project --min-confidence 0.70 --pattern srp

# 4. View registered rules catalog (all 35 rules)
uv run pattern-detector rules

# 5. Run test suite
uv run pytest -v
```

---

## 🧪 Quality & Verification

```bash
uv run pytest --cov=pattern_detector -v
uv run ruff check .
uv run mypy src/pattern_detector
```

* **Test Suite:** `39 / 39 PASSED` (100% pass rate).
* **Linter:** `ruff` (0 errors).
* **Static Typing:** strict `mypy` compliant.

---

## 🌐 The DPX Suite Family

Cross-language architectural static analysis across all modern programming languages:

| Repository | Language / Ecosystem | Primary Paradigms & Focus |
|---|---|---|
| **[`DPX-Yul`](https://github.com/bivex/DPX-Yul)** | **Yul / EVM Assembly** (0.8.x - 0.8.28+ / Cancun) | **Memory Management, Storage Packing, Transient Storage (EIP-1153), GoF 23** |
| **[`DPX-Cairo`](https://github.com/bivex/DPX-Cairo)** | **Cairo** (Cairo 1.0 - 2.8+ / Starknet) | **Components, Storage Mapping, Syscalls, Account Abstraction, Upgrades, GoF 23** |
| **[`DPX-Move`](https://github.com/bivex/DPX-Move)** | **Move** (Move 2024 / Aptos / Sui) | **Linear Resources, Abilities, Sui Objects, Hot Potato, Prover, GoF 23** |
| **[`DPX-Lua`](https://github.com/bivex/DPX-Lua)** | **Lua / Luau** (5.1 - 5.4 / LuaJIT) | **Metatable OOP, Coroutines, LuaJIT FFI, GameDev (Roblox/Neovim), GoF 23** |
| **[`DPX-Solidity`](https://github.com/bivex/DPX-Solidity)** | **Solidity** (0.8.x - 0.8.28+) | **EVM Gas Optimization, Proxies, CEI Reentrancy, Yul, GoF 23, Security** |
| **[`DPX-Zig`](https://github.com/bivex/DPX-Zig)** | **Zig** (0.11 - 0.14+) | **Comptime Generics, Allocator RAII, Defer Cleanup, SIMD, GoF 23** |
| **[`DPX-Gleam`](https://github.com/bivex/DPX-Gleam)** | **Gleam** (1.0 - 1.8+) | **Type-Safe OTP Actors, Algebraic Data Types, Railway Monads, GoF 23** |
| **[`DPX-Mojo`](https://github.com/bivex/DPX-Mojo)** | **Mojo** (24.x - 25.x+) | **SIMD Vectorization, Ownership, Memory Safety, GoF 23, AI Acceleration** |
| **[`DPX-Julia`](https://github.com/bivex/DPX-Julia)** | **Julia** (1.6 - 1.11+) | **Multiple Dispatch, Holy Traits, Metaprogramming, Tasks, GoF 23** |
| **[`DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin)** | **Kotlin** (1.8 - 2.0+) | **Coroutines, Flow, Jetpack Compose, Multiplatform, GoF 23** |
| **[`DPX-Swift`](https://github.com/bivex/DPX-Swift)** | **Swift** (5.5 - 6.0+) | **Protocol-Oriented, Actor Concurrency, SwiftUI, ARC Safety** |
| **[`DPX-CSharp`](https://github.com/bivex/DPX-CSharp)** | **C#** (10 - 13 / .NET 8-9) | **Clean Architecture, CQRS MediatR, Channel Pipelines** |
| **[`DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript)** | **TypeScript / JavaScript** | **Hexagonal DI, Decorator Meta, Reactive Streams, React/NestJS** |
| **[`DPX-Rust`](https://github.com/bivex/DPX-Rust)** | **Rust** (Edition 2021/2024) | **Zero-Cost Abstractions, RAII Lifetimes, Typestate Pattern** |
| **[`DPX-Go`](https://github.com/bivex/DPX-Go)** | **Go** (1.18 - 1.24+) | **Goroutine Channels, CSP Concurrency, Pipeline Streaming** |
| **[`DPX-Py`](https://github.com/bivex/DPX-Py)** | **Python** (3.8 - 3.13+) | **Multi-Paradigm Hexagonal, Data Flow Engine, AsyncIO** |
| **[`DPX-Php`](https://github.com/bivex/DPX-Php)** | **PHP** (8.1 - 8.4+) | **Attribute-driven DDD, Fiber Concurrency, Laravel/Symfony** |
| **[`DPX-Haskell`](https://github.com/bivex/DPX-Haskell)** | **Haskell** (GHC 9.2 - 9.12+) | **Category Theory, Monad Transformers, Free Monads, Optics** |
| **[`DPX-OCaml`](https://github.com/bivex/DPX-OCaml)** | **OCaml** (4.14 - 5.3+ Multicore) | **Functor Modules, Effect Handlers, GADTs, Railway Monads** |
| **[`DPX-Elixir`](https://github.com/bivex/DPX-Elixir)** | **Elixir** (OTP 25 - 27+) | **GenServer, DynamicSupervisor, Actor Fault Tolerance** |
| **[`DPX-Erlang`](https://github.com/bivex/DPX-Erlang)** | **Erlang/OTP** (24 - 27+) | **OTP Behaviors, Supervision Trees, Message Passing** |
| **[`DPX-C`](https://github.com/bivex/DPX-C)** | **C** (C99 - C23) | **Opaque Structs, VTables, MISRA/CERT Safety, Arena Allocators** |
| **[`DPX-Cpp`](https://github.com/bivex/DPX-Cpp)** | **C++** (C++14 - C++20) | **CRTP, Policy-Based Design, RAII Memory Safety, ANTLR4 AST** |
| **[`DPX-Java`](https://github.com/bivex/DPX-Java)** | **Java** (17 - 23+) | **Virtual Threads, Spring Boot / Jakarta EE, GoF Patterns** |
| **[`DPX`](https://github.com/bivex/DPX)** | **Clojure** / Meta Engine | **Pure Functional, Multimethods, Homoiconic Macro Architecture** |
---

