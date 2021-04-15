def is_api_request(request):
    """Check if the request is consuming an API."""
    return "api" in request.path
