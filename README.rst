**************************************
WAVE - Whole Architecture Verification
**************************************

Environment
-----------

.. code::

    $ conda env create -f environment.yml
    $ conda activate wave

Example
-------

Inside the wave environment use pip to install jupyter and then
try these examples in a notebook.

.. code:: python

    import wavelib
    from wavelib import dbif
    from wavelib import metamodel
    from wavelib import operations

    join = metamodel.Function(operations.join, fix = 'in', symbol = '.')
    diff = metamodel.Function(operations.diff, fix = 'in', symbol = '-')
    invert = metamodel.Function(operations.invert, fix = 'pre', symbol = '~')
    close =  metamodel.Function(operations.close, fix = 'pre', symbol = '^')
    mm = metamodel.Metamodel()
    mm.add_function(join, 'join', 'join')
    mm.add_function(diff, 'diff', 'diff')
    mm.add_function(invert, 'invert', 'invert')
    mm.add_function(close, 'close', 'close')
