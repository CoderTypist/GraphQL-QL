import graphql as gql
from graphql import GraphQL
import pprint
import requests
import subprocess
import system as sos


def main():

    # rick and morty graphql api query
    # - queries are stored in strings
    # - does not use GraphQL-QL
    # ex_gql_01()

    # rick and morty graphql api query
    # - queries are stored in strings
    # - uses GraphQL-QL
    # ex_gql_02()

    # rick and morty graphql api queries
    # - queries are in a separate .gql file
    # - uses GraphQL-QL
    # ex_gql_03()

    # spacex graphql api queries
    # - queries are in a separate .gql file
    # - uses GraphQL-QL
    # ex_gql_04()

    # loads, formats, and prints queries from .gql files
    # - uses GraphQL-QL
    # ex_gql_05()

    ex_gql_06()

    # execute shell commands
    # - uses system.shell()
    # - more robust than subprocess.run()
    # ex_shell()

    # get environment variables through desired shell/platform
    # ex_env()


def ex_gql_01():

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
    pprint.pprint(r.json())

    r = requests.post(url, json={'query': query_status})
    pprint.pprint(r.json())

    r = requests.post(url, json={'query': query_info})
    pprint.pprint(r.json())


def ex_gql_02():

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

    api = GraphQL('https://rickandmortyapi.com/graphql/')
    qs = gql.load('./queries/rick_and_morty.gql')

    api.pquery(qs['name'])
    api.pquery(qs['status'])
    api.pquery(qs['info'])


def ex_gql_04():

    api = GraphQL('https://api.spacex.land/graphql/')
    qs = gql.load('./queries/spacex.gql')

    # print all available queries
    # gql.pqueries(qs)

    r = api.query(qs['name'])
    gql.rprint(r)

    r = api.query(qs['basics'])
    gql.rprint(r)

    r = api.query(qs['verbose'])
    gql.rprint(r)
    # gql.rprint(r, verbose=False)


def ex_gql_05():
    gql.pqueries(gql.load('./queries/rick_and_morty.gql'), title='RICK AND MORTY:')
    gql.pqueries(gql.load('./queries/spacex.gql'), title='SPACEX:')


def ex_gql_06():
    api = GraphQL('https://rickandmortyapi.com/graphql/')
    print(api.types)
    print(api.type_fields("Episodes"))
    pprint.pprint(api.all_types_all_fields(waiter=True, omit_introspective=True))


def ex_shell():
    print(sos.shell(sos.WINDOWS, ['dir'], tab=True, verbose=True))
    print(sos.shell(sos.CMD, ['dir'], tab=True, verbose=True))
    print(sos.shell(sos.POWERSHELL, ['ls'], tab=True, verbose=True))
    print(sos.shell(sos.WSL, ['ls', '-la'], tab=True, verbose=True))
    print(sos.shell(sos.LINUX, ['ls', '-la'], tab=True, verbose=True))


def ex_env():
    print(sos.env(sos.WINDOWS, 'USERNAME'))
    print(sos.env(sos.CMD, 'USERNAME'))
    print(sos.env(sos.POWERSHELL, 'USERNAME'))
    print(sos.env(sos.WSL, 'WSL_DISTRO_NAME'))
    print(sos.env(sos.LINUX, 'USER'))

    # do not use, as its behavior will change depending on platform
    # denv() uses the default shell
    # denv is for env what subprocess.run() is for system.shell()
    # Both Windows and Linux have a PATH variable
    print(sos.denv('PATH'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
