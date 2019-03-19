EXTRA_STOPWORDS = [
    'sr.', 'nesse', 'deputados', '``', "''", 'empresa', 'trabalhadores',
    'brasil', 'brasileiro', 'brasileira', 'sociedade', 'grandes', 'meios',
    'principal', 'deputada', 'nesta', 'valor', 'reais', 'representante',
    'brasileiros', 'necessidade', 'quero', 'ser', 'geral', 'todo', 'toda',
    'estar', 'ter', 'parlamentares', 'região', 'forma', 'parte', 'disso',
    'debate', 'entregar', 'nessa', 'nome', 'vez', 'quer', 'primeira', 'tema',
    'soberania', 'justamente', 'ponto', 'presentes', 'faz', 'futuro', 'podem',
    'maneira', 'falar', 'interesses', 'caso', 'espaço', 'entrega', 'deste',
    'mesma', 'negócio', 'existe', 'avançar', 'ano', 'diz', 'próprios',
    'criação', 'própria', 'dizendo', 'trazer', 'preocupação', 'ali', 'ficar',
    'desse', 'importância', 'senhor', 'queremos', 'poderia', 'ir', 'próprio',
    'área', 'segundo', 'acontece', 'sei', 'sabem', 'comum', 'mim', 'tratar',
    'obrigação', 'falando', 'discurso', 'muitas', 'acabou', 'falou', 'outro',
    'capacidade', 'força', 'querem', 'significa', 'serviço', 'dados', 'tentar',
    'ninguém', 'gente', 'ideia', 'deputadas', 'dentro', 'fazendo', 'mão',
    'época', 'uso', 'fiz', 'último', 'nenhum', 'números', 'alguma',
    'acreditamos', 'achamos', 'pagar', 'paga', 'conjunto', 'contentam',
    'lacunas', 'esperamos', 'digo', 'sente', 'logo', 'pesquisar', 'principais',
    'mudar', 'sequer', 'pagou', 'pagando', 'traz', 'desafio', 'concreto',
    'atende', 'tendo', 'aberto', 'curto', 'recebe', 'receber', 'décadas',
    'minutos', 'horas', 'segundos', 'motivo', 'posso', 'dando', 'entra',
    'volto', 'construir', 'algumas', 'passar', 'muita', 'nisso', 'deveria',
    'dá', 'construir', 'muito', 'longo', 'muitas', 'outras', 'existem',
    'conseguimos', 'precisamos', 'feita', 'mencionou', 'falei', 'cujo', 'hora',
    'dizia', 'venha', 'conseguindo', 'conseguir', 'votar', 'alguém', 'somente',
    'todas', 'fizemos', 'citar', 'saiba', 'boa', 'deveriam', 'acontecendo',
    'algo', 'apresentei', 'sabemos', 'outra', 'junto', 'daqui', 'aconteceu',
    'haver', 'sinto', 'preciso', 'muitos', 'minimamente', 'amanhã', 'ontem',
    'partir', 'objetivo', 'opinião', 'vivemos', 'discutindo', 'agradecemos',
    'utilizados', 'contra', 'dona', 'falta', 'possa', 'manhã', 'novas',
    'após', 'pessoas', 'fundamental', 'desses', 'devido', 'item', 'século',
    'domingo', 'sábado', 'presidente', ',', '.', '...', 'é', 'questão', 'art',
    'ordem', 'v.exa', ':', 'governo', 'sr', 'agência', 'aqui', 'vai', 'artigo',
    '§', 'neste', 'vamos', 'agora', "''", 'fazer', 'mesa', 'ainda', 'porque',
    'trata', 'estrutura', 'sobre', 'então', 'todos', 'obstrução', 'votação',
    'presença', 'deputados', 'vou', 'brasil', 'discutir', 'vigência',
    'regimento', 'momento', ';', 'dois', 'dessa', 'medida', 'proposta', 'casa',
    'matéria', 'queria', 'assim', 'possamos', 'microfone', 'certeza', 'hoje',
    'profissional', 'deixar', 'provisória', 'ora', 'base', 'importante',
    'fala', '!', 'aumento', 'inciso', 'sra.', 'talvez', 'cima', 'servir',
    'nunca', 'dias', 'deus', 'dei', 'entendemos', 'chega', 'possam', 'entendo',
    'poderá', 'celeridade', 'tirar', 'mista', 'fechou-se', 'lado', 'lido',
    'repassado', 'demais', 'venho', 'marcar', 'xiii', 'diálogo', 'podemos',
    'apenas', 'poder', 'efeitos', 'pode', 'acordo', 'solicitação', 'reflexão',
    '?', 'ausência', 'aprovada', 'lideranças', 'dizer', 'portanto', 'peço',
    'recolher', 'prática', 'pois', 'milhões', 'bilhões', 'melhoria',
    'atividade', 'claro', 'saber', 'dar', 'avanço', 'condições', 'desastre',
    'especialmente', 'exatamente', 'política', 'vezes', 'fazê-lo', 'têm',
    'derrubar', 'precisa', 'custo', 'necessária', 'cláusula', 'proposição',
    '-', 'palavra', 'tempo', 'segundos', 'fez', 'necessário', 'zero',
    'interesse', 'srs', 'sr', 'sras', 'sra', 'deputado', 'presidente', 'é',
    'nº', 's.a.', 'v.exa.', 'v.exa', '#', 'anos', 'º', 'exa', 'mesa', 'veto',
    'legislatura', 'sessão', 'maioria', 'seguinte', 'mandato', 'bilhões',
    'quilômetros', 'ª', 'parabéns', 'membros', 'convido', 'usual', 'biênio',
    'brasil', 'palavra', 'discussão', 'período', 'início', 'pronunciamento',
    'suplente', 'atividade', 'ação', 'ações', 'daqueles', 'diferenças',
    'pasta', 'milhares', 'srªs', 'emenda', 'àqueles', 'tamanha', 'mês',
    'km', 'modelo', 'tarefas', 'colegas', 'programa', 'voz', 'pronunciamento',
    'casa', 'sessão', 'deliberativa', 'solene', 'ordinária', 'extraordinária',
    'encaminhado', 'orador', 'divulgar', 'deputado', 'parlamentar', 'projeto',
    'proposta', 'requerimento', 'destaque', 'veto', 'câmara', 'senado',
    'congresso', 'país', 'estado', 'brasil', 'lei', 'novo', 'nova', 'política',
    'povo', 'voto', 'partido', 'liderança', 'bancada', 'bloco', 'líder',
    'lider', 'frente', 'governo', 'oposição', 'presença', 'presente',
    'ausência', 'ausencia', 'ausente', 'obstrução', 'registrar', 'aprovar',
    'rejeitar', 'rejeição', 'sabe', 'matéria', 'materia', 'questão', 'ordem',
    'emenda', 'sistema', 'processo', 'legislativo', 'plenário', 'pedir',
    'comissão', 'especial', 'permanente', 'apresentar', 'encaminhar', 'capaz',
    'encaminho', 'orientar', 'liberar', 'apoiar', 'situação', 'fato',
    'tempo', 'pauta', 'discutir', 'discussão', 'debater', 'retirar', 'atender',
    'colegas', 'autor', 'texto', 'medida', 'união', 'república', 'audiência',
    'audiencia', 'público', 'publico', 'reunião', 'agradecer', 'solicitar',
    'assistir', 'contrário', 'favorável', 'pessoa', 'comemorar', 'ato',
    'momento', 'diretora', 'possível', 'atenção', 'agradeço', 'naquele',
    'necessárias', 'presidenta', 'compromisso', 'geradas', 'primeiro', 'peço',
    'simplesmente', 'ideal', 'argumento', 'i', 'válido', 'envolvidos', 'nesse',
    'aspecto', 'existentes', 'normativo', 'irá', 'nada', 'melhor',
    'pouco', 'resolvermos', 'problema', 'postura', 'faltas', 'declara', '%',
    'dia', 'obrigado', 'agradeço', 'agradecido', 'população', 'maior', 'cada',
    'bem', 'mundo', 'desta', 'mil', 'sendo', 'outros', '$', '!', '@', '#', '&',
    '(', ')', 'r', 'sempre', 'além', 'semana', 'relação', 'onde', 'meio',
    'inclusive', 'lá', 'vem', 'menos', 'menor', 'qualquer', 'desde', 'ontem',
    'hoje', 'exemplos', 'exemplo', 'tão', 'fim', 'janeiro', 'fevereiro',
    'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro',
    'novembro', 'dezembro', 'alguns', 'durante', 'gostaria', 'três', 'conta',
    'feito', 'através', 'antes', 'depois', 'verdade', 'bom', 'quase', 'setor',
    'aí', 'disse', 'principalmente', 'final', 'vão', 'coisa', 'ver', 'sentido',
    'vários', 'nenhuma', 'quanto', 'infelizmente', 'felizmente', 'número',
    'duas', 'dois', 'tanto', 'acho', 'achar', 'enquanto', 'deve', 'apelo',
    'papel', 'últimos', 'faço', 'fazer', 'garantir', 'garantia', 'fica',
    'obrigado..', 'assunto', 'sido', 'vir', 'incrementar', 'central',
    'aproximado', 'aproximadamente', 'hipotética', 'hipotese', 'hipótese',
    'superiores', 'entende', 'pedido', 'oradora', 'tal', 'v.exas', 'favor',
    'vota', 'nº', 'srª', 'vista', 'sim', 'dito', 'tudo', 'obrigado', 'º',
    'profundamente', 'custódio', 'divulgado', 'características', 'perfeito',
    'começarmos', 'nomes', 'amigo', 'possibilidade', 'mensagem', 'come',
    'parabenizar', 'começar', 'hs', 'atendimento', 'povos', '¯', 'ocorreu',
    'entanto', 'diante', 'defender', 'dr.', '“', '”', '•', 'v.', './', 'és',
    'senhoras', 'senhores', 'tipo', 'várias', 'gerais', 'quais', 'dessas',
    'deu', 'havia', 'devem', 'enfim', 'apesar', 'passa', 'chegou', 'vêm',
    'parece', 'u', 'querido', 'deram', 'vendendo', 'deixa-me', 'abaixo',
    'naquela', 'inicialmente', 'ouvi', 'assumido', 'veio', 'atento', 'vi',
    'ouvir', 'entender', 'consigamos', 'debatendo', 'mostrar', 'v.sa', 'vejo',
    'nessas', 'diga', 'abra', 'mudando', 'graças', 'colocaram', 'irei',
    'nesses', 'vê-la', 'consigo', 'senão', 'faremos', '\-', 'colocar',
    'passado', 'revisão', 'esperarmos', 'outubro',
]

ONEGRAM_STOPWORDS = [
    'grande', 'nacional', 'são', 'e', 'de', 'das', 'dos', 'da', 'do',
    'cedo', 'urgência', 'equipe', 'produtos', 'serviços', 'pequeno', 'total',
    'podermos', 'consenso', 'popular', 'mérito', 'único', 'pública', 'escolha',
    'acesso', 'pilotos', 'trabalhar', 'ministério', 'países', 'combate',
    'estados', 'vida', 'cidade', 'municípios', 'histórico', 'defesa',
    'município', 'prefeito', 'ii', 'santa', 'vereadora', 'centro',
    'governador', 'código', 'apoio', 'exercício', 'categoria', 'campo', 'kit',
    'ministro', 'social', 'recursos', 'direito', 'empresas', 'comunicação',
    'democracia', 'tribuna', 'história', 'respeito', 'luta', 'oportunidade',
    'dinheiro', 'públicos', 'civil', 'qualidade', 'políticas', 'sociais',
    'registro', 'públicas', 'crescimento', 'responsabilidade', 'participação',
    'importantes', 'gestão', 'minas', 'cidades', 'lugar', 'problemas',
    'decisão', 'mulher', 'nobre', 'capital', 'aprovação', 'humanos',
    'internacional', 'senador', 'redução', 'realmente', 'realidade', 'plano',
    'partidos', 'conselho', 'posição', 'medidas', 'termos', 'divulgação',
    'econômico', 'federais', 'fiscal', 'emprego', 'maiores', 'rede', 'ruas',
    'regional', 'continuar', 'profissionais', 'sob', 'homens', 'político',
    'atual', 'nação', 'meses', 'grupo', 'áreas', 'fundo', 'iniciativa',
    'executivo', 'cerca', 'cidadão', 'prazo', 'homem', 'trabalhador',
    'órgãos', 'campanha', 'controle', 'mínimo', 'mundial', 'dúvida',
    'legislação', 'relatório', 'emendas', 'atividades', 'razão', 'resultado',
    'instituições', 'brasileiras', 'líderes', 'última', 'secretário',
    'precisam', 'criar', 'movimento', 'data', 'fazem', 'novos', 'casos',
    'ambiente', 'administração', 'distrito', 'pesquisa', 'relator',
    'cumprimento', 'causa', 'informações', 'evento', 'aliás', 'superior',
    'filho', 'tarde', 'caminho', 'dificuldades', 'risco', 'publicação',
    'sobretudo', 'coisas', 'obrigada', 'santo', 'solicito', 'cargos',
    'condição', 'próximo', 'secretaria', 'formação', 'penal', 'forte',
    'representa', 'aprovado', 'acima', 'políticos', 'setores', 'chegar',
    'espírito', 'prefeitos', 'grave', 'solução', 'governos', 'conhecimento',
    'espero', 'preço', 'mudança', 'instituto', 'tributária', 'amigos', 'levar',
    'diversos', 'municipal', 'dado', 'filhos', 'proteção', 'pagamento',
    'federação', 'entidades', 'br-', 'funcionários', 'média', 'organização',
    'veículos', 'difícil', 'patrimônio', 'marco', 'geração', 'diversas',
    'honra', 'aumentar', 'movimentos', 'idade', 'passou', 'inclusão',
    'responsável', 'única', 'busca', 'questões', 'operação', 'participar',
    'pequenos', 'ajudar', 'regime', 'vítimas', 'pior', 'orgulho', 'unidos',
    'embora', 'forças', 'inteiro', 'modo', 'simples', 'programas',
    'legislativa', 'caixa', 'leis', 'passada', 'cidadãos', 'dignidade',
    'associação', 'absolutamente', 'contribuição', 'trata-se', 'esforço',
    'representantes', 'fizeram', 'vereador', 'ficou', 'volta', 'quadro',
    'lembrar', 'concluir', 'votos', 'classe', 'atuação', 'médio', 'receita',
    'palavras', 'nível', 'encontro', 'milhão', 'diferente', 'local',
    'estaduais', 'constitucional', 'recurso', 'certamente', 'nossa', 'turno',
    'candidato', 'eleitores', 'eleito', 'governa', 'vá', 'voltar', 'divulgue',
    'governar', 'direção', 'inadmissível', 'peças', 'acúmulo', 'entristecido',
    'confiança', 'votado', 'votamos', 'vazio', 'juntamente', 'convidados',
    'lógico', 'si', 'chamada', 'salto', 'fale', 'mato', 'agendada', 'ganha',
    'ame', 'verde', 'amarela', 'entender', 'custa', 'federal', 'prefeitura',
    'estadual',
]
