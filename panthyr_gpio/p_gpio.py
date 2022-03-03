#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

import gpiod  # noqa

ALLOWED_MODES = ('out')
ADC_NOT_IMPLEMENTED = 'ADC not yet implemented.'


def initialize_logger() -> logging.Logger:
    """Set up logger
    If the module is ran as a module, name logger accordingly as a sublogger.
    Returns:
        logging.Logger: logger instance
    """
    if __name__ == '__main__':
        return logging.getLogger('{}'.format(__name__))
    else:
        return logging.getLogger(
            '__main__.{}'.format(__name__))


class ADCNotImplemented(NotImplementedError):
    """ADC functionality not yet implemented."""
    pass


class pGPIO:

    def __init__(self, chip, offset, mode=None, value=None):
        self.chip = chip
        self.offset = offset
        if mode and mode not in ALLOWED_MODES:
            raise ValueError(
                'Mode {} not allowed, should be one of: {}'.
                format(mode, ALLOWED_MODES))
        self.mode = mode
        self.value = value
        self._get_pin()
        self._configure_mode()
        self.log = initialize_logger()

    def _get_pin(self) -> None:
        """Select the pin so we have access to the HW."""
        chip = gpiod.chip(self.chip)
        self.pin = chip.get_line(self.offset)

    def _configure_mode(self) -> None:
        """Configure pin mode (ie set to output/adc/...)"""

        pin_configuration = gpiod.line_request()

        if self.mode == 'out':
            pin_configuration.request_type = gpiod.line_request.DIRECTION_OUTPUT
            # pin_configuration.flags = gpiod.line_request.FLAG_BIAS_PULL_DOWN
            # TODO: PULLDOWN trows exception:
            # status = ioctl(fd, GPIO_GET_LINEHANDLE_IOCTL, req)
            # OSError: [Errno 22] Invalid argument
            self.pin.request(pin_configuration)

            # set value if given
            if self.mode is None:
                # self.value = self.pin.get_value()  # TODO doesn't work yet (is this possible??)
                pass
            elif self.mode == 1:
                self.on()
            else:
                self.off()

        if self.mode == 'adc':
            self.log.exception('ADC not implemented yet')
            raise ADCNotImplemented

    def on(self) -> None:
        """Sets ouput pin high"""
        self._set_pin_value(1)

    def off(self) -> None:
        """Sets output pin low"""
        self._set_pin_value(0)

    def _set_pin_value(self, value: int):
        if self.mode != 'out':
            self.log.exception(
                f'Cannot set pin {self.pin}, not set as output.'
            )
            raise Exception('Pin is not set to output')
        self.log.debug(f'Pin {self.pin} set to {value}')
        self.value = value
        self.pin.set_value(value)

    def update_value_from_hw(self):
        if self.mode == 'out':
            self.value = self.pin.get_value()
            return self.value

        if self.mode == 'adc':
            raise NotImplementedError()
