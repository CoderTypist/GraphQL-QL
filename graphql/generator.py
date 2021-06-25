import filio
import re


def load(file_path: str) -> dict:

    with open(file_path, 'r') as file:

        # read in all text
        str_queries = filio.str_file(file_path)

        # separate individual queries
        str_queries = str_queries.split('query_')

        # if the first element is None, remove it
        if not str_queries[0]:
            str_queries = str_queries[1::]

        # remove any leading or trailing whitespace for each query
        str_queries = [_.strip() for _ in str_queries]

    # compile regular expression to extract query name
    re_get_query_name = re.compile(r"^.*?(?=[\s])")

    # What does the regex do?:
    #     - match with characters leading up to the first space
    #
    # Explained:
    #   .*       ==> match with anything
    #   (?=[\s]) ==> positive look ahead, must end with a space
    #   *?       ==> shortest pattern match (do not do greedy matching)

    queries: dict = {}

    for q in str_queries:

        # get query name
        m = re_get_query_name.match(q)
        name = m.group(0)

        # change query name to say 'query'
        q = re.sub(name, 'query', q, count=1)

        # add the name/query pair to the dict
        queries[name] = q

    return queries


def pqueries(queries: dict):

    for k in queries.keys():
        print('-----------------------------------------------------')
        print('{}:'.format(k))
        print(queries[k])
