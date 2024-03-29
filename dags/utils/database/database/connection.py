
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import snowflake
def getConnection(logger,ACCOUNT,WAREHOUSE,DATABASE,ROLE,SCHEMA,USER):

    logger.info("Connection Parameters : ")
    logger.info("ACCOUNT : "+ACCOUNT)
    logger.info("WAREHOUSE : "+WAREHOUSE)
    logger.info("DATABASE : "+DATABASE)
    logger.info("ROLE : "+ROLE)
    logger.info("SCHEMA : "+SCHEMA)
    logger.info("USER : "+USER)
    pemFile =  os.path.join(os.path.expanduser('~') ,".pem",str(USER).lower()+".pem")
    with open(pemFile, "rb") as key:
        p_key= serialization.load_pem_private_key(
            key.read(),
            password=None,
            backend=default_backend()
        )
    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())
     # SF Connection 
    ctx = snowflake.connector.connect(
        user=str(USER),
        account=ACCOUNT,
        private_key=pkb,
        warehouse=WAREHOUSE,
        database=DATABASE,
        schema=SCHEMA,
        ROLE=ROLE
        )
    return ctx