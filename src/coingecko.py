from pycoingecko import CoinGeckoAPI

client = CoinGeckoAPI()


def get_coins(*ids):
    for coin in client.get_coins_markets("usd", ids=",".join(ids), per_page=20):
        if not coin["market_cap_rank"]:
            coin["market_cap_rank"] = -1

        yield {
            "id": coin["id"],
            "symbol": coin["symbol"],
            "name": coin["name"],
            "rank": coin["market_cap_rank"],
            "img": coin["image"],
            "url": f'https://www.coingecko.com/en/coins/{coin["id"]}',
            "price": coin["current_price"],
            "price_change": coin["price_change_percentage_24h"],
            "atl": coin["atl"],
            "atl_change": coin["atl_change_percentage"],
            "ath": coin["ath"],
            "ath_change": coin["ath_change_percentage"],
        }


def search(symbols: set = None) -> list:
    ids = []

    for coin in client.get_coins_list():
        if coin["symbol"] in symbols:
            ids.append(coin["id"])

    return get_coins(*ids)
