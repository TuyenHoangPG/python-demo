add_post_validation_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "minLength": 1, "maxLength": 120},
        "description": {"type": "string", "maxLength": 500},
    },
    "required": ["title"],
}

update_post_validation_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "minLength": 1, "maxLength": 120},
        "description": {"type": "string", "maxLength": 500},
    },
}
