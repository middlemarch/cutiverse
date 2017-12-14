Usage
=====
.. _usage:

Arguments
---------

Command line arguments:

- ``-h`` ``--help`` Show a help message and exit
- ``-o`` ``--image-only`` Link directly to an image rather than a website
- ``-t`` ``--threads`` The number of threads to use for URL validation
- ``-n`` ``--noun`` Use a specific noun instead of randomly selecting one
- ``-V`` ``--version`` Print the version and exit
- ``-l`` ``--log-level`` Set command line verbosity {DEBUG,INFO,WARNING,ERROR,CRITICAL}
- ``-L`` ``--logfile`` Specify a file to output log messages to

Examples
--------

Basic::

    $ dopameme

Go directly to an image about cats::

    $ dopameme -o -n cat
