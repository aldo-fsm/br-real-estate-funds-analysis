FUNDS_FILTERS = [
    {
        'label': 'Setor',
        'column': 'nome_setor',
        'type': 'multiselect',
    },
    {
        'label': 'Subsetor',
        'column': 'nome_subsetor',
        'type': 'multiselect',
    },
    {
        'label': 'Segmento',
        'column': 'segmento',
        'type': 'multiselect',
    },
    {
        'label': 'Tipo de Gestão',
        'column': 'tipo_gestao',
        'type': 'multiselect',
    },
    {
        'label': 'Divdend Yield (ult.12 meses)',
        'column': 'dividend_yield',
        'type': 'numeric-range',
    },
    {
        'label': 'P/VP',
        'column': 'p_vp',
        'type': 'numeric-range',
    },
    {
        'label': 'Val. Patrimonial p/cota',
        'column': 'valor_patrimonial_cota',
        'type': 'numeric-range',
    },
    {
        'label': 'Liquidez Média Diária',
        'column': 'liquidez_media_diaria',
        'type': 'numeric-range',
    },
    {
        'label': 'Percentual em Caixa',
        'column': 'percentual_caixa',
        'type': 'numeric-range',
    },
    {
        'label': 'Número de Cotistas',
        'column': 'numero_cotistas',
        'type': 'numeric-range',
    },
    {
        'label': 'Número de Cotas',
        'column': 'numero_cotas',
        'type': 'numeric-range',
    },
    {
        'label': 'Patrimônio Líquido',
        'column': 'patrimonio_liquido',
        'type': 'numeric-range',
    },
    {
        'label': 'Quantidade de Imóveis',
        'column': 'qtd_imoveis_renda_acabados',
        'type': 'numeric-range',
    },
    {
        'label': 'Máxima Fração de Receita por Imóvel',
        'column': 'max_percentual_receitas_imovel',
        'type': 'numeric-range',
        'help': 'Maior participação na receita dentre os imóveis do fundo (valor entre 0 e 1)'
    },
    {
        'label': 'Máxima Fração de Receita por Inquilino',
        'column': 'max_percentual_receitas_inquilino',
        'type': 'numeric-range',
        'help': 'Maior participação na receita dentre os inquilinos do fundo (valor entre 0 e 1)'
    },
    {
        'label': 'Quantidade de Inquilinos',
        'column': 'qtd_inquilinos',
        'type': 'numeric-range',
    },
]
