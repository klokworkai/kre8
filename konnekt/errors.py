# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Klokwork AI Inc.

from typing import Literal

ErrorCategory = Literal["no_creds", "invalid_secret_store", "invalid_api_keys"]


class KonnektError(Exception):
    def __init__(
        self,
        provider: str,
        model: str,
        task: str,
        message: str,
        category: ErrorCategory | None = None,
        category_breakdown: dict[str, ErrorCategory] | None = None,
    ):
        self.provider = provider
        self.model = model
        self.task = task
        self.message = message
        self.category = category
        self.category_breakdown = category_breakdown
        super().__init__(f"[konnekt] {provider}/{model} ({task}): {message}")
