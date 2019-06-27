
LIBRUSEC = 'librusec'
TAIGA_PROZA = 'taiga_proza'

WIKI = 'wiki'

LENTA = 'lenta'
RIA = 'ria'
TAIGA_FONTANKA = 'taiga_fontanka'
BURIY_NEWS = 'buriy_news'
BURIY_WEBHOSE = 'buriy_webhose'
ODS_GAZETA = 'ods_gazeta'
ODS_INTERFAX = 'ods_interfax'

CORPORA = [
    LIBRUSEC,
    TAIGA_PROZA,

    WIKI,

    LENTA,
    RIA,
    TAIGA_FONTANKA,
    BURIY_NEWS,
    BURIY_WEBHOSE,
    ODS_GAZETA,
    ODS_INTERFAX,
]


def corpus_read(args):
    texts = corpus_read_(args.name, args.path)
    for text in texts:
        print(text)


def corpus_read_(name, path):
    import corus

    functions = {
        LIBRUSEC: corus.load_librusec,
        TAIGA_PROZA: corus.load_taiga_proza,

        WIKI: corus.load_wiki,

        LENTA: corus.load_lenta,
        RIA: corus.load_ria,
        TAIGA_FONTANKA: corus.load_taiga_fontanka,
        BURIY_NEWS: corus.load_buriy_news,
        BURIY_WEBHOSE: corus.load_buriy_webhose,
        ODS_GAZETA: corus.load_ods_gazeta,
        ODS_INTERFAX: corus.load_ods_interfax
    }
    load = functions[name]
    records = load(path)
    for record in records:
        text = record.text

        # for malformed text like
        # Наиболее напряженная обстановка
        # наблюдалась
        # в Париже, где полиции неоднократно пришлось
        # применять водометы
        # , слезоточивый газ и резиновые пули.
        text = text.replace('\n', ' ')

        yield text
