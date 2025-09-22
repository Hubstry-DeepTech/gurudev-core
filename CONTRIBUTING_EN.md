# 🤝 Contribution Guide — GuruDev® & Hubstry

Thank you for your interest in contributing to the GuruDev® ecosystem and Hubstry platform! This document provides guidelines for effective contributions aligned with our vision of an ontological and multisemiotic programming language.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Types of Contribution](#types-of-contribution)
- [Development Process](#development-process)
- [Code Standards](#code-standards)
- [Documentation](#documentation)
- [Testing](#testing)
- [Communication](#communication)

---

## 📜 Code of Conduct

This project adheres to the principles of the **GuruDev® Dodecalogue**:

1. **Universality**: All languages are valid
2. **Interoperability**: Communication between paradigms
3. **Education**: Learning through comparison
4. **Innovation**: Evolution through diversity
5. **Accessibility**: Democratization of knowledge
6. **Precision**: Systematic and rigorous analysis
7. **Flexibility**: Adaptation to different contexts
8. **Collaboration**: Joint work between communities
9. **Sustainability**: Responsible development
10. **Future**: Preparation for emerging technologies
11. **Inclusion**: Welcoming all approaches
12. **Excellence**: Pursuit of technical quality

---

## 🚀 How to Contribute

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/Hubstry-DeepTech/gurudev-core.git
cd gurudev-core

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Configure development environment
make setup
```

### 2. Workflow

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a branch for your feature/fix
4. **Develop** following established standards
5. **Test** your changes
6. **Document** the changes
7. **Commit** with descriptive messages
8. **Push** to your fork
9. **Open** a Pull Request

---

## 🎯 Types of Contribution

### 🐛 Bug Fixes
- Report bugs through [Issues](https://github.com/Hubstry-DeepTech/gurudev-core/issues)
- Include detailed reproduction information
- Provide logs and environment context

### ✨ New Features
- Discuss proposals in [Discussions](https://github.com/Hubstry-DeepTech/gurudev-core/discussions)
- Follow RFC process for significant changes
- Maintain compatibility with GuruDev® philosophy

### 📚 Documentation
- Improve existing documentation
- Add practical examples
- Translate content (PT ↔ EN)
- Contribute tutorials

### 🧪 Testing
- Add tests for new features
- Improve existing test coverage
- Test in different environments

### 🌐 Grammar and Language
- Contribute to EBNF grammar
- Propose new tokens or constructions
- Follow the [Grammar Contribution Guide](docs/CONTRIBUICAO_GRAMATICA_EN.md)

---

## 🔧 Development Process

### Branches
- `main`: Stable code ready for production
- `develop`: Integration of new features
- `feature/*`: Development of specific features
- `hotfix/*`: Urgent fixes
- `docs/*`: Documentation updates

### Commits
Follow the [Conventional Commits](https://www.conventionalcommits.org/) standard:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Refactoring
- `test`: Tests
- `chore`: Maintenance

**Examples:**
```
feat(lexer): add support for multisemiotic tokens
fix(parser): fix ontological expression analysis
docs(readme): update installation instructions
```

---

## 📏 Code Standards

### Python
- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting
- Use [isort](https://isort.readthedocs.io/) for imports
- Use [flake8](https://flake8.pycqa.org/) for linting

### File Structure
```
gurudev-core/
├── src/                    # Main source code
├── docs/                   # Documentation
├── tests/                  # Tests
├── examples/               # Usage examples
├── research/               # Research and experimentation
└── alexandria/             # Interoperability library
```

### Naming Conventions
- **Classes**: `PascalCase`
- **Functions/Methods**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Files**: `snake_case.py`
- **Documents**: `UPPER_SNAKE_CASE.md`

---

## 📖 Documentation

### Docstrings
Use Google Style format:

```python
def process_semantics(text: str, context: dict) -> dict:
    """Process text semantics using GuruMatrix 5D.
    
    Args:
        text: Text to be processed
        context: Semantic context
        
    Returns:
        Semantic processing result
        
    Raises:
        SemanticError: When processing fails
    """
```

### Bilingual Documentation
- Maintain versions in Portuguese and English
- Use `_EN.md` suffix for English versions
- Include bilingual navigation links

---

## 🧪 Testing

### Test Structure
```
tests/
├── unit/                   # Unit tests
├── integration/            # Integration tests
├── fixtures/               # Test data
└── conftest.py            # Pytest configuration
```

### Running Tests
```bash
# All tests
make test

# Specific tests
pytest tests/unit/test_lexer.py

# With coverage
make test-coverage
```

### Test Standards
- Use `pytest` as framework
- Maintain coverage > 80%
- Test edge cases
- Use fixtures for shared data

---

## 💬 Communication

### Official Channels
- **GitHub Issues**: Bugs and feature requests
- **GitHub Discussions**: General discussions and proposals
- **Email**: guilhermemachado@hubstry.com
- **LinkedIn**: [Guilherme Gonçalves Machado](https://linkedin.com/in/guilhermegmachado)

### Review Process
1. **Automated Checks**: CI/CD must pass
2. **Code Review**: At least one approved reviewer
3. **Documentation**: Updated documentation
4. **Tests**: Passing tests and maintained coverage

---

## 🏷️ Labels and Priorities

### Issue Labels
- `bug`: Fix needed
- `enhancement`: New feature
- `documentation`: Documentation improvement
- `good first issue`: Ideal for beginners
- `help wanted`: Community help desired
- `priority:high`: High priority
- `priority:medium`: Medium priority
- `priority:low`: Low priority

### PR Labels
- `ready for review`: Ready for review
- `work in progress`: Under development
- `needs changes`: Requires changes
- `approved`: Approved for merge

---

## 🎓 Resources for Contributors

### Technical Documentation
- [EBNF Grammar](docs/GRAMMAR_V1_0_0_ALPHA_EN.md)
- [Namespace Architecture](docs/ARQUITETURA_NAMESPACES_EN.md)
- [Standard Library](docs/BIBLIOTECA_PADRAO_EN.md)
- [Mathematical Formalization](docs/FORMALIZACAO_MATEMATICA_EN.md)

### Examples and Tutorials
- [Validation Examples](docs/EXEMPLOS_VALIDACAO_EN.md)
- [Comparative Programming](research/programacao_comparada_EN.md)
- [Alexandria Library](ALEXANDRIA_README_EN.md)

### Development Tools
- [Microsoft for Startups Founders Hub](https://foundershub.startups.microsoft.com/)
- [GitHub Education](https://education.github.com/)
- [Google Gemini Pro](https://gemini.google.com/)

---

## 🙏 Recognition

Contributors are recognized through:
- Listing in `CONTRIBUTORS.md` file
- Mention in releases
- Contribution badges
- Invitations to community events

---

## 📞 Support

For contribution questions:
- Open a [Discussion](https://github.com/Hubstry-DeepTech/gurudev-core/discussions)
- Contact: guilhermemachado@hubstry.com
- Check the [documentation](docs/)

---

**Thank you for contributing to the future of ontological and multisemiotic programming!**

© 2025 Hubstry-DeepTech · All rights reserved.