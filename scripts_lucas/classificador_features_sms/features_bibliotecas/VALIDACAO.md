# Validação da versão com bibliotecas

Data: 14/09/2026. Ambiente temporário com Python 3.12.8, macOS ARM64, CPU e OpenJDK 25.0.1. As dependências testadas estão em `validacao/dependencias_testadas.txt`; os ambientes e caches usados nos testes ficaram em `/tmp`, fora da pasta de entrega.

## Funcionamento verificado

- 13 testes da nova versão passaram. URLs, telefones e PIX foram testados com bibliotecas reais; NLI e LanguageTool foram simulados nos testes de contrato, filtragem e falhas.
- A avaliação adicional em `validacao/avaliacao_semantica.json` usou o modelo NLI real.
- A execução completa em `validacao/exemplo_execucao.json` usou o modelo final real e LanguageTool 6.8 local. Retornou as 24 features e identificou `bloquiada`, com sugestão `bloqueada`.
- Interface de terminal por módulo, ajuda por caminho direto e mensagem vazia verificadas.
- Os 6 testes originais passaram e os hashes SHA-256 confirmaram que nenhum arquivo Python original foi modificado.
- Todos os arquivos Python da nova pasta têm sintaxe válida e docstring explicativa.

## Avaliação semântica didática

Modelo final: `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`. Revisão: `8adb042d524ecd5c26d3e3ba0e3fbcf7e2d0864c`. Limiar: `0.7`. Escore de apoio com softmax sobre apoio, neutralidade e contradição.

**27 acertos em 38 casos; 11 divergências. A versão permanece experimental.** São apenas um exemplo positivo e um negativo para cada uma das 19 features semânticas. O conjunto foi usado para desenvolvimento e seleção do método; não é um teste independente e não mede generalização nem valida uso operacional.

A comparação inicial obteve 19/38 com MiniLM e 26/38 com mDeBERTa usando a normalização entre apoio e contradição, sem neutralidade. Preservar a classe neutra mudou o resultado para 27/38. Os limiares e as hipóteses não foram ajustados por exemplo. Os arquivos das comparações estão em `validacao/`; seus escores têm definição diferente dos escores finais.

### Divergências na versão final

| Feature | Esperado | Observado | Escore | Mensagem |
| --- | --- | --- | --- | --- |
| `solicita_codigo_autenticacao` | 1 | 0 | 0.3395 | Digite aqui o código de 6 números que você recebeu por SMS para confirmar sua conta. |
| `solicita_atualizacao_cadastro` | 0 | 1 | 0.9569 | Cadastro atualizado. |
| `solicita_clique` | 1 | 0 | 0.3286 | Clique no link abaixo para atualizar seu cadastro imediatamente. |
| `solicita_clique` | 0 | 1 | 0.7891 | https://exemplo.com |
| `solicita_ligacao` | 0 | 1 | 0.9883 | Telefone: (19) 99999-1234. |
| `carga_emocional` | 1 | 0 | 0.1752 | URGENTE!!! Você pode perder todo o seu dinheiro! Resolva AGORA antes que seja tarde!!! |
| `possui_urgencia` | 1 | 0 | 0.5721 | Regularize sua conta imediatamente. Você tem somente até hoje. |
| `possui_linguagem_alarmista` | 1 | 0 | 0.0158 | ALERTA MÁXIMO! Detectamos uma atividade suspeita em sua conta. Resolva imediatamente! |
| `possui_vantagem_inesperada` | 0 | 1 | 0.8702 | Seu salário foi depositado. |
| `possui_oferta_financeira` | 0 | 1 | 0.9118 | Seu dinheiro foi recebido. |
| `possui_chamada_acao` | 1 | 0 | 0.0771 | Informe seu CPF e clique no botão abaixo para confirmar. |

Os testes de funcionamento aprovados não anulam esses erros de classificação. Em especial, ainda existem confusões entre avisos e pedidos, entre benefício habitual e vantagem inesperada, e falhas em emoção, urgência e chamada à ação. Antes de rotular um dataset para uso real, revise as hipóteses com especialistas e avalie em SMS anotados independentemente. Para uma versão supervisionada especializada, são necessários rótulos humanos por feature e separação entre treino, validação e teste.
