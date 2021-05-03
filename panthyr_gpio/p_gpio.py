#!/usr/bin/python3
# coding: utf-8

import gpiod
ALLOWED_MODES = ('out', 'adc')
class p_gpio:

    def __init__(self, chip,offset,mode, value = None):  
        self.chip = chip
        self.offset = offset
        if mode not in ALLOWED_MODES:
            raise ValueError('Mode {} not allowed, should be one of: {}'.format(mode, ALLOWED_MODES))
        self.mode = mode
        self.value = value
        self._get_pin()
        self._configure_mode()

    def _get_pin(self) -> None:
        chip = gpiod.chip(self.chip)
        self.pin = chip.get_line(self.offset)

    def _configure_mode(self) -> None:
        # configure mode
        pin_configuration = gpiod.line_request()

        if self.mode == 'out':
            pin_configuration.request_type = gpiod.line_request.DIRECTION_OUTPUT
            pin_configuration.flags = gpiod.line_request.FLAG_BIAS_PULL_DOWN

        if self.mode == 'adc':  # TODO
            raise NotImplementedError('Still need to implement ADC')

        self.pin.request(pin_configuration)

        if self.mode == 'out' and not self.value:  # current value of pin is not yet known
            self.value = self.pin.get_value()

    def on(self) -> None:
        """Sets ouput pin high"""
        if self.mode != 'out':
            raise Exception('Pin is not output type')
        self.value = 1
        self.pin.set_value(1)

    def off(self) -> None:
        """Sets output pin low"""
        if self.mode != 'out':
            raise Exception('Pin is not output type')
        self.value = 0
        self.pin.set_value(0)
    
    def update_value(self):
        if self.mode == 'out':
            self.value = self.pin.get_value()
            return self.value
        
        if self.mode == 'adc':  # TODO
            raise NotImplementedError('Still need to implement ADC')