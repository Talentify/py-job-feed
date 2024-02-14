from feed_generator.es_hit_formatters import ESHitFormatterABC


class DefaultESHitFormatter(ESHitFormatterABC):

    @staticmethod
    def source() -> [str]:
        return ["id",
                "description.common",
                "title",
                "location.*",
                "compensation.*",
                "type.*",
                "client.*",
                "urls.*",
                ]

    @staticmethod
    def format(es_hit):
        return es_hit
