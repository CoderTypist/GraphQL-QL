# GraphQL-QL (GraphQL Query Loader)

## Readme Section Outline
- GraphQL-QL Overview
- GraphQL-QL documentation
- system documentation

# GraphQL-QL Overview

### Description
GraphQL-QL makes it easier to query GraphQL APIs and write cleaner code.
Load queries from a .gql file into a Python dictionary. 

### How to Use
1) Download code
2) import graphql
3) Write queries in a separate .gql file
4) Load queries into dict using get_queries()
5) Make queries using query()

### Example

```
import graphql as gql

# load in queries from the .gql file
qs = gql.load('some-file-path/queries.gql')

# GraphQL API endpoint
url = 'https://some-url/graphql'

# make a query
r = gql.query(url, qs['name-of-query'])

# print query details
gql.rprint(r)

# make a query and print results
gql.pquery(url, qs['name-of-query'])
```


### Motivation
Making queries to a GraphQL API in Python would look something like this:

```
import pprint

def foo():

    url = 'https://some_url/graphql'

    if True:
        r = None
		
        if True:
            query_one = """"query {
                                something {
                                    attr1
                                    attr4
                                    attr7
                                }
                            }"""

            r = request.post(url, json={'query': query_one})

        else:
            query_two = """query {
                otherthing {
                    attr3
                    attr8
                }
            }"""	

            r = request.post(url, json={'query': query_two})
	
        pprint(r.json())
```

Writing queries in the code works, but it may get cluttered if there are too many queries.
What if all of the queries were moved out to a separate file?

```
query_one {
    something {
        attr1
        attr4
        attr7
    }
}

query_two {
    otherthing {
        attr3
        attr8
    }
}
```

By moving all of the queries out to a separate file, the resulting code is both easier to read and write.
```
import graphql as gql
import json

def foo():

    url = 'https://some_url/graphql'
    qs = gql.load('some_file_path/queries.gql')
	
        if True:
            r = None
		
            if True:
                r = gql.query(url, qs['one'])
            else:
                r = gql.query(url, qs['two'])
	
            pprint(r.json())
```

### Drawbacks
##### Hidden Logic
The primary drawback to this approach is that the purpose of the query is not apparent in the code.
Anybody reading the code would need to refer to the .gql file to see what the queries do.

##### Query Modification
Another potential drawback is query modification.
If a query is modified or renamed after initially being used in the code the behavior of the code may change without anybody noticing. 

# GraphQL documentation

## loader.py

### load()

_load(file_path: str) -> dict_

Loads in queries from a .gql file (extension not enforced) and saves them to a dictionary.
Instead of starting with `query {`, all queries must start with `query_<query_name> {`.

|params|description|
|---|---|
|file_path: str|File containing queries|

__returns:__ _dict:_ Dictionary where the keys are the query names and the values are the queries themselves.

### pqueries()

_pqueries(queries: dict, title=None) -> None_

|params|description|
|---|---|
|queries: dict|Dictionary of queries <name, query>|

__returns:__ _None_

## requet.py

### query()
_query(url: str, q: str) -> dict_

Makes a query to specified endpoint.

|params|description|
|---|---|
|url: str|GraphQL API endpoint|
|q: str|Query|

__returns:__ _str:_ Result of query

### is_ok()
_is\_ok(r: requests.Response) -> bool_

Returns if the request was successful.

|params|description|
|---|---|
|r: requests.Response|Query response|

__returns:__ _bool:_ True if the status code was 200, False otherwise. 

### rprint()
_rprint(r: requests.Response, verbose=True) -> None_

Prints the text from a query response.

|params|description|
|---|---|
|r: requests.Response|Query response|
|verbose=True|Prints a header and the status code|

__returns:__ _None_

### pquery()
_pquery(url: str, q: str, verbose=False) -> dict_

Runs the query and prints the response.

|params|description|
|---|---|
|url: str|GraphQL API endpoint|
|verbose=False|

# system documentation

## system.py

### get_platform()

_get\_platform() -> int_

Detect if running inside of Windows, WSL, or some other Linux distribution.

__returns:__ _int:_ _system.WINDOWS_ or _system.WSL_ or _system.LINUX_

### win_or_linux()

_win\_or\_linux() -> int_

Detect if running inside of Windows or Linux.

__returns:__ _int:_ _system.WINDOWS_ or _system.LINUX_

### win_default_shell()

_win_default_shell() -> int_

Return the default shell for Windows.

__returns:__ _int:_ The Windows default shell

### shell()

_shell(target: int, args: List, tab=False, verbose=False) -> str_

A more robust method of executing shell commands. Run shell commands with the shell of 
your choice without worrying about whether you are running your code from inside of 
CMD, PowerShell, WSL, or Linux. shell() will detect what your default shell is and
craft the appropriate call to subprocess.run()

|param|description|
|---|---|
|target: int|Target shell|
|args: List|List containing shell command|
|tab=False|Insert a tab at the beginning of each line of the output|
|verbose=False|Output source shell and target shell|

__returns:__ _str:_ Output of shell command

Ex: Making a call to WSL from inside of WSL

```
import subprocess
out = subprocess.run(['ls', '-la'], stdout.subprocess.PIPE).stdout.decode()
```

Ex: Making a call to WSL from inside of Windows
```
import subprocess
out = subprocess.run(['wsl', 'ls', '-la'], shell=True, stdout.subprocess.PIPE).stdout.decode()
```


Ex: Making a call to WSL from inside of WSL or Windows

```
import system as sos
out = sos.shell(sos.WSL, ['ls', '-la'])
```

### is_alpha()
_is\_alpha(text: str, extra: List = None) -> bool_

Checks that the text is only composed of letters.

|params|description|
|---|---|
|text: str|Text to check|
|extra: List = None|In addition to checking for letters, also include these characters|

__returns:__ _bool:_ True if the text only contains letters, False otherwise.

### env()
_env(target, var\_name) -> str_

Retrieve the value for an environment variable on the desired platform/shell.

|param|description|
|---|---|
|target: int|Target shell|
|var_name: str|Name of environment variable|
__returns:__ _str:_ Value for environment variable _var\_name_

