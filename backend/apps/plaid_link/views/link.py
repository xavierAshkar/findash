from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

from apps.plaid_link.utils import get_plaid_client


@login_required
def create_link_token(request):
    client = get_plaid_client()

    link_request = LinkTokenCreateRequest(
        user=LinkTokenCreateRequestUser(
            client_user_id=str(request.user.id)
        ),
        client_name="Findash",
        products=[Products("transactions")],
        country_codes=[CountryCode("US")],
        language="en",
    )

    response = client.link_token_create(link_request)
    return JsonResponse(response.to_dict())
