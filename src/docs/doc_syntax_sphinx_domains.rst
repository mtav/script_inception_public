=====================================================
Sphinx domains Cheat Sheet: Syntax Reminders
=====================================================

.. seealso::

  * http://sphinx-doc.org/domains.html
  * http://sphinx-doc.org/markup/para.html

Overview:
=========

functions::

  :py:func:`FUNCTION`

class::

  :py:class:`CLASS`

parameters::

  :param VARNAME: TYPE+DESCRIPTION

return values::

  :return: VARNAME+TYPE+DESCRIPTION
  :return VARNAME: TYPE+DESCRIPTION

tables::

  TODO

`Bullet lists and numbered lists <http://www.sphinx-doc.org/en/stable/rest.html#lists-and-quote-like-blocks>`_::

  * ITEM
  * ITEM
  * ITEM

  * This is a bulleted list.
  * It has two items, the second
    item uses two lines.

  * this is
  * a list

    * with a nested list
    * and some subitems

  * and here the parent list continues

  1. This is a numbered list.
  2. It has two items too.

  #. This is a numbered list.
  #. It has two items too.

bold::

  **BOLD**

italic::

  *ITALIC*

code/verbatim::

  ``CODE``

Long code/verbatim section::

  DESCRIPTION::
    CODE
    CODE
    CODE
    CODE
    CODE

Warnings::

  .. warning:: TEXT

`Todo notes <http://www.sphinx-doc.org/en/stable/ext/todo.html>`_::

  .. todo:: TEXT

Links::

  `Link text <http://example.com/>`_

Directives:

  * http://www.sphinx-doc.org/en/stable/rest.html#directives
  * http://docutils.sourceforge.net/docs/ref/rst/directives.html

Example:
========
Inside Python object description directives, reST field lists with these fields
are recognized and formatted nicely:

* ``param``, ``parameter``, ``arg``, ``argument``, ``key``, ``keyword``:
  Description of a parameter.
* ``type``: Type of a parameter.
* ``raises``, ``raise``, ``except``, ``exception``: That (and when) a specific
  exception is raised.
* ``var``, ``ivar``, ``cvar``: Description of a variable.
* ``returns``, ``return``: Description of the return value.
* ``rtype``: Return type.

The field names must consist of one of these keywords and an argument (except
for ``returns`` and ``rtype``, which do not need an argument).  This is best
explained by an example::

   .. py:function:: send_message(sender, recipient, message_body, [priority=1])

      Send a message to a recipient

      :param str sender: The person sending the message
      :param str recipient: The recipient of the message
      :param str message_body: The body of the message
      :param priority: The priority of the message, can be a number 1-5
      :type priority: integer or None
      :return: the message id
      :rtype: int
      :raises ValueError: if the message_body exceeds 160 characters
      :raises TypeError: if the message_body is not a basestring

This will render like this:

   .. py:function:: send_message(sender, recipient, message_body, [priority=1])
      :noindex:

      Send a message to a recipient

      :param str sender: The person sending the message
      :param str recipient: The recipient of the message
      :param str message_body: The body of the message
      :param priority: The priority of the message, can be a number 1-5
      :type priority: integer or None
      :return: the message id
      :rtype: int
      :raises ValueError: if the message_body exceeds 160 characters
      :raises TypeError: if the message_body is not a basestring
