import ast
import pprint
import requests


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
            print(r.request.url)
            if r.request.body:
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
