import os
import logging

from django.apps import AppConfig
from django.core.cache import cache
from django.db.utils import ProgrammingError

import requests

logger = logging.getLogger(__name__)

AGENT_URL = os.environ.get("AGENT_URL")

API_KEY = os.environ.get("AGENT_ADMIN_API_KEY", "")

class EmailVerificationConfig(AppConfig):
    name = "email_verification"

    def ready(self):

        # Hack to let the manage command to create the cache table through...
        try:
            cache.get("")
        except ProgrammingError:
            return
        # credential_definition_id="FUKLxsjrYSHgScLbHuPTo4:3:CL:29366:RegistreAccesVirtuelCQEN-0.1.23-flihp"
        if cache.get("credential_definition_id") is None:
            schema_body = {
                "schema_name": "CQENDroitAccesVirtuel",
                "schema_version": "0.1.22",
                "attributes": ["email", "time"],
            }
            schema_response = requests.post(f"{AGENT_URL}/schemas", headers={"x-api-key": API_KEY}, json=schema_body)

            logger.info(schema_response.text)

            schema_response_body = schema_response.json()
            schema_id = schema_response_body["schema_id"]

            credential_definition_body = {"schema_id": schema_id}
            credential_definition_response = requests.post(
                f"{AGENT_URL}/credential-definitions", headers={"x-api-key": API_KEY}, json=credential_definition_body
            )

            logger.info(credential_definition_response.text)

            credential_definition_response_body = credential_definition_response.json()
            credential_definition_id = credential_definition_response_body[
                "credential_definition_id"
            ]

            logger.info(f"cred def id: {credential_definition_id}")

            cache.set("credential_definition_id", credential_definition_id, None)
