prsannots
=========

prsannots is a Python script that lets you save versions of PDF files
that you've annotated on your Sony PRS-T1 ereader.  It supports both
freehand and highlighted annotations, though the latter is apt to be a
bit flaky.  Drawings attached to highlighted passages are not transfered.

Usage
-----
Invoke the script with the mount point of your ereader as the argument::

  prsannots.py /path/to/ereader

On my Ubuntu Linux system, this mount point is ``/media/READER``. You'll
be presented with a list of all PDF files with annotations on the
ereader; select the one you want and optionally specify the filename to
save it as.  The script will exit after creating the annotated PDF file.

Requirements
------------
You'll need some version of Python 2.  Thus far, prsannots has been
tested on 2.6 and 2.7, but there's no reason it shouldn't work on
previous versions.  (That said, maintaining compatibility with 2.5 and
earlier is not a goal.)  It is not compatible with Python 3.

In addition to the standard library, it requires the pyPdf_ (>= 1.13),
ReportLab_, and PDFMiner_ libraries.  For Debian-based systems, the
first two are provided by the ``python-pypdf`` and ``python-reportlab``
packages.  (Note that Debian prior to Wheezy and Ubuntu prior to 11.10
have a too-old version of pyPdf.)  All three are available in PyPI_.
prsannots also makes use of a modified version of svglib_, but this is
shipped with the script.

.. _pyPDF: http://pybrary.net/pyPdf/
.. _ReportLab: http://www.reportlab.com/software/opensource/rl-toolkit/
.. _PDFMiner: http://www.unixuser.org/~euske/python/pdfminer/
.. _PyPI: http://pypi.python.org/pypi
.. _svglib: http://pypi.python.org/pypi/svglib/

This script has been developed and tested in Linux, but it should work
on any other operating system that can meet the above requirements.
I wouldn't be surprised if there were path problems on Windows; please
let me know and they should be fixable.

Right now, only the Sony PRS-T1 is supported, because that's what I have.
I would not be surprised if other Sony ereaders used similar schemes for
their annotations, and I'm happy to add support for them if someone
provides the gritty details.  I don't know about other brands.

Installation
------------
The best way to get prsannots is by cloning the git repository::

  git clone git://github.com/rschroll/prsannots.git

Alternatively, you can download and unpack the zipball_.

.. _zipball: https://github.com/rschroll/prsannots/zipball/master

There's no installation procedure yet—just run the script.

Development
-----------
prsannots is being developed on GitHub_.  Check out that site for
updated versions.  Please report bugs and feature requests to the
Github `bug tracker`_.

.. _GitHub: https://github.com/rschroll/prsannots
.. _bug tracker: https://github.com/rschroll/prsannots/issues

prsannots has been written (thus far) by Robert Schroll
(rschroll@gmail.com).  Feel free to get in touch with questions and
comments.