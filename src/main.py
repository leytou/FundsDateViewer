#!/usr/bin/python
# -*- coding: utf-8 -*-

import fund_list
import fl
import hold
import figure
from itertools import islice


def chunks(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k: data[k] for k in islice(it, SIZE)}


if __name__ == "__main__":
    hold_data = hold.get_hold_data_from_excel()
    print('hold_data:', hold_data)

    l = fund_list.get_fund_list()
    for item in chunks(hold_data, 9):
        print('9item', item)
        figure.draw(item, l)
    figure.show()
