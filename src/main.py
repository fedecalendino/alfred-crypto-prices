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
        sort_by = "change"
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
        price = coin["price"]

        title = "{rank} · {symbol} [{price} USD]".format(
            rank=coin["rank"],
            symbol=coin["symbol"].upper(),
            name=coin["name"],
            price=formatters.price(price),
        )

        subtitle = "24h change: {change}".format(
            change=formatters.percent(coin["change"]),
        )

        workflow.new_item(
            title=title,
            subtitle=subtitle,
            arg=coin["url"],
            uid=coin["id"],
        ).set_icon_url(
            url=coin["img"],
            filename=f"{coin['name']}.png".lower(),
        )


if __name__ == "__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
