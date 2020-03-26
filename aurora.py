import boto3
import json

create_table_sql = """
CREATE TABLE example_table(
    id INT,
    val1 TEXT,
    PRIMARY KEY( id )
);
"""

insert_sql = """
INSERT INTO example_table
    VALUES (1, 'valueOne');
"""

select_sql = """
SELECT * FROM example_table
"""

def pprint(j):
    print(json.dumps(j, indent=4))


def convert_type(record_dict):
    if "arrayValue" in record_dict:
        raise NotImplementedError("Converter cannot currently handle array types")

    if "isNull" in record_dict:
        return None

    if "stringValue" in record_dict:
        return record_dict["stringValue"]
    elif "blobValue" in record_dict:
        assert isinstance(record_dict["blobValue"], bytes)
        return record_dict["blobValue"]
    elif "booleanValue" in record_dict:
        assert isinstance(record_dict["booleanValue"], bool)
        return record_dict["booleanValue"]
    elif "doubleValue" in record_dict:
        assert isinstance(record_dict["doubleValue"], (float, str))
        return float(record_dict["doubleValue"])
    elif "longValue" in record_dict:
        assert isinstance(record_dict["longValue"], (int, str))
        return int(record_dict["longValue"])




def parse_query_result(response):
    assert "columnMetadata" in response.keys(), "Cannot automatically parse query results without metadata about the " \
                                                "columns. Make sure your query has includeResultMetadata=True"
    headers = [col_meta["name"] for col_meta in response["columnMetadata"]]
    result_rows = []
    for row in response["records"]:
        result_row = []
        for cell in row:
            result_row.append(convert_type(cell))
        result_rows.append(result_row)
    return headers, result_rows




if __name__ == '__main__':
    DB_ARN = "arn:aws:rds:us-west-2:664043321167:cluster:magnet-serverless"
    SECRET_ARN = "arn:aws:secretsmanager:us-west-2:664043321167:secret:rds-db-credentials/cluster-3FQXKG45SDFMZIKYOMCDN5KNGI/postgres-aip5D2"
    client = boto3.client('rds-data')


    response = client.execute_statement(
            continueAfterTimeout=True,
            database='testdb',
            includeResultMetadata=True,
            resourceArn=DB_ARN,
            secretArn=SECRET_ARN,
            sql=select_sql,
    )

    # print(json.dumps(response, indent=4))
    headers, result_rows = parse_query_result(response)
    print(headers)
    print()
    for row in result_rows:
        print(row)
