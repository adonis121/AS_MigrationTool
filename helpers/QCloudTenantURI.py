from urllib.parse import urlparse, urlunparse


def format_qcloud_tenant_uri(tenant: str) -> str:
    parsed_uri = urlparse(tenant)

    # Ensure the scheme is HTTPS
    scheme = 'https'

    # Set the port to 443
    netloc = parsed_uri.hostname
    if parsed_uri.port and parsed_uri.port != 443:
        netloc = f"{parsed_uri.hostname}:443"
    elif not parsed_uri.port:
        netloc = f"{parsed_uri.hostname}:443"

    # Reconstruct the URL with the updated scheme and port
    formatted_uri = urlunparse(
        (scheme, netloc, parsed_uri.path, parsed_uri.params, parsed_uri.query, parsed_uri.fragment))

    return formatted_uri


# Example usage
if __name__ == "__main__":
    tenant = "http://example.com/some/path"
    formatted_uri = format_qcloud_tenant_uri(tenant)
    print(formatted_uri)  # Output: https://example.com:443/some/path222
