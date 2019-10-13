#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

import argparse
import sys
from scrapy.cmdline import execute


def main(args):

    if args.stage == 1:
        execute(['scrapy', 'crawl', 'product', "-a", "cate_id=1", "-a", "origin_id=1"])
    if args.stage == 2:
        execute(['scrapy', 'crawl', 'comment'])

    print('加入stage参数')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', '-s', default=0, type=int, help='stage')
    args = parser.parse_args(sys.argv[1:])

    main(args)


