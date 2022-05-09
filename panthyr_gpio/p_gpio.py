#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
from typing import Union

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
        return logging.getLogger(f'{__name__}')
    else:
        return logging.getLogger(f'__main__.{__name__}')


class ADCNotImplemented(NotImplementedError):
    """ADC functionality not yet implemented."""
    pass


class pGPIO:

    def __init__(
        self,
        chip: int,
        offset: int,
        mode: Union[str, None] = None,
        value: Union[int, None] = None,
    ):
        """Initialize pin.

        Args:
            chip (int): Chip number
            offset (int): Pin hardware offset
            mode (str, optional): one of ALLOWED_MODES (currently only 'out'). Defaults to None.
            value (int, optional): 0 for low, 1 for high. Defaults to None.

        Raises:
            ValueError: if given mode is not allowed
        """
        self.log = initialize_logger()
        self.chip = chip
        self.offset = offset
        if mode and mode not in ALLOWED_MODES:
            raise ValueError(
                f'Mode {mode} not allowed, should be one of: {ALLOWED_MODES}',
            )
        self.mode = mode
        self._get_pin()
        if self.mode is not None:
            self._configure_mode()
            if self.value is not None:
                self._set_pin_value(value)

    def _get_pin(self) -> None:
        """Select the pin so we have access to the HW."""
        chip = gpiod.chip(self.chip)
        self.pin = chip.get_line(self.offset)

    def current_value(self) -> Union[int, None]:
        """Update the current value and return it.

        Returns:
            int: Current value (0/1 if output or 0-256 for ADC)
        """
        self.update_value_from_hw()
        return self.value

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
                self.value = self.pin.get_value()
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
        """Set an output pin to high or low.

        Args:
            value (int): 0 for off, 1 for on

        Raises:
            ValueError: if pin is not configured as output
        """
        if self.mode != 'out':
            self.log.exception(
                f'Cannot set pin {self.pin}, not set as output.',
            )
            raise ValueError('Pin is not set to output')
        self.log.debug('Pin {self.pin} set to {value}')
        self.value = value
        self.pin.set_value(value)

    def update_value_from_hw(self) -> None:
        """Get current value from hardware.

        Updates the current status (on/off) if pin is set to OUT.
        Will contain code to read value on input if pin set to ADC.

        Raises:
            NotImplementedError: If pin is set to adc
        """
        if self.mode == 'out':
            self.value = self.pin.get_value()

        if self.mode == 'adc':
            raise NotImplementedError()
