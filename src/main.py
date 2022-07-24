import sys

from pyflow import Workflow

import coinmarketcap
import formatters


def get_parameters(workflow):
    args = workflow.args

    if len(args) == 0:
        args = workflow.env.get("WATCHLIST", "").split(",")
    else:
        args = workflow.args

    slugs = []
    symbols = []
    invalid = []

    for arg in args:
        if arg.isupper():
            symbols.append(arg)
        elif arg.islower():
            slugs.append(arg)
        else:
            invalid.append(arg)

    return slugs, symbols, invalid


def main(workflow):
    if workflow.args == ["marketcap"]:
        found = coinmarketcap.fetch(workflow)
    else:
        slugs, symbols, invalid = get_parameters(workflow)

        for value in invalid:
            workflow.new_item(
                title=f"{value} has an invalid format.",
                subtitle="Use '{lower}' to search as a slug or '{upper}' to search as a symbol.".format(
                    lower=value.lower(),
                    upper=value.upper()
                ),
                valid=False,
            )

        if invalid:
            return

        try:
            by_slug = coinmarketcap.fetch(workflow, slugs=slugs)
            by_symbol = coinmarketcap.fetch(workflow, symbols=symbols)

            found = by_slug + by_symbol
        except:
            workflow.new_item(
                title="Something went wrong.",
                subtitle="Check if you are using valid slugs from coinmarketcap.com.",
                arg="https://coinmarketcap.com/coins/views/all/",
                valid=True,
            )

            return

    currencies = {}

    for currency in found:
        mc = currency["rank"]
        currencies[mc] = currency

    for rank in sorted(currencies.keys()):
        currency = currencies[rank]
        price = currency["price"]

        title = "[{rank}. {symbol}] {price} USD".format(
            rank=currency["rank"],
            symbol=currency["symbol"],
            name=currency["name"],
            price=formatters.price(price),
        )

        subtitle = u"[hour: {hour}] • [day: {day}] • [week: {week}]".format(
            hour=formatters.percent(currency["changes"]["h"]),
            day=formatters.percent(currency["changes"]["d"]),
            week=formatters.percent(currency["changes"]["w"]),
        )

        workflow.new_item(
            title=title,
            subtitle=subtitle,
            arg=currency["url"],
        ).set_icon_url(
            url=currency["img"],
            filename=f"{currency['name']}.png".lower(),
        )


if __name__ == u"__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
