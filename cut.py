#!/usr/bin/python3

import http.client
import json

from urllib.parse import urlparse

cutcode = {
    "inputs" : "meganalysis_employees",
    "query" : [
        {"map" : {
            "language" : "javascript",
            "source" : """function(v) {
  var parsedData = JSON.parse(v.values[0].data);
  parsedData.salary = parsedData.salary / 2.0;
  return [{"key" : v.key, "value" : parsedData}];
}"""}}]}

header = {"content-type" : "application/json"}
host = "http://localhost:8091/mapred"

def main():
    connection = http.client.HTTPConnection(urlparse(host).netloc)
    print("Sending request:\n" + json.dumps(cutcode))
    connection.request("POST", host, headers=header, body=json.dumps(cutcode))
    response = connection.getresponse()
    responsetext = json.loads(response.readall().decode())
    print("\nResponse:\n\tCode: %d\n\tResult:%s" % (response.code, responsetext))
    connection.close()
    print("\nWriting back results...")
    targetdb = "http://localhost:8091/riak/meganalysis_employees"
    print("targetdb: " + targetdb)
    print("Connectiong to " + urlparse(targetdb).netloc)
    connection = http.client.HTTPConnection(urlparse(targetdb).netloc)
    for elem in responsetext:
        print(elem["value"])
        targetkey = targetdb + "/%s" % (elem["key"])
        print(targetkey)
        connection.request("PUT" , targetkey,
                           headers=header, body=json.dumps(elem["value"]))
        print(connection.host)
        response = connection.getresponse()
        if not 200 <= response.code < 205:
            raise ValueError("Request returned unexpected response: %s"
                             % (response.code))
        print(response.readall())
    connection.close()

if __name__ == "__main__":
    main()
