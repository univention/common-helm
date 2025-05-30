# The following values should all lead to no annotations being rendered output

NO_ANNOTATION_VALUES = [
    "{}",
    "null",
    "~",
    # NOTE: Setting an empty string is technically invalid, people tend to
    # use the empty string at times to unset a value. This ensures that the
    # implementation is robust in this case.
    '""',
]
