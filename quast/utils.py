import json
from urllib.parse import parse_qs


def data_as_dict(request):
    """
    :param request: ``Flask.Request`` request instance
    :return:        Data after parsing as json.
    """
    data = request.get_data().decode()
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        data = parse_qs(data)
        if data:
            tmp = data
            for key, value in tmp.items():
                if isinstance(value, list) and len(value) == 1:
                    data[key] = value[0]
        else:
            raise json.JSONDecodeError("Cannot decode as json: " + data)
    finally:
        return data

