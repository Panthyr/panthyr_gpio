===============================
Panthyr gpio example code
===============================

Test from command line:

.. code:: bash
    > test_pwr
    Which output (1-6) do you want to power on?
    > 1

    Output 1 on chip 3 at offset 19 is now ON.
    Type exit or press CTRL+C to switch back off and exit...
    >exit

.. code:: python

    >>> from panthyr_gpio.p_gpio import pGPIO
    # create object for pin P9_27 (chip 3 offset 19) and set it to output, high
    >>> g = pGPIO(3,19,'out',1)
    # Set pin low again
    >>> g.off()
    # Get current pin value from pin
    >>> g.current_value()
    0