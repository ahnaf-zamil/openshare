from ..src.util import bad_request_resp

import jsonschema


def test_bad_request_resp():
    exc_no_rel_path = jsonschema.ValidationError(message="Invalid username")
    assert bad_request_resp(exc_no_rel_path) == ({"error": "Invalid username"}, 400)

    exc_with_rel_path = jsonschema.ValidationError(message="Invalid username")
    exc_with_rel_path.relative_path = (
        "username",
        "password",
    )
    assert bad_request_resp(exc_with_rel_path) == (
        {"error": "Invalid value for 'username'"},
        400,
    )
