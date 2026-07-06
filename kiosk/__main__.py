# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Klokwork AI Inc.

import uvicorn


def main() -> None:
    uvicorn.run("kiosk.server:app", host="127.0.0.1", port=8000, log_level="info")


if __name__ == "__main__":
    main()
