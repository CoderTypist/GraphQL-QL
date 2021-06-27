# GraphQL-QL (GraphQL Query Loader)

### Description
GraphQL-QL makes it easier to query GraphQL APIs and write cleaner code.
Load queries from a .gql file into a Python dictionary. 
Add comments to your queries by starting lines with a '#'.

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

### Comments
Add comments directly inside queries by starting lines with '#'.
```
# get student grades
query_grades {
    # computer science students
    student {
        name
        id
        # grades are between 0 and 100
        test {
            date
            grade
        }
    }
}
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

This is not pleasant to look at and is somewhat difficult to read. 
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
The primary drawback to this approach is that the purpose of the query is not apparent in the code. Anybody reading the code would need to refer to the .gql file to see what the queries do.

##### Query Modification
Another potential drawback is query modification. If a query is modified or renamed after initially being used in the code the behavior of the code may change without anybody noticing. 