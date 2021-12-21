# coding=utf-8

import os
import sys

import coinmarketcap
from workflow import Workflow


def error(title, subtitle=None):
    if subtitle:
        title = "{}: {}".format(title, subtitle)

    raise Exception(title)


def getenv(key):
    return os.getenv(key, "").upper().replace(" ", "").split(",")


def get_parameters(workflow):
    if len(workflow.args) == 0:
        return getenv("WATCHLIST")

    if len(workflow.args) == 1:
        if workflow.args[0] == "mc":
            return None

    return list(map(lambda symbol: symbol.upper(), workflow.args))


def main(workflow):
    currencies = get_parameters(workflow)

    for currency in coinmarketcap.fetch(currencies):
        price = currency["price"]

        if price < 0.01:
            formatted_price = "{:0.8f}".format(price)
        elif price < 1:
            formatted_price = "{:0.6f}".format(price)
        else:
            formatted_price = "{:0.2f}".format(price)

        title = "[{rank}. {symbol}] {price} USD".format(
            rank=currency["rank"],
            symbol=currency["symbol"],
            name=currency["name"],
            price=formatted_price,
        )
        subtitle = "1H={h:0.2f}% | 1D={d:0.2f}% | 1W={w:0.2f}%".format(
            h=currency["changes"]["h"],
            d=currency["changes"]["d"],
            w=currency["changes"]["w"],
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
