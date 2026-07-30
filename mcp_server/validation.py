from jsonschema import validate, ValidationError

# Schema 1: Campaign ID Validation (for details & simple actions)
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

# Schema 2: Role Change Input Validation
role_change_schema = {
    "type": "object",
    "properties": {
        "role": {
            "type": "string",
            "enum": ["ANALYST", "MANAGER", "ADMIN", "employee", "manager", "admin"]
        }
    },
    "required": ["role"],
    "additionalProperties": False
}

# Schema 3: Campaign Approval Input Validation
approval_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 3},
        "password": {"type": "string", "minLength": 3},
        "campaign_id": {"type": "integer", "minimum": 1}
    },
    "required": ["username", "password", "campaign_id"],
    "additionalProperties": False
}


def validate_campaign_input(data):
    try:
        validate(instance=data, schema=campaign_schema)
        return True, None
    except ValidationError as e:
        return False, e.message


def validate_role_input(data):
    try:
        validate(instance=data, schema=role_change_schema)
        return True, None
    except ValidationError as e:
        return False, e.message


def validate_approval_input(data):
    try:
        validate(instance=data, schema=approval_schema)
        return True, None
    except ValidationError as e:
        return False, e.message