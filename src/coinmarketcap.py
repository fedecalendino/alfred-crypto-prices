import requests


BASE_URL = "https://pro-api.coinmarketcap.com/v1"
LISTING_URL = BASE_URL + "/cryptocurrency/listings/latest"
QUOTES_URL = BASE_URL + "/cryptocurrency/quotes/latest"

IMAGE_URL = "https://s2.coinmarketcap.com/static/img/coins/128x128/{id}.png"


def fetch(workflow, slugs=None, symbols=None):
    api_key = workflow.env.get("COINMARKETCAP_API_KEY")

    if not api_key:
        raise ValueError("Missing COINMARKETCAP_API_KEY environment variable")

    headers = {
        "Accept": "application/json",
        "X-CMC_PRO_API_KEY": api_key,
    }

    if slugs:
        url = QUOTES_URL

        params = {
            "convert": "USD",
            "skip_invalid": "true",
            "slug": ",".join(slugs).lower(),
        }
    elif symbols:
        url = QUOTES_URL

        params = {
            "convert": "USD",
            "skip_invalid": "true",
            "symbol": ",".join(symbols).upper(),
        }
    elif slugs is None and symbols is None:
        url = LISTING_URL

        params = {
            "convert": "USD",
            "limit": 20,
        }
    else:
        return []

    response = requests.get(url, headers=headers, params=params)
    response = response.json()["data"]

    data = []

    if isinstance(response, dict):
        currencies = response.values()
    else:
        currencies = response

    for currency in currencies:
        quote = currency["quote"]["USD"]

        data.append(
            {
                "id": currency["id"],
                "marketcap": quote["market_cap"],
                "name": currency["name"],
                "price": quote["price"],
                "rank": currency["cmc_rank"],
                "symbol": currency["symbol"],
                "slug": currency["slug"],
                "img": IMAGE_URL.format(id=currency["id"]),
                "url": "https://coinmarketcap.com/currencies/{slug}/".format(
                    slug=currency["slug"],
                ),
                "changes": {
                    "h": quote["percent_change_1h"],
                    "d": quote["percent_change_24h"],
                    "w": quote["percent_change_7d"],
                },
            }
        )

    return data
