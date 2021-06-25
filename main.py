import graphql as gql


def main():

    # rick and morty graphql api queries
    example_01()

    # spacex graphql api queries
    example_02()


def example_01():

    url = 'https://rickandmortyapi.com/graphql/'
    qs = gql.load('./queries/rick_and_morty.gql')

    gql.pquery(url, qs['info'])
    gql.pquery(url, qs['name'])
    gql.pquery(url, qs['status'])
    # gql.pquery(url, qs['status'], verbose=False)


def example_02():

    url = 'https://api.spacex.land/graphql/'
    qs = gql.load('./queries/spacex.gql')

    # print all available queries
    # gql.pqueries(qs)

    r = gql.query(url, qs['name'])
    gql.rprint(r)

    r = gql.query(url, qs['basics'])
    gql.rprint(r)

    r = gql.query(url, qs['verbose'])
    gql.rprint(r)
    # gql.rprint(r, verbose=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

