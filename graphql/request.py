import ast
import pprint
import re
import requests
from typing import List


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


'''
Making a function that returns the types by making a query could rapidly consume the gas limit.

    Ex:
        api = GraphQL(url)
        print(api.types())
        print(api.types())
        print(api.types())
    
The solution seems to be save the result of the query in an instance variable

    Ex: 
        class GraphQL:
        
            def __init__(self):
                self.types = self.query('{__schema{types{name}}}')
                
            def query(self, q: str) -> dict:
                return requests.post(self.url, json={'query': q})
    
        api = GraphQL(url)
        print(api.types)
        print(api.types)
        print(api.types)
        
However, doing this means that simply instantiating the GraphQL object will use some of the gas limit. 
This is not desirable, especially if the information retrieved is never used.

To get around this, the @property field is used so that the instance variable is only ever initialized if the variable
is accessed. The query is only made if necessary. 
'''


class GraphQL:

    def __init__(self, url: str):

        self.url: str = url

        self._re_name: re.Pattern = None
        self._types: List[str] = None
        self._fields = {}

    @property
    def re_name(self):
        if not self._re_name:
            self._re_name = re.compile("{'name': '(.*?)'}")
        return self._re_name

    @property
    def types(self):
        if not self._types:
            r = self.query('{__schema{types{name}}}')
            types_raw = pprint.pformat(r.json())
            self._types = self.re_name.findall(types_raw)

        return self._types

    # invoked by self.type_fields
    # invoked by self.all_types_all_fields
    def _init_type_fields(self, type_name: str) -> str:

        r = self.query('{__type(name: "' + type_name + '") {fields{name}}}')
        field_names = self.re_name.findall(pprint.pformat(r.json()))

        if not field_names:
            field_names = []

        self._fields[type_name] = field_names
        return self._fields[type_name]

    def type_fields(self, type_name: str) -> str:

        f = self._fields.get(type_name)

        # type fields not yet queried
        if not f:
            return self._init_type_fields(type_name)

        # type fields were already queried
        else:
            return f

    # this function is intentionally given a long name so as to discourage its use
    # calling this function will invoke a chain of queries
    def all_types_all_fields(self, waiter=False, omit_introspective=True):

        if waiter:
            print('------------------------------')
            print('waiter: all_types_all_fields()')
            print('------------------------------')

        # make sure that the dictionary is completed
        # if the fields for a type are not present, add them
        for t in self.types:

            if omit_introspective:
                if len(t) >= 3 and '__' == t[:2]:
                    continue

            if waiter:
                print('-', t)

            f = self._fields.get(t)

            # an empty list means that _init_type_fields was already called
            if not f and not isinstance(f, list):
                self._init_type_fields(t)

        if waiter:
            print('----------------------------')

        return self._fields

    def query(self, q: str) -> dict:
        return requests.post(self.url, json={'query': q})

    # print results of query
    def pquery(self, q: str, verbose=False) -> dict:
        r = self.query(q)

        if verbose:
            rprint(r, verbose=verbose)

        else:
            pprint.pprint(r.json())

        return r
