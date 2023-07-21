This examples demonstrates how to use the Tag class when
you require a function for replacing the tags with some values.

For simplicity, let's say we're still working with the same `example1.xlsx` template:

+-----------+------------+----------+
|   Title   |   Author   |   Date   |
+===========+============+==========+
| {{TITLE}} | {{AUTHOR}} | {{DATE}} |
+-----------+------------+----------+

For this example, the functions needed can be used without any arguments::

    from ieasyreports.core.tags.tag import Tag
    from ieasyreports.utils import import_from_string

    from ieasyreports.settings import Settings

    settings = Settings()
    DataManager = import_from_string(settings.data_manager_class)


    def dummy_author_name():
        return "John Doe"


    # Define tags
    title_tag = Tag("TITLE", "Water Discharge Report")
    author_tag = Tag(
        "AUTHOR",
        dummy_author_name
    )
    date_tag = Tag(
        "DATE",
        DataManager.get_localized_date
    )

    # create the ReportGenerator instance
    report_generator = import_from_string(settings.template_generator_class)(
        tags=[title_tag, author_tag, date_tag],
        template='example1.xlsx'
    )

    report_generator.validate()
    report_generator.generate_report(output_filename="example2.xlsx")

This should produce an `example2.xlsx` file in the `reports` folder and it's content
should be the following:

+------------------------+----------+---------------+
|         Title          |  Author  |     Date      |
+========================+==========+===============+
| Water Discharge Report | John Doe | July 21, 2023 |
+------------------------+----------+---------------+

The value of the date tag depends on what date it is when running the script.
