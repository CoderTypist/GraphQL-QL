import query_manager as qm
from query_manager import GraphQL
from query_manager import Rest
import json
import pprint
import requests
import subprocess
import system as sos


def main():

    # github rest api query
    # - queries are embedded in the url
    # - does not use GraphQL-QL
    ex_rest_01()

    # github rest api query
    # - entire urls are used to make queries
    # - uses GraphQL-QL
    ex_rest_02()

    # github rest api query
    # - queries use partial urls
    # - uses GraphQL-QL
    ex_rest_03()

    # rick and morty graphql api query
    # - queries are stored in strings
    # - does not use GraphQL-QL
    ex_gql_01()

    # rick and morty graphql api query
    # - queries are stored in strings
    # - uses GraphQL-QL
    ex_gql_02()

    # spacex graphql api queries
    # - queries are in a separate .gql file
    # - uses GraphQL-QL
    ex_gql_03()

    # rick and morty graphql api queries
    # - queries are in a separate .gql file
    # - uses GraphQL-QL
    ex_gql_04()

    # loads, formats, and prints queries from .gql files
    # - uses GraphQL-QL
    ex_gql_05()

    # Uses introspection to get scheme types and their fields
    # - uses GraphQL-QL
    ex_gql_06()

    # execute shell commands
    # - uses system.shell(), which is a wrapper for subprocess.run()
    # - more robust than subprocess.run()
    ex_shell_01()

    # execut shell commands
    # - uses wrappers for system.shell()
    ex_shell_02()

    # get environment variables through desired shell/platform
    ex_env_01()

    # get environment variables from the desired platform
    ex_env_02()

    # get environment variables and check for None
    ex_env_03()


def ex_rest_01():

    title('ex_rest_01')

    url = 'https://api.github.com/users/thenewboston'
    r = requests.get(url)
    pprint.pprint(r.json())

    url = 'https://api.github.com/users/nationalsecurityagency'
    r = requests.get(url)
    pprint.pprint(r.json())

    url = 'https://api.github.com/users/ethereum'
    r = requests.get(url)
    pprint.pprint(r.json())


def ex_rest_02():

    title('ex_rest_02')

    api = Rest('https://api.github.com')

    r = api.query('/users/thenewboston')
    qm.rprint(r)

    r = api.query('/users/nationalsecurityagency')
    qm.rprint(r)

    r = api.query('/users/ethereum')
    qm.rprint(r)


def ex_rest_03():

    title('ex_rest_03')

    api = Rest('https://api.github.com')
    api.pquery('/users/thenewboston')
    api.pquery('/users/nationalsecurityagency')
    api.pquery('/users/ethereum')


def ex_gql_01():

    title('ex_gql_01')

    query_name = '''query {
                        characters {
                            results {
                                name
                            }
                        }
                    }'''

    query_status = '''query {
                        characters {
                            results {
                                status
                            }
                        }
                    }'''

    query_info = '''query {
                        characters {
                            results {
                                name
                                status
                                species
                                type
                                gender
                            }
                        }
                    }'''

    url = 'https://rickandmortyapi.com/graphql/'

    r = requests.post(url, json={'query': query_name})

    d = json.loads(r.text)
    pprint.pprint(r.json())

    # r = requests.post(url, json={'query': query_status})
    pprint.pprint(r.json())

    # r = requests.post(url, json={'query': query_info})
    pprint.pprint(r.json())


def ex_gql_02():

    title('ex_gql_02')

    query_name = '''query {
                        characters {
                            results {
                                name
                            }
                        }
                    }'''

    query_status = '''query {
                        characters {
                            results {
                                status
                            }
                        }
                    }'''

    query_info = '''query {
                        characters {
                            results {
                                name
                                status
                                species
                                type
                                gender
                            }
                        }
                    }'''

    api = GraphQL('https://rickandmortyapi.com/graphql/')
    api.pquery(query_name)
    api.pquery(query_status)
    api.pquery(query_info)


def ex_gql_03():

    title('ex_gql_03')

    api = GraphQL('https://api.spacex.land/graphql/')
    qs = qm.load('./queries/spacex.gql')

    # print all available queries
    # qm.pqueries(qs)

    r = api.query(qs['name'])
    qm.rprint(r)

    r = api.query(qs['basics'])
    qm.rprint(r)

    r = api.query(qs['verbose'])
    qm.rprint(r)
    # qm.rprint(r, verbose=False)


def ex_gql_04():

    title('ex_gql_04')

    api = GraphQL('https://rickandmortyapi.com/graphql/')
    qs = qm.load('./queries/rick_and_morty.gql')

    api.pquery(qs['name'])
    api.pquery(qs['status'])
    api.pquery(qs['info'])


def ex_gql_05():

    title('ex_gql_05')

    qm.pqueries(qm.load('./queries/rick_and_morty.gql'), title='RICK AND MORTY:')
    qm.pqueries(qm.load('./queries/spacex.gql'), title='SPACEX:')


def ex_gql_06():

    title('ex_gql_06')

    api = GraphQL('https://rickandmortyapi.com/graphql/')
    print(api.types)
    print(api.type_fields("Episodes"))
    pprint.pprint(api.all_types_all_fields(waiter=True, omit_introspective=False))


def ex_shell_01():

    title('ex_shell_01')

    # Use like this in practice
    '''
    print(sos.shell(sos.WINDOWS, ['dir']))
    print(sos.shell(sos.CMD, ['dir']))
    print(sos.shell(sos.POWERSHELL, ['ls']))
    print(sos.shell(sos.WSL, ['ls', '-la']))
    print(sos.shell(sos.LINUX, ['ls', '-la']))
    '''

    # Extra arguments are used for formatting and debugging
    print(sos.shell(sos.WINDOWS, ['dir'], tab=True, verbose=True))
    print(sos.shell(sos.CMD, ['dir'], tab=True, verbose=True))
    print(sos.shell(sos.POWERSHELL, ['ls'], tab=True, verbose=True))
    print(sos.shell(sos.WSL, ['ls', '-la'], tab=True, verbose=True))
    print(sos.shell(sos.LINUX, ['ls', '-la'], tab=True, verbose=True))


def ex_shell_02():

    title('ex_shell_02')

    # Use like this in practice
    '''
    print(sos.windows(['dir']))
    print(sos.cmd(['dir']))
    print(sos.powershell(['ls']))
    print(sos.wsl(['ls', '-la']))
    print(sos.linux(['ls', '-la']))
    '''

    # Extra arguments are used for formatting and debugging
    print(sos.windows(['dir'], tab=True, verbose=True))
    print(sos.cmd(['dir'], tab=True, verbose=True))
    print(sos.powershell(['ls'], tab=True, verbose=True))
    print(sos.wsl(['ls', '-la'], tab=True, verbose=True))
    print(sos.linux(['ls', '-la'], tab=True, verbose=True))


def ex_env_01():

    title('ex_env_01')

    print(sos.env(sos.WINDOWS, 'USERNAME'))
    print(sos.env(sos.CMD, 'USERNAME'))
    print(sos.env(sos.POWERSHELL, 'USERNAME'))
    print(sos.env(sos.WSL, 'WSL_DISTRO_NAME'))
    print(sos.env(sos.LINUX, 'USER'))


def ex_env_02():

    title('ex_env_02')

    # get an environment variable from Windows
    print(sos.wenv('USERNAME'))

    # get an environment variable from Linux
    print(sos.lenv('USER'))

    # do not use denv(), as its behavior will change depending on platform
    # instead use wenv() or lenv()
    # denv() uses the default shell
    # denv is for env what subprocess.run() is for system.shell()
    # Both Windows and Linux have a PATH variable
    print(sos.denv('PATH'))


def ex_env_03():

    title('ex_env_03')
    pass


def title(s: str):
    print('-----------------------------------------------------------------------------------------------------------')
    print(s)
    print('-----------------------------------------------------------------------------------------------------------')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
