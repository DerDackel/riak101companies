#!/usr/bin/env python3

import json
import os
import http.client

from urllib.parse import urlparse

EMPLOYEES = {
    "craig" : {"salary": 123456, "name": "Craig", "address": {"city": "Redmond", "country": "USA"}},
    "ralf" : {"salary": 1234, "name": "Ralf", "address": {"city": "Koblenz", "country": "Germany"}},
    "ray" : {"salary": 234567, "name": "Ray", "address": {"city": "Redmond", "country": "USA"}},
    "klaus" : {"salary": 23456, "name": "Klaus", "address": {"city": "Boston", "country": "USA"}},
    "karl" : {"salary": 2345, "name": "Karl", "address": {"city": "Riga", "country": "Latvia"}},
    "joe" : {"salary": 2344, "name": "Joe", "address": {"city": "Wifi City", "country": "The Metaverse"}},
    "erik" : {"salary": 12345, "name": "Erik", "address": {"city": "Utrecht", "country": "Netherlands"}}
}

DEPTS = {
    "research" : {"name": "Research"},
    "development" : {"name": "Development"},
    "dev1" : {"name": "Dev1"},
    "dev1.1" : {"name" : "Dev1.1"}
}

LINKS = {
    "dev1.1" : [("employs", "meganalysis_employees/joe")],
    "research" : [("employs", "meganalysis_employees/ralf"), ("employs", "meganalysis_employees/erik"), ("employs", "meganalysis_employees/craig")],
    "development" : [("employs", "meganalysis_employees/ray"), ("has_subunit", "meganalysis_depts/dev1")],
    "dev1" : [("employs", "meganalysis_employees/klaus"), ("has_subunit", "meganalysis_depts/dev1.1")],
    "craig" : [("manages", "meganalysis_depts/research")],
    "ray" : [("manages", "meganalysis_depts/development")],
    "klaus" : [("manages", "meganalysis_depts/dev1")],
    "karl" : [("manages" , "meganalysis_depts/dev1.1")]
}

HOST = "http://localhost:8091"

def put_entry(bucket, key, value):
    targeturl = urlparse("{0}/riak/{1}/{2}?returnbody=true".format(HOST, bucket, key))
    print(targeturl.netloc)
    connection = http.client.HTTPConnection(targeturl.netloc)
    headers = {
        "content-type" : "application/json",
    }
    links = []
    if LINKS.get(key):
        for rel, target in LINKS[key]:
            links.append(
                '</riak/{0}>; riaktag="{1}"'.format(
                    target, rel))
            headers["Link"] = ", ".join(links)
            print(headers)
    connection.request("PUT", targeturl.geturl(),
                       headers = headers,
                       body = json.dumps(value))
    return connection.getresponse().code


def main():
    for e, v in EMPLOYEES.items():
        code = put_entry("meganalysis_employees", e, v)
        print("Put {0} into DB - Returned {1}".format(e, code))
    for d, v in DEPTS.items():
        code = put_entry("meganalysis_depts", d, v)
        print("Put {0} into DB - Returned {1}".format(d, code))

if __name__ == "__main__":
    main()
