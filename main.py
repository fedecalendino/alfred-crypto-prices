# coding=utf-8

import sys

import coinmarketcap
from workflow import Workflow

import formatters
import util


def get_parameters(workflow):
    args = workflow.args

    if len(args) == 0:
        args = util.getenv("WATCHLIST").split(",")
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
        found = coinmarketcap.fetch()
    else:
        slugs, symbols, invalid = get_parameters(workflow)

        for value in invalid:
            workflow.add_item(
                title="{value} has an invalid format.".format(value=value),
                subtitle="Use '{lower}' to search as a slug or '{upper}' to search as a symbol.".format(
                    lower=value.lower(),
                    upper=value.upper()
                ),
                valid=False,
            )

        if invalid:
            return

        try:
            by_slug = coinmarketcap.fetch(slugs=slugs)
            by_symbol = coinmarketcap.fetch(symbols=symbols)

            found = by_slug + by_symbol
        except:
            workflow.add_item(
                title="Something went wrong.",
                subtitle="Check if you are using valid slugs from coinmarketcap.com.".format(
                    args=workflow.args,
                ).replace("u'", "'"),
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

        workflow.add_item(
            title=title,
            subtitle=subtitle,
            arg=currency["url"],
            icon=currency["img"],
            valid=True,
        )


if __name__ == u"__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
