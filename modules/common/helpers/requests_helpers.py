import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def get_retry_session(retries, session=None, backoff_factor=2):
    """Requests-Session mit automatischen Retries

    retries: Anzahl Versuche
    backoff_factor: Anzahl Sekunden, die zwischen den Versuchen gewartet wird (nach jedem Versuch wird der Faktor mal zwei genommen)
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        method_whitelist=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
