#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

import json


def orm_to_json(all_vendors):
    v = [ven.double_to_dict() for ven in all_vendors]
    # v = [ven.double_to_dict() for ven in all_vendors]
    return v
