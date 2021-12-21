import os

from workflow import web


BASE_URL = "https://pro-api.coinmarketcap.com/v1"
LISTING_URL = BASE_URL + "/cryptocurrency/listings/latest"
QUOTES_URL = BASE_URL + "/cryptocurrency/quotes/latest"

IMAGE_FILENAME = "/tmp/{id}.png"
IMAGE_URL = "https://s2.coinmarketcap.com/static/img/coins/128x128/{id}.png"


def fetch(currencies):
    api_key = os.getenv("COINMARKETCAP_API_KEY")

    if not api_key:
        raise ValueError("Missing COINMARKETCAP_API_KEY environment variable")

    headers = {
        "Accept": "application/json",
        "X-CMC_PRO_API_KEY": api_key,
    }

    if currencies is None:
        url = LISTING_URL

        params = {
            "convert": "USD",
            "limit": 20,
        }
    else:
        url = QUOTES_URL

        params = {
            "convert": "USD",
            "skip_invalid": "true",
            "symbol": ",".join(currencies),
        }

    response = web.get(url, headers=headers, params=params)
    response = response.json()["data"]

    data = []

    if isinstance(response, dict):
        currencies = response.values()
    else:
        currencies = response

    for currency in sorted(currencies, key=lambda c: c["cmc_rank"]):
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
                "img": get_image(currency["id"]),
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


def load_image(id_):
    filename = IMAGE_FILENAME.format(id=id_)
    return filename if os.path.isfile(filename) else None


def get_image(id_):
    filename = load_image(id_)

    if filename:
        return filename

    filename = IMAGE_FILENAME.format(id=id_)

    url = IMAGE_URL.format(id=id_)

    with open(filename, "wb") as f:
        f.write(web.get(url).content)

    return f.name
