from urllib.parse import urlencode, urlparse, urlunparse


def build_utm_url(
    base_url: str,
    *,
    utm_source: str,
    utm_medium: str,
    utm_campaign: str,
    utm_content: str | None = None,
    utm_term: str | None = None,
) -> str:
    """Append UTM parameters to a base URL.

    Empty UTM values are omitted. If the base URL has no scheme, https:// is assumed.
    """
    base = base_url.strip()
    if not base:
        raise ValueError("base_url is required")

    if "://" not in base:
        base = f"https://{base}"

    parsed = urlparse(base)
    if not parsed.netloc:
        raise ValueError(f"Invalid base_url: {base_url}")

    params = {
        "utm_source": utm_source,
        "utm_medium": utm_medium,
        "utm_campaign": utm_campaign,
    }
    if utm_content:
        params["utm_content"] = utm_content
    if utm_term:
        params["utm_term"] = utm_term

    query = urlencode(params)
    return urlunparse(parsed._replace(query=query))
