import jsonschema


def bad_request_resp(e: jsonschema.ValidationError):
    field = e.relative_path[0]
    return {"error": f"Invalid value for '{field}'", "field": field}, 400
