# Baixando discursos do Babel

1. Crie um arquivo `settings.ini` em `./src/parla/` com as seguintes variáveis:
```
[settings]

BABEL_API_URL = https://babel.labhackercd.leg.br/api/v1/
BABEL_SPEECH_TYPE_ID = 1
```

2. Para iniciar a coleta dos discursos, execute o seguinte comando: 
```bash
$ ./src/manage.py fetch_speeches
```

# Adicionando um novo algoritmo de análise dos discursos

1. Adicione o nome da nova análise no modelo `Analysis` em `./src/apps/nlp/models.py`;

2. Crie um arquivo com o nome do algoritmo em `./src/apps/nlp/nome_do_algoritmo.py` e implemente os métodos necessários para a análise.

3. Crie um método para gerar e salvar suas análises em `./src/apps/nlp/analysis.py`, o conteúdo do campo `data` deve ser em formato `json` com a seguinte estrutura para a visualização:
```json
{
  "memória": {
    "authors": {
      "7444": {
        "texts_count": 1,
        "texts": [
          {
            "300565": 1
          }
        ]
      }
    },
    "authors_count": 1
  },
  "incêndio": {
    "authors": {
      "7444": {
        "texts_count": 1,
        "texts": [
          {
            "300565": 1
          }
        ]
      }
    },
    "authors_count": 1
  },
  "rio": {
    "authors": {
      "7444": {
        "texts_count": 1,
        "texts": [
          {
            "300565": 1
          }
        ]
      }
    },
    "authors_count": 1
  },
  "museu": {
    "authors": {
      "7444": {
        "texts_count": 1,
        "texts": [
          {
            "300565": 1
          }
        ]
      }
    },
    "authors_count": 1
  },
}
```

4. Adicione o nome do novo algoritmo ao filtro do template em `src/templates/filter-modal.html`