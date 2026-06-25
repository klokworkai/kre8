# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Klokwork AI Inc.


class KonnektError(Exception):
    def __init__(self, provider: str, model: str, task: str, message: str):
        self.provider = provider
        self.model = model
        self.task = task
        self.message = message
        super().__init__(f"[konnekt] {provider}/{model} ({task}): {message}")
