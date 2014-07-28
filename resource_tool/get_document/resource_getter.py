# -*- coding: utf-8 -*-
import os
import subprocess

def zunda(chapas_data):
    proc = subprocess.Popen(
        ['zunda', '-i', '3'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    return proc.communicate(chapas_data)[0]


def chapas(text_data):
    CHAPAS_PATH = os.getenv("HOME") + "/local/dist/chapas-0.742"
    proc = subprocess.Popen(
        ['java', '-jar', '{}/chapas.jar'.format(CHAPAS_PATH), '-I', 'RAW'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    return proc.communicate(text_data)[0]


if __name__ == '__main__':
    pass
