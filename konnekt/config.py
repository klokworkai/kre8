# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Klokwork AI Inc.

from pydantic import BaseModel


class KonnektConfig(BaseModel):
    temperature: float = 0.2
    max_tokens: int = 2000
    timeout: int = 30
