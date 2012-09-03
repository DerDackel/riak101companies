#!/usr/bin/python3

import http.client
import json

from urllib.parse import urlparse

totalcode = {
    "inputs" : "meganalysis_employees",
    "query" : [
        {"map" : {
            "language" : "javascript",
            "source" : """function(v) {
    var parsedData = JSON.parse(v.values[0].data);
    return [{'salary' : parsedData.salary}];
}"""
        }
        },
        {"reduce" : {"language" : "javascript",
                    "source" : """function(mappedVals) {
    var sums = {'salary' : 0};
    for (var i in mappedVals) {
        sums.salary += mappedVals[i].salary;
    }
    return [sums];
}"""}}]}

header = {"content-type" : "application/json"}
host = "http://localhost:8091/mapred"


def main():
    connection = http.client.HTTPConnection(urlparse(host).netloc)
    print("Sending request:\n" + json.dumps(totalcode))
    connection.request("POST", host, headers=header, body=json.dumps(totalcode))
    response = connection.getresponse()
    responsetext = json.loads(response.readall().decode())
    print("\nResponse:\n\tCode: %d\n\tResult:%s" % (response.code, responsetext))
    connection.close()

if __name__ == "__main__":
    main()
