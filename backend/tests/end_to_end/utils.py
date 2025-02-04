from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def get_url(
    path_name: str, path_params: dict | None = None, query_params: dict | None = None
) -> str:
    url = reverse(viewname=path_name, kwargs=path_params)

    if query_params:
        url += "?" + urlencode(query_params)

    return url
