# 🤝 Guia de Contribuição — GuruDev® & Hubstry

Obrigado por seu interesse em contribuir para o ecossistema GuruDev® e a plataforma Hubstry! Este documento fornece diretrizes para contribuições efetivas e alinhadas com nossa visão de uma linguagem de programação ontológica e multissemiótica.

---

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Contribuir](#como-contribuir)
- [Tipos de Contribuição](#tipos-de-contribuição)
- [Processo de Desenvolvimento](#processo-de-desenvolvimento)
- [Padrões de Código](#padrões-de-código)
- [Documentação](#documentação)
- [Testes](#testes)
- [Comunicação](#comunicação)

---

## 📜 Código de Conduta

Este projeto adere aos princípios do **Dodecálogo GuruDev®**:

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

---

## 🚀 Como Contribuir

### 1. Preparação do Ambiente

```bash
# Clone o repositório
git clone https://github.com/Hubstry-DeepTech/gurudev-core.git
cd gurudev-core

# Instale as dependências
pip install -r requirements.txt
pip install -e .

# Configure o ambiente de desenvolvimento
make setup
```

### 2. Fluxo de Trabalho

1. **Fork** o repositório
2. **Clone** seu fork localmente
3. **Crie** uma branch para sua feature/correção
4. **Desenvolva** seguindo os padrões estabelecidos
5. **Teste** suas alterações
6. **Documente** as mudanças
7. **Commit** com mensagens descritivas
8. **Push** para seu fork
9. **Abra** um Pull Request

---

## 🎯 Tipos de Contribuição

### 🐛 Correção de Bugs
- Reporte bugs através de [Issues](https://github.com/Hubstry-DeepTech/gurudev-core/issues)
- Inclua informações detalhadas sobre reprodução
- Forneça logs e contexto do ambiente

### ✨ Novas Funcionalidades
- Discuta propostas em [Discussions](https://github.com/Hubstry-DeepTech/gurudev-core/discussions)
- Siga o processo de RFC para mudanças significativas
- Mantenha compatibilidade com a filosofia GuruDev®

### 📚 Documentação
- Melhore documentação existente
- Adicione exemplos práticos
- Traduza conteúdo (PT ↔ EN)
- Contribua com tutoriais

### 🧪 Testes
- Adicione testes para novas funcionalidades
- Melhore cobertura de testes existentes
- Teste em diferentes ambientes

### 🌐 Gramática e Linguagem
- Contribua para a gramática EBNF
- Proponha novos tokens ou construções
- Siga o [Guia de Contribuição para Gramática](docs/CONTRIBUICAO_GRAMATICA.md)

---

## 🔧 Processo de Desenvolvimento

### Branches
- `main`: Código estável e pronto para produção
- `develop`: Integração de novas funcionalidades
- `feature/*`: Desenvolvimento de funcionalidades específicas
- `hotfix/*`: Correções urgentes
- `docs/*`: Atualizações de documentação

### Commits
Siga o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```
tipo(escopo): descrição

[corpo opcional]

[rodapé opcional]
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Manutenção

**Exemplos:**
```
feat(lexer): adiciona suporte para tokens multissemióticos
fix(parser): corrige análise de expressões ontológicas
docs(readme): atualiza instruções de instalação
```

---

## 📏 Padrões de Código

### Python
- Siga [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) para formatação
- Use [isort](https://isort.readthedocs.io/) para imports
- Use [flake8](https://flake8.pycqa.org/) para linting

### Estrutura de Arquivos
```
gurudev-core/
├── src/                    # Código fonte principal
├── docs/                   # Documentação
├── tests/                  # Testes
├── examples/               # Exemplos de uso
├── research/               # Pesquisa e experimentação
└── alexandria/             # Biblioteca de interoperabilidade
```

### Nomenclatura
- **Classes**: `PascalCase`
- **Funções/Métodos**: `snake_case`
- **Constantes**: `UPPER_SNAKE_CASE`
- **Arquivos**: `snake_case.py`
- **Documentos**: `UPPER_SNAKE_CASE.md`

---

## 📖 Documentação

### Docstrings
Use o formato Google Style:

```python
def processar_semantica(texto: str, contexto: dict) -> dict:
    """Processa semântica de texto usando GuruMatrix 5D.
    
    Args:
        texto: Texto a ser processado
        contexto: Contexto semântico
        
    Returns:
        Resultado do processamento semântico
        
    Raises:
        SemanticError: Quando o processamento falha
    """
```

### Documentação Bilíngue
- Mantenha versões em português e inglês
- Use sufixo `_EN.md` para versões em inglês
- Inclua links de navegação bilíngue

---

## 🧪 Testes

### Estrutura de Testes
```
tests/
├── unit/                   # Testes unitários
├── integration/            # Testes de integração
├── fixtures/               # Dados de teste
└── conftest.py            # Configuração pytest
```

### Executando Testes
```bash
# Todos os testes
make test

# Testes específicos
pytest tests/unit/test_lexer.py

# Com cobertura
make test-coverage
```

### Padrões de Teste
- Use `pytest` como framework
- Mantenha cobertura > 80%
- Teste casos extremos
- Use fixtures para dados compartilhados

---

## 💬 Comunicação

### Canais Oficiais
- **GitHub Issues**: Bugs e solicitações de funcionalidades
- **GitHub Discussions**: Discussões gerais e propostas
- **Email**: guilhermemachado@hubstry.com
- **LinkedIn**: [Guilherme Gonçalves Machado](https://linkedin.com/in/guilhermegmachado)

### Processo de Review
1. **Automated Checks**: CI/CD deve passar
2. **Code Review**: Pelo menos um revisor aprovado
3. **Documentation**: Documentação atualizada
4. **Tests**: Testes passando e cobertura mantida

---

## 🏷️ Labels e Prioridades

### Labels de Issue
- `bug`: Correção necessária
- `enhancement`: Nova funcionalidade
- `documentation`: Melhoria de documentação
- `good first issue`: Ideal para iniciantes
- `help wanted`: Ajuda da comunidade desejada
- `priority:high`: Alta prioridade
- `priority:medium`: Média prioridade
- `priority:low`: Baixa prioridade

### Labels de PR
- `ready for review`: Pronto para revisão
- `work in progress`: Em desenvolvimento
- `needs changes`: Requer alterações
- `approved`: Aprovado para merge

---

## 🎓 Recursos para Contribuidores

### Documentação Técnica
- [Gramática EBNF](docs/GRAMMAR_V1_0_0_ALPHA.md)
- [Arquitetura de Namespaces](docs/ARQUITETURA_NAMESPACES.md)
- [Biblioteca Padrão](docs/BIBLIOTECA_PADRAO.md)
- [Formalização Matemática](docs/FORMALIZACAO_MATEMATICA.md)

### Exemplos e Tutoriais
- [Exemplos de Validação](docs/EXEMPLOS_VALIDACAO.md)
- [Programação Comparada](research/programacao_comparada.md)
- [Alexandria Library](ALEXANDRIA_README.md)

### Ferramentas de Desenvolvimento
- [Microsoft for Startups Founders Hub](https://foundershub.startups.microsoft.com/)
- [GitHub Education](https://education.github.com/)
- [Google Gemini Pro](https://gemini.google.com/)

---

## 🙏 Reconhecimento

Contribuidores são reconhecidos através de:
- Listagem no arquivo `CONTRIBUTORS.md`
- Menção em releases
- Badges de contribuição
- Convites para eventos da comunidade

---

## 📞 Suporte

Para dúvidas sobre contribuição:
- Abra uma [Discussion](https://github.com/Hubstry-DeepTech/gurudev-core/discussions)
- Entre em contato: guilhermemachado@hubstry.com
- Consulte a [documentação](docs/)

---

**Obrigado por contribuir para o futuro da programação ontológica e multissemiótica!**

© 2025 Hubstry-DeepTech · Todos os direitos reservados.