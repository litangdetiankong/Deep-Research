from __future__ import annotations

import re
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._skip:
            return
        t = " ".join((data or "").split())
        if t:
            self.parts.append(t)


def _html_to_text(html: str) -> str:
    parser = _TextExtractor()
    try:
        parser.feed(html)
        parser.close()
    except Exception:
        pass
    text = " ".join(parser.parts)
    return re.sub(r"\s+", " ", text).strip()


def fetch_url(url: str, max_chars: int = 2000, timeout_s: int = 8) -> str:
    """下载网页并抽正文。失败返回空字符串，不要抛到主流程。"""
    url = (url or "").strip()
    if not url.startswith(("http://", "https://")):
        return ""
    # 跳过明显不是文章页的
    if any(url.lower().endswith(ext) for ext in (".pdf", ".zip", ".png", ".jpg", ".mp4")):
        return ""

    req = Request(
        url,
        headers={"User-Agent": "Deep-Research/0.1 (local demo)"},
        method="GET",
    )
    try:
        with urlopen(req, timeout=timeout_s) as resp:
            ctype = (resp.headers.get("Content-Type") or "").lower()
            if ctype and "html" not in ctype and "text/" not in ctype and "xml" not in ctype:
                return ""
            raw = resp.read(500_000)  # 最多 500KB
        html = raw.decode("utf-8", errors="ignore")
    except (URLError, HTTPError, TimeoutError, ValueError, OSError) as e:
        print(f"[fetch_url] skip {url}: {e}")
        return ""

    text = _html_to_text(html)
    if len(text) < 80:
        return ""
    return text[:max_chars]