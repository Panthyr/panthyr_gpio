#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from panthyr_gpio.p_gpio import pGPIO

outputs = [
    (3, 19),
    (3, 18),
    (2, 12),
    (2, 6),
    (0, 8),
    (0, 9),
]


def power_up():
    outp = _get_output_from_user()
    if outp == 0:
        gpios = []
        for chip, offset in outputs:
            gpios.append(
                pGPIO(
                    chip=chip,
                    offset=offset,
                    mode='out',
                    value=1,
                ),
            )
        print(
            f'\nAll outputs in {outputs} are now ON. \n'
            'Type exit or press CTRL+C to switch back off and exit...', )
    else:
        chip, offset = _convert_to_chip_offset(outp)
        gpio = pGPIO(
            chip=chip,
            offset=offset,
            mode='out',
            value=1,
        )
        print(
            f'\nOutput {outp} on chip {chip} at offset {offset} is now ON. \n'
            'Type exit or press CTRL+C to switch back off and exit...', )

    try:
        while True:
            inp = input('>').lower()
            if inp == 'exit':
                raise KeyboardInterrupt
    except KeyboardInterrupt:
        sys.exit()


def _get_output_from_user() -> int:
    inp: str = input(
        'Which output do you want to power on? Choose 1-6 for a specidfic output or 0 for all.\n> ',
    )
    try:
        inp_int = int(inp)
        if inp_int not in {0, 1, 2, 3, 4, 5, 6}:
            raise ValueError
    except (TypeError, ValueError):
        print('Invalid output, can be 1/2/3/4/5/6')
        sys.exit()
    return inp_int


def _convert_to_chip_offset(inp: int) -> tuple:
    return outputs[inp - 1]
