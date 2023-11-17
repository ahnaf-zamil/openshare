import jsonschema


def bad_request_resp(e: jsonschema.ValidationError):
    if len(e.relative_path):
        return {"error": f"Invalid value for '{e.relative_path[0]}'"}, 400
    return {"error": e.message}, 400
