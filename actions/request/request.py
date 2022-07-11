from __future__ import annotations

import requests


def request_post_api(url: str, json: any = None, params: any = None) -> requests.Response:
    try:
        return requests.post(url=url, json=json, params=params)

    except requests.exceptions.HTTPError as errh:
        return errh
    except requests.exceptions.ConnectionError as errc:
        return errc
    except requests.exceptions.Timeout as errt:
        return errt
    except requests.exceptions.RequestException as err:
        return err


def request_get_api(url: str, json: any = None, params: any = None) -> requests.Response:
    try:
        return requests.get(url=url, json=json, params=params)

    except requests.exceptions.HTTPError as errh:
        return errh
    except requests.exceptions.ConnectionError as errc:
        return errc
    except requests.exceptions.Timeout as errt:
        return errt
    except requests.exceptions.RequestException as err:
        return err
