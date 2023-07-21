=====
Usage
=====

This guide shows some basic usages of the library.

Tag creation
------------

iEasyReports revolves around the creation of Tag objects.
A Tag maps a placeholder in a template to a function that provides the actual data.
Here's an example of creating a Tag::

    from ieasyreports.core.tags.tag import Tag

    author_tag = Tag(
        "AUTHOR",
        "John Doe",
        "Report author"
    )


The first argument is the name of the tag as it appears in the template, the second argument is the actual value or a function that returns the value
and the third argument is an optional description.

Here are all the parameters that a Tag object accepts during instantiation::

    name: The name of the tag.
    get_value_fn: The function or string used to get the replacement value for the tag.
    value_fn_args: Arguments that will be passed to the `get_value_fn`.
    description (optional): A description of the tag.
    custom_number_format_fn (optional): A custom function to format the tag's value.


DataManager Classes
___________________

DataManager classes encapsulate the logic required to access and format the data.
The DefaultDataManager class provides a basic example of a DataManager,
providing a method to format a date::

    from ieasyreports.core.data_manager import DefaultDataManager

    date = DefaultDataManager.get_localized_date(datetime.today(), 'en', 'long')



Examples
________

.. include:: example1.rst

.. include:: example2.rst

.. include:: example3.rst
