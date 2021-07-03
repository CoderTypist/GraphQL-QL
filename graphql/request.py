import ast
import pprint
import requests


def query(url: str, q: str) -> dict:
    return requests.post(url, json={'query': q})


def is_ok(r: requests.Response) -> bool:
    if 200 == r.status_code:
        return True
    return False


# response print
def rprint(r: requests.Response, verbose=True) -> None:

    if verbose:
        print('-------------------------------------------------------------------------------------------------------')
        print('REQUEST & RESPONSE:')
        print('-------------------------------------------------------------------------------------------------------')

        if r:
            q = ast.literal_eval(r.request.body.decode())['query']
            print(q)
        else:
            print('\tError')

        print('-------------------------------------------------------------------------------------------------------')

        if r:
            pprint.pprint(r.json())
        else:
            print('\tError')

        print('-------------------------------------------------------------------------------------------------------')
        print('Status Code:', r.status_code)
        print('-------------------------------------------------------------------------------------------------------')

    else:
        pprint.pprint(r.json())


# print results of query
def pquery(url: str, q: str, verbose=False) -> dict:
    r = query(url, q)

    if verbose:
        rprint(r, verbose=verbose)

    else:
        pprint.pprint(r.json())

    return r
