class TemplateNotValidatedException(Exception):
    """
    Raised when a report is attempted to be generated based
    on an un-validated template.
    """


class TemplateNotFoundException(Exception):
    """
    Raised when the specified template cannot be found.
    """


class InvalidTagException(Exception):
    """
    Raised whenever an invalid tag is provided to the report generator.
    """


class MultipleHeaderTagsException(Exception):
    """
    Raised when there multiple header tags are found in a template.
    """


class MissingHeaderTagException(Exception):
    """
    Raised when no header tag is found in a template.
    """


class MissingDataTagException(Exception):
    """
    Raised when no data tags are found in a template.
    """


class InvalidSpecialParameterException(Exception):
    """
    Raised when an invalid value for a special tag is used.
    """


class InvalidSettingsException(Exception):
    """
    Raised when an invalid type is passed for the custom settings argument to the report generator class.
    """
