=======
Design
=======

Immutability
============
Being coded in a functional style (Guido, forgive me), processr never changes or mutates objects during processing.


Error Handling
==============
By design, processr will let every exception raised by a stage bubble up.
Its up to you to catch the exception raised during the dict processing and act accordingly.
