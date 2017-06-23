HUBSPOT_OAUTH_SECRET = 'credentials.json'
"""
Path to a JSON file containing a single object
{"client_id": "...", "client_secret": "..."},
where ID and secret are specific to your Hubspot app
(find them in your developer’s dashboard).
"""

HUBSPOT_OAUTH_SCOPES = ['deals']
"""
List of OAuth 2.0 scopes as string identifiers.
"""

HUBSPOT_OAUTH_CREDENTIALS_SESSION_KEY = 'hubspot_oauth_token'
"""
Key under which Django will store serialized access/refresh
credentials in ``request.session`` for later
authenticated API calls on behalf of the user.
"""