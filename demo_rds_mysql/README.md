# Install RDS

Use the following AWS CLI command:

    $ aws rds create-db-instance --db-instance-identifier MysqlExample --db-instance-class db.t2.micro --engine MySQL --allocated-storage 5 --no-publicly-accessible --db-name ExampleDB --master-username username --master-user-password password --backup-retention-period 3

Get rds end point information

    $ aws rds describe-db-instances

### Edit RDS security group configuration

Add your ip address to inbound rule

### Install pymysql

    pip install pymysql

### Test connection
Edit connection settings in rds_mysql_connection_demo.py

    db_username = "username"
    db_password = "password"
    db_name = "ExampleDB"
    db_endpoint = "[RDS Host]"

run:

    $ python rds_mysql_connection_demo.py

Result:

    SUCCESS: Connection to RDS mysql instance succeeded
    (0, 'name_0')
    (1, 'name_1')
    ....
    (98, 'name_98')
    (99, 'name_99')
    Added 100 items to RDS MySQL table
    

After the exercise, remove the RDS instance
