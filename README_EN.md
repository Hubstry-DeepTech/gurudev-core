# gurudev-core
# GuruDev Core · Powered by Hubstry-DeepTech

> **Language**: [Português](README.md) | **English** | [Bilingual Index](BILINGUAL_INDEX.md)

**GuruDev** is a holistic and ontological programming language, developed by the deep tech company **Hubstry-DeepTech**.
This repository contains the language core, including its grammar, interpreter, lexer, and conceptual architecture.

---

## 🌟 Vision

GuruDev integrates linguistics, artificial intelligence, epistemology, and software engineering to create a multimodal and semantic paradigm, aligned with the demands of the next generation of computational systems. Its unique syntax of ontological blocks, semantic annotations, and multilingual interoperability sets it apart from any other existing programming language.

---

## ✨ Current Project Status (May 2026)

The `gurudev-core` repository has undergone significant restructuring in 2025-2026, consolidating the technical foundation for continuous evolution. The following milestones have been achieved:

### Core Engineering
- **Refactored PLY Lexer**: State machine `ply.lex` with 9 dedicated lexical states (`pycode`, `jscode`, `rustcode`, `csharpcode`, `javacode`, `cppcode`, `gotocode`, `rubycode`, `codelang`), static rules (no dynamic `setattr`), and `module=_this_module` for correct token resolution.
- **Semantic Analyzer (Alexandria)**: Fixed critical bugs in `analyzer.py` (JSON path fallback, int-in-str conversion, file duplication).
- **Modern packaging**: Migration from `setup.py` to `pyproject.toml` with lightweight dependencies (`ply`, `click`, `rich`) and optional dependency groups.
- **CI/CD (GitHub Actions)**: Pipeline configured for Python 3.10-3.12 with `pip install -e .` and automated tests.

### Documentation & Governance
- **Bilingual README** (PT/EN), **CONTRIBUTING**, **FOUNDER_PROFILE**, **roadmap**, and **bilingual index**.
- **Financial modeling** with burn rate, runway, CAC, LTV, and net margin projections.
- **Revenue models** documented (SaaS, B2B, marketplace, licensing, etc.).
- **Whitepaper**, EBNF grammar, and articles on the GuruDev Processor published.

### Ecosystem
- **Alexandria**: Pioneering Comparative Programming library — analysis, translation, and type mapping across 15+ languages.
- **GuruDev Interactive Lexer**: Online MVP for real-time tokenization ([IA Manus](https://dyh6i3cqzgoz.manus.space/)).
- **Platform presence**: GitHub, Product Hunt, Google Colab, LinkedIn, Substack.

---

## 📂 Repository Structure

```
gurudev-core/
├── src/                  # Lexer, interpreter, and GuruDev compiler
│   └── lexer/            # PLY state machine (gurudev_lexer.py)
├── alexandria/           # Comparative Programming library
│   └── core/             # Analyzer, translator, type mapper
├── grammar/              # EBNF grammar definitions
├── examples/             # GuruDev example scripts
├── docs/                 # Whitepapers, technical documentation, pitch decks
├── tests/                # Automated tests
├── .github/workflows/    # CI/CD (GitHub Actions)
├── README.md             # Portuguese version
├── README_EN.md          # This file (English)
├── CONTRIBUTING.md       # Contribution guide
├── FOUNDER_PROFILE.md    # Founder profile
├── FINANCIAL_MODEL.md    # Financial modeling
├── REVENUE_MODELS.md     # Revenue models
├── roadmap.md            # Complete roadmap
└── LICENSE               # Apache 2.0 License
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/Hubstry-DeepTech/gurudev-core.git
cd gurudev-core

# Install in editable (development) mode
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

### Running the Lexer

```bash
python examples/run_example.py
```

### Tests

```bash
# Run tests with pytest
pytest tests/

# Or via CI/CD (GitHub Actions automatically on each push)
```

---

## 🔗 Official Links

- **Hubstry Website:** [www.hubstry.dev](https://www.hubstry.dev)
- **GuruDev Website:** [gurudev-tech.site](https://gurudev-tech.site)
- **GitHub Pages:** [marcabru-tech.github.io/gurudev-site](https://marcabru-tech.github.io/gurudev-site/)
- **Main Repository:** [github.com/Hubstry-DeepTech/gurudev-core](https://github.com/Hubstry-DeepTech/gurudev-core)
- **Product Hunt:** [producthunt.com/products/gurudev](https://www.producthunt.com/products/gurudev)
- **GuruDev Interactive Lexer:** [IA Manus Demo](https://dyh6i3cqzgoz.manus.space/)
- **EBNF Grammar (History):** [cxnvssbu.manus.space](https://cxnvssbu.manus.space/)

---

## 🔐 Security and Governance

This project is maintained under Hubstry-DeepTech's GitHub Enterprise infrastructure, utilizing:

- **GitHub Advanced Security** (Code Scanning, Secret Scanning)
- **Dependabot** for dependency management
- **GitHub Actions** for continuous integration and automated deployment
- **GitHub Enterprise** as official organization ([Hubstry-DeepTech](https://github.com/Hubstry-DeepTech))

---

## 🤝 Contribute

Your collaboration is welcome! Open issues for suggestions, bugs, or questions. Pull requests are carefully evaluated to ensure project integrity. Check the [Contribution Guide](CONTRIBUTING_EN.md) for details.

---

## 📞 Contact

- **Founder & CEO:** Guilherme Gonçalves Machado
- **Email:** guilhermemachado.ceo@hubstry.dev
- **Website:** [www.hubstry.dev](https://www.hubstry.dev)
- **Phone:** +55 (21) 96725-1593
- **LinkedIn:** [Guilherme Gonçalves Machado](https://linkedin.com/in/guilhermegmachado)
- **GitHub:** [@Hubstry-DeepTech](https://github.com/Hubstry-DeepTech)

---

## 📜 License

This project is licensed under the **Apache 2.0 License**.

Reprogram the world with semantics, intelligence, and resilience.

© Hubstry-DeepTech · All rights reserved.
