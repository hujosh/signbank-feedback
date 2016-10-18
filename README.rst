=============================
Signbank-Feedback
=============================

.. image:: https://badge.fury.io/py/signbank-feedback.png
    :target: https://badge.fury.io/py/signbank-feedback

.. image:: https://travis-ci.org/hujosh/signbank-feedback.png?branch=master
    :target: https://travis-ci.org/hujosh/signbank-feedback
    
.. image:: https://codecov.io/gh/hujosh/signbank-feedback/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/hujosh/signbank-feedback

The feedback component of Signbank

Documentation
-------------

The full documentation is at https://signbank-feedback.readthedocs.org.

Quickstart
----------

Install Signbank-Feedback::

    pip install signbank-feedback

Then use it in a project::

    import feedback
    
    
You must define the following variables in ``sttings.py``

* ``LANGUAGE_NAME``
* ``COUNTRY_NAME`` 
* ``SITE_TITLE``
    
Features
--------

* TODO

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
