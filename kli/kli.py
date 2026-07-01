import sys

import requests


def main():
    intent = " ".join(sys.argv[1:])
    response = requests.post("http://localhost:8080/plan", json={"intent": intent})
    print(response.json())


if __name__ == "__main__":
    main()
