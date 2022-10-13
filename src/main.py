import sys

from pyflow import Workflow

from src import coingecko, formatters


def main(workflow):
    sort_by = "rank"
    sort_dir = "asc"

    args = workflow.args

    if not args:
        ids = workflow.env.get("FAVORITES", "").split("\n")
        coins = coingecko.get_coins(*ids)
        sort_by = "price_change"
        sort_dir = "desc"
    elif args == ["marketcap"]:
        coins = coingecko.get_coins()
    else:
        coins = coingecko.search(set(map(lambda arg: arg.lower().strip(), args)))

    coins = sorted(
        coins,
        key=lambda c: c[sort_by],
        reverse=sort_dir == "desc",
    )

    for coin in coins:
        title = "{rank} · {symbol} [{price} USD]".format(
            rank=coin["rank"],
            symbol=coin["symbol"].upper(),
            name=coin["name"],
            price=formatters.price(coin["price"]),
        )

        subtitle = "24H: {change}".format(
            change=formatters.percent(coin["price_change"]),
        )

        workflow.new_item(
            title=title,
            subtitle=subtitle,
            arg=coin["price"],
            uid=coin["id"],
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
