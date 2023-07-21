Let's start with a basic example where a template contains only tags
that should be replaced with simple string values.
Let's say this template is called `example1.xlsx`.

+-----------+------------+----------+
|   Title   |   Author   |   Date   |
+===========+============+==========+
| {{TITLE}} | {{AUTHOR}} | {{DATE}} |
+-----------+------------+----------+

To parse this template and replace the tags with actual values, you could do
something like this::
    from ieasyreports.core.tags.tag import Tag
    from ieasyreports.utils import import_from_string

    from ieasyreports.settings import Settings

    settings = Settings()

    # Define tags
    title_tag = Tag("TITLE", "Water Discharge Report")
    author_tag = Tag("AUTHOR", "John Doe")
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
| Water Discharge Report | John Doe | January 1st, 2023 |
+------------------------+----------+-------------------+
