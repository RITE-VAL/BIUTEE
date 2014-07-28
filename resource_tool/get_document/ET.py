# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET


def xml_iter(filename):
    root = ET.parse(filename).getroot()
    for pair in root:
        yield pair


if __name__ == '__main__':
    pass

