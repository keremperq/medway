import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS CATEGORY (
            CAT_ID   SERIAL PRIMARY KEY,
            CAT_NAME   VARCHAR(50) UNIQUE
        )  
        """,

        """ 
        CREATE TABLE IF NOT EXISTS EQUIPMENT (
            EQ_ID           SERIAL PRIMARY KEY,
            EQ_NAME         VARCHAR(100),
            EQ_BRAND        VARCHAR(100),
            EQ_IMAGE        VARCHAR(200),
            CAT_ID          INTEGER REFERENCES CATEGORY (CAT_ID)
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS ADDRESS (
            ADDRESS_ID      SERIAL PRIMARY KEY,
            ADDRESS_NAME    VARCHAR(30),
            COUNTRY         VARCHAR(30) NOT NULL,
            CITY            VARCHAR(30) NOT NULL,
            NEIGHBORHOOD    VARCHAR(30),
            STREET          VARCHAR(30),
            ADDRESS_NO      VARCHAR(10),
            ZIPCODE         CHAR(5),
            EXPLANATION     VARCHAR(500)
        )  
        """,

        """
            CREATE TABLE IF NOT EXISTS CUSTOMER (
            CUSTOMER_ID     SERIAL PRIMARY KEY,
            CUSTOMER_NAME   VARCHAR(50) NOT NULL,
            SURNAME         VARCHAR(50) NOT NULL,
            USERNAME        VARCHAR(20) UNIQUE NOT NULL,
            IS_ACTIVE       BOOLEAN DEFAULT TRUE,
            EMAIL           VARCHAR(50) UNIQUE NOT NULL,
            PHONE           CHAR(10) UNIQUE NOT NULL,
            PASSWORD        CHAR(87) NOT NULL,
            ADDRESS_ID      INTEGER REFERENCES ADDRESS (ADDRESS_ID) UNIQUE
            
        )  
        """,

            """
            CREATE TABLE IF NOT EXISTS COMMENT (
            COMMENT_ID        SERIAL PRIMARY KEY,
            CUSTOMER_ID       INTEGER REFERENCES CUSTOMER (CUSTOMER_ID),
            EQ_ID             INTEGER REFERENCES EQUIPMENT (EQ_ID),
            COMMENT_TITLE     VARCHAR(50) NOT NULL,
            COMMENT_STATEMENT VARCHAR(500) NOT NULL,
            ADDED_TIME        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UPDATED_TIME      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        )
        """,
        
        """CREATE TABLE IF NOT EXISTS EQ_CASE (
            CASE_TYPE     VARCHAR(50),
            HAS_AUDIO     VARCHAR(20),
            IS_TRANSPARENT  VARCHAR(20),
            HAS_PSU         VARCHAR(20),
            EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID),
        )
        """,

        """CREATE TABLE IF NOT EXISTS EQ_COOLER (
            COOLER_TYPE     VARCHAR(50),
            COOLER_SIZE     VARCHAR(50),
            LED_COLOR       VARCHAR(20),
            EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID),
        )
        """,   
        
        """CREATE TABLE IF NOT EXISTS EQ_HEADSET (
            USAGE_AREA    VARCHAR(50),
            HEADSET_TYPE  VARCHAR(50),
            HAS_MIC       VARCHAR(20),
            EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID),
        )
        """,   
        
        """CREATE TABLE IF NOT EXISTS EQ_KEYBOARD (
            KEYBOARD_TYPE    VARCHAR(50),
            KEY_SEQUENCE     VARCHAR(20),
            IS_MECHANIC      VARCHAR(20),
            IS_RGB           VARCHAR(20),
            EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID),
        )
        """,  

        """CREATE TABLE IF NOT EXISTS EQ_MONITOR (
            SCREEN_SIZE    VARCHAR(20),
            RESOLUTION     VARCHAR(20),
            REFRESH_RATE   VARCHAR(20),
            EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID),
        )
        """,

        """CREATE TABLE IF NOT EXISTS EQ_MOTHERBOARD (
            RAM_TYPE            VARCHAR(50),
            MAX_RAM             VARCHAR(20),
            RAM_SLOT_NUMBER     SMALLINT,
            SOCKET_TYPE         VARCHAR(20),
            RAM_FRE_SPEED       VARCHAR(50),
            EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID),
        )
        """,

        """CREATE TABLE IF NOT EXISTS EQ_MOUSE (
            MOUSE_TYPE     VARCHAR(50),
            DPI            VARCHAR(20),
            BUTTONS        SMALLINT,
            EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID),
        )
        """,

        """CREATE TABLE IF NOT EXISTS EQ_POWERSUPPLY (
            POWER_W     VARCHAR(30),
            POWER_TYPE     VARCHAR(30),
            SATA_CONNECTION  VARCHAR(30),
            EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID),
        )
        """,

        """CREATE TABLE IF NOT EXISTS EQ_PROCESSOR (
            MODEL     VARCHAR(30),
            FRE_SPEED     VARCHAR(20),
            CORE_NUMBER  SMALLINT,
            EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID),
        )
        """,

        """CREATE TABLE IF NOT EXISTS EQ_RAM (
            RAM_TYPE     VARCHAR(50),
            CAPACITY     VARCHAR(20),
            FRE_SPEED    VARCHAR(20),
            EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID),
        )
        """,

        """CREATE TABLE IF NOT EXISTS EQ_VIDEOCARD (
            MEMORY_SIZE     VARCHAR(20),
            CORE_SPEED      VARCHAR(20),
            GPU_MODEL       VARCHAR(50),
            MANUFACTURER    VARCHAR(20),
            EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID),
        )
        """,

        """CREATE TABLE IF NOT EXISTS TRANSACTION (
            TRANSACTION_ID           SERIAL PRIMARY KEY,
            CUSTOMER_ID              INTEGER REFERENCES CUSTOMER (CUSTOMER_ID),
            ADDRESS_ID               INTEGER REFERENCES ADDRESS (ADDRESS_ID) DEFAULT NULL,
            TRANSACTION_EXPLANATION  VARCHAR(200) DEFAULT NULL,
            TRANSACTION_TIME         TIMESTAMP DEFAULT NULL,
            PAYMENT_TYPE             VARCHAR(30) DEFAULT NULL,
            IS_COMPLETED             BOOLEAN DEFAULT FALSE
        )
        """,

        """CREATE TABLE IF NOT EXISTS SUPPLIER (
            SUPP_ID     SERIAL PRIMARY KEY,
            SUPPLIER_NAME     VARCHAR(50),
            SUPP_PHONE        CHAR(10) UNIQUE NOT NULL,
            SUPP_ADDRESS    VARCHAR(200)
        )
        """,

        """CREATE TABLE IF NOT EXISTS PRODUCT (
            EQ_ID                INTEGER,
            REMAINING            SMALLINT NOT NULL DEFAULT 0,
            PRICE                FLOAT,
            NUMBER_OF_SELLS      SMALLINT DEFAULT 0,
            EXPLANATION          VARCHAR(500),
            IS_ACTIVE            BOOLEAN DEFAULT TRUE,
            SUPP_ID              INTEGER REFERENCES SUPPLIER (SUPP_ID),
            FOREIGN KEY          (EQ_ID) REFERENCES EQUIPMENT (EQ_ID),
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS TRANSACTION_PRODUCT (
            TRANSACTION_ID  INTEGER REFERENCES TRANSACTION (TRANSACTION_ID),
            PIECE           SMALLINT DEFAULT 1,
            DISCOUNT        FLOAT,
            UNIT_PRICE      FLOAT,
            EQ_ID           INTEGER,
            FOREIGN KEY     (EQ_ID) REFERENCES PRODUCT (EQ_ID),
            PRIMARY KEY     (TRANSACTION_ID, EQ_ID)
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
	create_tables()