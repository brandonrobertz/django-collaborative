from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# NOTE: when these change, ensure the columnswidget.html
# JavasCript changes to include any new fields
COLUMN_TYPES = (
    ("text", "Textbox field"),
    ("short-text", "Text field"),
    ("date", "Only date field"),
    ("time", "Only time field"),
    ("datetime", "Date and time field"),
    ("number", "Number field"),
    # ("foreignkey", "Associated Table"),
    ("tagging", "Tags field"),
)
REQUIRED_FIELDS = (
    "name", "type",
)
ALL_FIELDS = REQUIRED_FIELDS + (
    "attrs", "original_name", "args",
    "searchable", "filterable",
)


def validate_columns(value):
    if not value:
        return

    for col in value:
        for field_name in REQUIRED_FIELDS:
            req_field = col.get(field_name)
            if not req_field:
                raise ValidationError(
                    _("A column is missing required field: %s" % field_name)
                )
            if field_name not in ALL_FIELDS:
                raise ValidationError(
                    _("A column contains invalid field: %s" % field_name)
                )

        type = col.get("type")
        valid_type_names = [v[0] for v in COLUMN_TYPES]
        if type not in valid_type_names:
            raise ValidationError(_("A column has invalid type: %s" % type))

        attrs = col.get("attrs", {})
        if attrs and not isinstance(attrs, dict):
            raise ValidationError(_("Column attributes must be a dictionary"))

