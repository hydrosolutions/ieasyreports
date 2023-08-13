Let's start with a basic example where a template contains only tags
that should be replaced with simple string values.
Let's say this template is called `example1.xlsx`.

+-----------+------------+----------+
|   Title   |   Author   |   Date   |
+===========+============+==========+
| {{TITLE}} | {{AUTHOR}} | {{DATE}} |
+-----------+------------+----------+

Also, to spice things up, the author tag will have the `custom_number_format_fn` argument in order
to demonstrate how it works. What the argument does is call the passed in callback function and
call it with the value returned by the replacement function which means that first the replacement function
will be called, then the custom number format function will be called to further transform the value which
will then be added in the output report. Notice that even though the `author_uppercase` function receives
an argument, you only pass in the reference to the function to the `custom_number_format_fn` and the library
will make sure to call the function with the value passed in.

To parse this template and replace the tags with actual values, you could do
something like this::
    from ieasyreports.core.tags.tag import Tag
    from ieasyreports.utils import import_from_string

    from ieasyreports.settings import Settings

    def author_uppercase(author):
        return author.upper()

    settings = Settings()

    # Define tags
    title_tag = Tag("TITLE", "Water Discharge Report")
    author_tag = Tag("AUTHOR", "John Doe", custom_number_format_fn=author_uppercase)
    date_tag = Tag("DATE", "July 20, 2023")

    # create the ReportGenerator instance
    report_generator = import_from_string(settings.template_generator_class)(
        tags=[title_tag, author_tag, date_tag],
        template='example.xlsx'
    )

    report_generator.validate()
    report_generator.generate_report()


This should produce an output report .xlsx file in the location specified
in the `report_output_path` setting in the library's Settings object.
The default is that it will create a `reports` folder in the same location from where you are running this code.
The content of the output report should be the following:

+------------------------+----------+-------------------+
|         Title          |  Author  |       Date        |
+========================+==========+===================+
| Water Discharge Report | JOHN DOE | January 1st, 2023 |
+------------------------+----------+-------------------+
