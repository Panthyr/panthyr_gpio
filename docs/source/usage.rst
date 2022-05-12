===============================
Panthyr gpio example code
===============================



.. code:: python

    >>> from panthyr_gpio.p_gpio import pGPIO
    # create object for pin P9_27 (chip 3 offset 19) and set it to output, high
    >>> g = pGPIO(3,19,'out',1)
    # Set pin low again
    >>> g.off()
    # Get current pin value from pin
    >>> g.current_value()
    0