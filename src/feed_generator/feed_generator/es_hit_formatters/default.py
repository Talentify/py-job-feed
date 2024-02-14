from feed_generator.es_hit_formatters import ESHitFormatterABC


class DefaultESHitFormatter(ESHitFormatterABC):

    @staticmethod
    def source() -> [str]:
        return ["urls.cover",
                "description.common",
                "client.name",
                "location.is_remote",
                "location.city_name",
                "location.region_name",
                "location.country_iso_code",
                "location.full_address",
                "compensation.to_display",
                "type.to_display",
                "title",
                ]

    @staticmethod
    def format(es_hit):
        return {
            "url": (es_hit.get("urls") or {}).get("cover"),
            "description": (es_hit.get("description") or {}).get("common"),
            "company": (es_hit.get("client") or {}).get("name"),
            "location":  es_hit.get("location"),
            "compensation": (es_hit.get("compensation") or {}).get("to_display"),
            "type": (es_hit.get("type") or {}).get("to_display"),
            "title": es_hit.get("title")
        }
