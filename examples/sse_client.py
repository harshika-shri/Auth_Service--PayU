from __future__ import annotations

import urllib.request


def main() -> None:
    url = "http://127.0.0.1:8000/sse/stream"
    request = urllib.request.Request(url, headers={"Accept": "text/event-stream"})

    with urllib.request.urlopen(request) as response:
        for raw_line in response:
            line = raw_line.decode("utf-8", errors="ignore").rstrip()
            if line:
                print(line)


if __name__ == "__main__":
    main()
