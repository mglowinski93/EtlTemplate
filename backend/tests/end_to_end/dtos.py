from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework.test import APIClient

User = get_user_model()

@dataclass
class APIClientData:
    client: APIClient
    user: User  # type: ignore[valid-type]


@dataclass
class ClientData:
    client: Client
    user: User  # type: ignore[valid-type]
