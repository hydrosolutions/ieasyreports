class TemplateNotValidatedException(Exception):
    """
    Raised when a report is attempted to be generated based
    on an un-validated template.
    """
    pass


class InvalidTagException(Exception):
    """
    Raised whenever an invalid tag is provided to the report generator.
    """


class MultipleHeaderTagsException(Exception):
    """
    Raised when there multiple header tags are found in a template.
    """
