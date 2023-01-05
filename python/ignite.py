from pyignite import Client

test_table = 'test'
test_insert_query = '''INSERT INTO test(Code, Name) VALUES (?, ?)'''

test_create_table = '''CREATE TABLE test (
    Code CHAR(10) PRIMARY KEY,
    Name CHAR(52),
)'''

test_data = [
    [
        'snap1', 'United States1',
    ],
    [
        'snap2', 'CHINA1',
    ],
    [
        'new1', 'newdata1',
    ],
    [
        'new2', 'newdata2',
    ],
]

DROP_TABLE_QUERY = '''DROP TABLE {} IF EXISTS'''

DROP_TABLE_DATA_QUERY = '''TRUNCATE TABLE {}'''



client = Client()
#端口10800
with client.connect('10.2.17.192', 31138):



    #查询缓存列表
    cashe = client.get_cache_names()
    print(cashe)

    #建表
    for query in [
        test_create_table,
    ]:
        client.sql(query)

    # #插入数据
    for row in test_data:
        client.sql(test_insert_query, query_args=row)
    update_sql = '''UPDATE test SET Name = 'update_name' WHERE Code = 'snap2';'''
    delete_sql = '''DELETE FROM test  WHERE Code = 'snap2';'''
    result = client.sql(delete_sql)
    #查询数据
    SQL = '''select * from test'''

    with client.sql(SQL) as cursor:
        print('data:')
        for row in cursor:
            print(row)

    # clean up
    for table_name in [
        test_table,
    ]:
        result = client.sql(DROP_TABLE_QUERY.format(table_name))


    for table_name in [
        test_table,
    ]:
        result = client.sql(DROP_TABLE_DATA_QUERY.format(table_name))
