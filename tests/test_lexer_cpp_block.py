"""Regressão: abertura e fechamento de bloco de código C++ no lexer.

As regras de fechamento do estado 'cppcode' usavam c++ sem escape.
Em Python 3.10 isso é um erro de regex ("multiple repeat"); em Python 3.11+
vira quantificador possessivo e a tag ?/c++? deixa de ser reconhecida.
"""

from src.lexer.gurudev_lexer import tokenize


def _types(source):
    return [tok.type for tok in tokenize(source)]


def test_cpp_block_opens_and_closes():
    source = '¿c++?\nint main() { return 0; }\n?/c++?'
    types = _types(source)
    assert types == ['CPP_START', 'FOREIGN_CODE_CONTENT', 'CPP_END']


def test_cpp_block_content_is_preserved():
    body = '\nstd::cout << "ola" << std::endl;\n'
    tokens = tokenize('¿c++?' + body + '?/c++?')
    content = [t for t in tokens if t.type == 'FOREIGN_CODE_CONTENT']
    assert len(content) == 1
    assert content[0].value == body


def test_cpp_close_tag_requires_literal_plus_signs():
    # '?/c?' não é tag de fechamento de C++: o bloco não pode fechar com ela.
    types = _types('¿c++?\nx;\n?/c?\n?/c++?')
    assert types[0] == 'CPP_START'
    assert types[-1] == 'CPP_END'
    assert types.count('CPP_END') == 1
