def get_contacts(request):
    creds_blob = request.session.get(settings.HUBSPOT_OAUTH_CREDENTIALS_SESSION_KEY)

    if creds_blob:
        creds = client.OAuth2Credentials.from_json(creds_blob)

        if not creds.access_token_expired:
            get_query = {'property': ['country', 'hs_lead_status']}

            requests.get('{hapi_base}/{area}/{endpoint}/?{query}'.format(
                hapi_base='https://api.hubapi.com',
                area='/contacts/v1',
                endpoint='/lists/all/contacts/all',
                query=urllib.urlencode(get_query, do_seq=True),
            ), headers={
                'Authorization': 'Bearer {0}'.format(creds.access_token),
            })

    return shortcuts.redirect('hubspot_oauth')


if __name__ == "__main__":
    print get_contacts()