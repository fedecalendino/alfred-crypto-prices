import sys

from pyflow import Workflow

import coingecko
import formatters


def main(workflow):
    sort_by = "rank"
    sort_dir = "asc"

    args = workflow.args

    currency = workflow.env.get("CURRENCY", "USD")

    if not args:
        ids = workflow.env.get("FAVORITES", "").split("\n")
        coins = coingecko.get_coins(*ids, currency=currency)
        sort_by = "price_change"
        sort_dir = "desc"
    elif args == ["marketcap"]:
        coins = coingecko.get_coins(currency=currency)
    else:
        coins = coingecko.search(
            set(map(lambda arg: arg.lower().strip(), args)),
            currency=currency,
        )

    coins = sorted(
        coins,
        key=lambda c: c[sort_by],
        reverse=sort_dir == "desc",
    )

    for coin in coins:
        title = "{rank} · {symbol} [{price} {currency}]".format(
            rank=coin["rank"],
            symbol=coin["symbol"].upper(),
            name=coin["name"],
            price=formatters.price(coin["price"]),
            currency=currency.upper(),
        )

        subtitle = "24H: {change}".format(
            change=formatters.percent(coin["price_change"]),
        )

        workflow.new_item(
            title=title,
            subtitle=subtitle,
            arg=coin["price"],
        ).set_icon_url(
            url=coin["img"],
            filename=f"{coin['name']}.png".lower(),
        ).set_alt_mod(
            arg=coin["url"],
            subtitle="ATL: {price} / {change}".format(
                price=formatters.price(coin["atl"]),
                change=formatters.percent(coin["atl_change"]),
            ),
        ).set_cmd_mod(
            arg=coin["url"],
            subtitle="ATH: {price} / {change}".format(
                price=formatters.price(coin["ath"]),
                change=formatters.percent(coin["ath_change"]),
            ),
        )


if __name__ == "__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
