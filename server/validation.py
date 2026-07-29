from jsonschema import validate, ValidationError

campaign_schema = {
    "type": "object",
    "properties": {
        "campaign_id": {
            "type": "integer",
            "minimum": 1
        }
    },
    "required": ["campaign_id"],
    "additionalProperties": False
}


def validate_campaign_input(data):
    try:
        validate(instance=data, schema=campaign_schema)
        return True, None
    except ValidationError as e:
        return False, str(e)