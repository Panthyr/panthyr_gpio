#!/usr/bin/python3
# coding: utf-8

import argparse
from panthyr_gpio import p_gpio

DEFAULT_MAPPING = ((3,19),(3,18),(2,12),(2,6),(0,8),(0,9))

def get_arguments()-> dict:
    """
    Get (and check) command line arguments. 
    Args:
        none
    
    Returns:
        dict (see prepare_args_rtn)
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--setup',
                        action = 'store_true',
                        dest = 'setup',
                        default = False,
                        help = 'Set up/configure the GPIO pins')
    parser.add_argument('--status',
                        action ='store_true',
                        dest ='status',
                        default = False,
                        help = 'Print current output status')
    parser.add_argument('--high',
                        action='append',
                        dest='high',
                        default=[],
                        help = 'Each output that needs to be set high (1)')
    parser.add_argument('--low',
                        action ='append',
                        dest ='low',
                        default = [],
                        help = 'Each output that needs to be set low (0)')
    parser.add_argument('--mapping',
                        action = 'store',
                        dest = 'mapping',
                        type = tuple,
                        help = 'Provide a tuple describing the pin mapping, \
                            (chip id, offset) for each output, in order. For default: \
                            {}'.format(DEFAULT_MAPPING))
    results = parser.parse_args()
    return prep_args_rtn(results)

def prep_args_rtn(results) -> dict:
    """
    Process the parsed arguments and convert them in to a dict.
    Args:
        results: argparse.Namespace
    Returns:
        dict with following items:
            'setup': Bool: setup is one of the cli args
            'status': Bool: status is one of the cli args, return current status of outputs
            'high': list output numbers that needs to be set high
            'low': list output numbers that needs to be set low
    """
    rtn = {'setup': results.setup, 'status': results.status, 'high': [], 'low': []}

    for i in results.high:
        try:
            rtn['high'].append(int(i))
        except ValueError:
            print('ERROR: Value for high output ({}) not valid, should be a single integer. (range 1-6).\n'.format(i) + 
                'Ignoring this value and continuing.')
    for i in results.low:
        try:
            rtn['low'].append(int(i))
        except ValueError:
            print('ERROR: Value for low output ({}) not valid, should be a single integer (range 1-6).\n'.format(i) +
                'Ignoring this value and continuing.')

    # check that the user asked for anything at all
    check_rtn = (rtn['setup'], rtn['status'], len(rtn['low']), len(rtn['high']))
    if not any(check_rtn):
        print('No arguments specified. Use -h or --help for more information.')

    return rtn

def get_pin_descr() ->tuple:
    # sourcery skip: inline-immediately-returned-variable
    """
    Gets the pin description.

    Currently uses the default values

    Returns:
        pin_descr: tuple consisting of 6 tuples (chip, line/offset), one for each output.
    """
    pin_descr = DEFAULT_MAPPING
    return (pin_descr)

def init_gpio(pin_descr:tuple) -> tuple:
    """
    Initialize and configure the GPIO pins.

    Args: 
        pin_descr: tuple: consisting of 6 tuples (chip, line/offset), one for each output.
                ie. for the defaults: ((3,19), (3,18), (2,12), (2,6), (0,8), (0,9))
    Returns:
        tuple with as many gpio's as described in the pin_descr
    """
    outputs = []
    for chip, offset in pin_descr:
        pin = p_gpio(chip = chip,offset = offset, mode = 'out')
        outputs.append(pin)

    return outputs

if __name__ == '__main__':
    args = get_arguments()
    pin_descr = get_pin_descr()
    outputs = init_gpio(pin_descr)
    print('outputs: {}'.format(outputs))

    if len(args['high']) > 0:
        print('setting high: {}'.format(args['high']))
        for i in args['high']:
            outputs[i-1].on()

    if len(args['low']) > 0:
        print('setting low: {}'.format(args['low']))
        for i in args['low']:
            outputs[i-1].off()
    
    if args['status']:
        print('|OUTPUT|VALUE|')
        for index,output in enumerate(outputs):
            print('|{:6}|{:5}|'.format(index + 1, output.value))