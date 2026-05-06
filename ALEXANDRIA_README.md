# Alexandria: Biblioteca de Interoperabilidade e Programação Comparada

> 🌐 **Language / Idioma**: **Português** | [English](ALEXANDRIA_README_EN.md) | [Índice Bilíngue](BILINGUAL_INDEX.md)

[![PyPI version](https://badge.fury.io/py/alexandria-lang.svg)](https://badge.fury.io/py/alexandria-lang)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🏛️ Sobre o Projeto

**Alexandria** é uma biblioteca pioneira que implementa os princípios da **Programação Comparada**, uma nova área acadêmica que estuda a interoperabilidade entre linguagens de programação através de análise comparativa sistemática.

### 🎯 Objetivos

- **Análise Comparativa**: Comparação sistemática entre linguagens de programação
- **Tradução Automática**: Conversão de código entre diferentes linguagens
- **Mapeamento de Tipos**: Mapeamento inteligente de tipos entre linguagens
- **Ponte Linguística**: Criação de bridges para interoperabilidade
- **Educação**: Ferramentas para ensino de programação comparada

## 👨‍💻 Autoria e Desenvolvimento

**Idealizador e Criador Principal:**
- **Guilherme Gonçalves Machado** - Idealizador do conceito de Programação Comparada
- **Hubstry-DeepTech** - Empresa desenvolvedora

**Desenvolvimento:**
- Criado com auxílio de Inteligência Artificial (Claude AI)
- Implementação em Python 3.8+
- Arquitetura modular e extensível

## 🚀 Instalação

```bash
pip install alexandria-lang
```

## 📖 Uso Básico

```python
from alexandria import LanguageAnalyzer, CodeTranslator, TypeMapper

# Análise comparativa
analyzer = LanguageAnalyzer()
comparison = analyzer.compare("Python", "Rust")
print(f"Similaridade: {comparison.similarity_score:.2f}")

# Tradução de código
translator = CodeTranslator()
result = translator.translate("def hello(): print('Hello')", "python", "javascript")

# Mapeamento de tipos
mapper = TypeMapper()
mappings = mapper.map_types("python", "rust")
```

## 🛠️ Funcionalidades

### 1. Análise Comparativa
- Comparação de paradigmas
- Análise de similaridade sintática
- Score de interoperabilidade
- Análise de famílias linguísticas

### 2. Tradução Automática
- Conversão entre 15+ linguagens
- Preservação de semântica
- Detecção de padrões
- Sugestões de otimização

### 3. Mapeamento de Tipos
- Mapeamento inteligente
- Detecção automática
- Sugestões contextuais
- Compatibilidade cross-language

### 4. CLI Interativo
```bash
alexandria compare python rust
alexandria translate --from python --to javascript code.py
alexandria map-types python rust
```

## 📊 Linguagens Suportadas

- **Imperativas**: C, C++, C#, Java, Go, Rust
- **Funcionais**: Haskell, Lisp, Clojure
- **Scripting**: Python, JavaScript, Ruby, Perl, Lua
- **Históricas**: COBOL, Fortran, Pascal, Assembly
- **Emergentes**: Zig, Jai, Carbon, Bend

## 🎓 Programação Comparada

Este projeto implementa os princípios da **Programação Comparada**, uma nova disciplina que:

- **Estuda** as relações entre linguagens de programação
- **Desenvolve** metodologias de interoperabilidade
- **Cria** ferramentas para análise comparativa
- **Educa** sobre diversidade linguística computacional

### Dodecálogo Gurudev (Princípios)

1. **Universalidade**: Todas as linguagens são válidas
2. **Interoperabilidade**: Comunicação entre paradigmas
3. **Educação**: Aprendizado através da comparação
4. **Inovação**: Evolução através da diversidade
5. **Acessibilidade**: Democratização do conhecimento
6. **Precisão**: Análise sistemática e rigorosa
7. **Flexibilidade**: Adaptação a diferentes contextos
8. **Colaboração**: Trabalho conjunto entre comunidades
9. **Sustentabilidade**: Desenvolvimento responsável
10. **Futuro**: Preparação para tecnologias emergentes
11. **Inclusão**: Acolhimento de todas as abordagens
12. **Excelência**: Busca pela qualidade técnica

## 🔧 Desenvolvimento

### Instalação para Desenvolvimento

```bash
git clone https://github.com/Hubstry-DeepTech/gurudev-core.git
cd gurudev-core
pip install -e .
pip install -r requirements.txt
```

### Testes

```bash
pytest tests/
make test
```

### Linting e Formatação

```bash
make lint
make format
```

## 📚 Documentação

- [Guia de Uso](docs/usage.md)
- [API Reference](docs/api.md)
- [Programação Comparada](research/programacao_comparada.md)
- [Exemplos](examples/)

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor, leia o [CONTRIBUTING.md](CONTRIBUTING.md) antes de contribuir.

### Como Contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- **Claude AI (Anthropic)** - Auxílio no desenvolvimento
- **Cursor (Anysphere)** - Auxílio no desenvolvimento e automação
- **Comunidade Python** - Ferramentas e bibliotecas
- **Academia** - Inspiração para Programação Comparada
- **Hubstry-DeepTech** - Suporte e infraestrutura

## 📞 Contato

- **Autor**: Guilherme Gonçalves Machado
- **Empresa**: Hubstry-DeepTech
- **Email**: guilhermemachado.ceo@hubstry.dev
- **GitHub**: [@Hubstry-DeepTech](https://github.com/Hubstry-DeepTech)

## 🌟 Roadmap

- [ ] Suporte a mais linguagens
- [ ] Interface gráfica
- [ ] Integração com IDEs
- [ ] Análise de performance
- [ ] Machine Learning para tradução
- [ ] API REST
- [ ] Cloud deployment

---

**Alexandria** - Conectando linguagens, unindo paradigmas, educando o futuro.

© 2025 Guilherme Gonçalves Machado & Hubstry-DeepTech. Todos os direitos reservados.