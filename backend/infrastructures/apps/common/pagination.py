import urllib.parse as urlparse
from typing import Optional
from urllib.parse import urlencode

from rest_framework import serializers

from . import consts as common_consts


def make_paginated_response(
    url: str, count: int, offset: int, records_per_page: int, results: list[dict]
) -> serializers.Serializer:
    return PaginateSerializer(
        {
            common_consts.PAGINATION_COUNT_NAME: count,
            common_consts.PAGINATION_NEXT_LINK_NAME: _get_next_pagination_link(
                url, count, offset, records_per_page
            ),
            common_consts.PAGINATION_PREVIOUS_LINK_NAME: _get_previous_pagination_link(
                url, offset, records_per_page
            ),
            common_consts.PAGINATION_RESULTS_NAME: results,
        }
    )


def _get_next_pagination_link(
    url: str,
    records_count: int,
    offset: int,
    records_per_page: int,
) -> Optional[str]:
    link = None
    if records_count - records_per_page > offset:
        # More about adding query params to url:
        # https://stackoverflow.com/questions/2506379/add-params-to-given-url-in-python.
        params = {
            common_consts.PAGINATION_OFFSET_QUERY_PARAMETER_NAME: offset
            + records_per_page
        }
        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)  # type: ignore[arg-type]
        url_parts[4] = urlencode(query)
        link = urlparse.urlunparse(url_parts)

    return link


def _get_previous_pagination_link(
    url: str, offset: int, records_per_page: int
) -> Optional[str]:
    link = None
    if offset != 0 and records_per_page >= offset:
        link = (
            url.replace(
                f"{common_consts.PAGINATION_OFFSET_QUERY_PARAMETER_NAME}={offset}", ""
            )
            .rstrip("&")
            .rstrip("?")
        )
    elif records_per_page - offset < 0:
        link = url.replace(
            f"{common_consts.PAGINATION_OFFSET_QUERY_PARAMETER_NAME}={offset}",
            f"{common_consts.PAGINATION_OFFSET_QUERY_PARAMETER_NAME}={offset-records_per_page}",
        )

    return link


def __create_paginate_serializer():
    class Meta:
        fields = "_all_"

    attributes = {
        common_consts.PAGINATION_COUNT_NAME: serializers.IntegerField(),
        common_consts.PAGINATION_NEXT_LINK_NAME: serializers.URLField(allow_null=True),
        common_consts.PAGINATION_PREVIOUS_LINK_NAME: serializers.URLField(
            allow_null=True
        ),
        common_consts.PAGINATION_RESULTS_NAME: serializers.ListField(
            child=serializers.DictField()
        ),
        "Meta": Meta,
    }

    return type("PaginateSerializer", (serializers.Serializer,), attributes)


PaginateSerializer = __create_paginate_serializer()



