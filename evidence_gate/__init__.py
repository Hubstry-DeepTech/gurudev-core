"""GuruDev Evidence Gate (MVP).

Um modelo de linguagem responde a uma pergunta sobre um texto-fonte e
lista afirmacoes, cada uma com a citacao literal que a sustenta. O
Python faz verificacoes deterministicas e uma politica GuruDev estatica
(politica.guru) decide o veredito:

    BLOQUEADO          algo falhou ou nao pode ser verificado
    VALIDADO_LITERAL   toda afirmacao e um trecho literal da fonte
    REVISAO_SEMANTICA  as citacoes existem, mas ha parafrase ou inferencia

VALIDADO_LITERAL nao prova que a fonte e verdadeira nem que a resposta
esta correta: prova apenas que cada afirmacao esta escrita na fonte.
"""

VEREDITOS = ("BLOQUEADO", "VALIDADO_LITERAL", "REVISAO_SEMANTICA")
