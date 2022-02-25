# coding=utf-8

def percent(value):
    if value > 50:
        arrows = u"🟢 ⬆️️"
    elif value > 10:
        arrows = u"🟢 ↗️️"
    elif value > 0:
        arrows = u"🟢 ➡️️"
    elif value < -50:
        arrows = u"🔴 ⬇️️"
    elif value < -10:
        arrows = u"🔴 ↙️️"
    else:
        arrows = u"🔴 ⬅️️"

    return u"{value:0.2f}% {arrows}".format(value=value, arrows=arrows)


def price(value):
    if value < 0.01:
        return "{:0.8f}".format(value)

    if value < 1:
        return "{:0.6f}".format(value)

    return "{:0.2f}".format(value)
