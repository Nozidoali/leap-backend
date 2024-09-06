#!/usr/bin/env python
# -*- encoding=utf8 -*-

"""
Author: Hanyu Wang
Created time: 2024-05-22 14:46:26
Last Modified by: Hanyu Wang
Last Modified time: 2024-05-22 14:48:09
"""
from .blifGraph import BLIFGraphBase


class BLIFGraph(BLIFGraphBase):
    def __init__(self, *args, **kwargs) -> None:
        if len(args) == 0:
            BLIFGraphBase.__init__(self)

        elif len(args) == 1:
            self = args[0]

    def __repr__(self) -> str:
        return super().__repr__()
