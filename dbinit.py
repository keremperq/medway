import os
import sys
import psycopg2 as dbapi2


INIT_STATEMENTS = [
    #"DROP SCHEMA public CASCADE;CREATE SCHEMA public;",

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
        UPDATED_TIME      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """,
        
    """CREATE TABLE IF NOT EXISTS EQ_CASE (
        CASE_TYPE     VARCHAR(50),
        HAS_AUDIO     VARCHAR(20),
        IS_TRANSPARENT  VARCHAR(20),
        HAS_PSU         VARCHAR(20),
        EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS EQ_COOLER (
        COOLER_TYPE     VARCHAR(50),
        COOLER_SIZE     VARCHAR(50),
        LED_COLOR       VARCHAR(20),
        EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID)
    )
    """,   
        
    """
    CREATE TABLE IF NOT EXISTS EQ_HEADSET (
        USAGE_AREA    VARCHAR(50),
        HEADSET_TYPE  VARCHAR(50),
        HAS_MIC       VARCHAR(20),
        EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID)
    )
    """,   
        
    """
    CREATE TABLE IF NOT EXISTS EQ_KEYBOARD (
        KEYBOARD_TYPE    VARCHAR(50),
        KEY_SEQUENCE     VARCHAR(20),
        IS_MECHANIC      VARCHAR(20),
        IS_RGB           VARCHAR(20),
        EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID)
    )
    """,  

    """
    CREATE TABLE IF NOT EXISTS EQ_MONITOR (
        SCREEN_SIZE    VARCHAR(20),
        RESOLUTION     VARCHAR(20),
        REFRESH_RATE   VARCHAR(20),
        EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS EQ_MOTHERBOARD (
        RAM_TYPE            VARCHAR(50),
        MAX_RAM             VARCHAR(20),
        RAM_SLOT_NUMBER     SMALLINT,
        SOCKET_TYPE         VARCHAR(20),
        RAM_FRE_SPEED       VARCHAR(50),
        EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS EQ_MOUSE (
        MOUSE_TYPE     VARCHAR(50),
        DPI            VARCHAR(20),
        BUTTONS        SMALLINT,
        EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS EQ_POWERSUPPLY (
        POWER_W     VARCHAR(30),
        POWER_TYPE     VARCHAR(30),
        SATA_CONNECTION  VARCHAR(30),
        EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS EQ_PROCESSOR (
        MODEL     VARCHAR(30),
        FRE_SPEED     VARCHAR(20),
        CORE_NUMBER  SMALLINT,
        EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID)
    )
    
    """,

    """
    CREATE TABLE IF NOT EXISTS EQ_RAM (
        RAM_TYPE     VARCHAR(50),
        CAPACITY     VARCHAR(20),
        FRE_SPEED    VARCHAR(20),
        EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS EQ_VIDEOCARD (
        MEMORY_SIZE     VARCHAR(20),
        CORE_SPEED      VARCHAR(20),
        GPU_MODEL       VARCHAR(50),
        MANUFACTURER    VARCHAR(20),
        EQ_ID         INTEGER REFERENCES EQUIPMENT (EQ_ID)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS TRANSACTION (
        TRANSACTION_ID           SERIAL PRIMARY KEY,
        CUSTOMER_ID              INTEGER REFERENCES CUSTOMER (CUSTOMER_ID),
        ADDRESS_ID               INTEGER REFERENCES ADDRESS (ADDRESS_ID) DEFAULT NULL,
        TRANSACTION_EXPLANATION  VARCHAR(200) DEFAULT NULL,
        TRANSACTION_TIME         TIMESTAMP DEFAULT NULL,
        PAYMENT_TYPE             VARCHAR(30) DEFAULT NULL,
        IS_COMPLETED             BOOLEAN DEFAULT FALSE
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS SUPPLIER (
        SUPP_ID     SERIAL PRIMARY KEY,
        SUPPLIER_NAME     VARCHAR(50),
        SUPP_PHONE        CHAR(10) UNIQUE NOT NULL,
        SUPP_ADDRESS    VARCHAR(200)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS PRODUCT (
        EQ_ID                INTEGER REFERENCES EQUIPMENT(EQ_ID),
        REMAINING            SMALLINT NOT NULL DEFAULT 0,
        PRICE                FLOAT,
        NUMBER_OF_SELLS      SMALLINT DEFAULT 0,
        EXPLANATION          VARCHAR(500),
        IS_ACTIVE            BOOLEAN DEFAULT TRUE,
        SUPP_ID              INTEGER REFERENCES SUPPLIER (SUPP_ID),
        PRIMARY KEY          (EQ_ID)
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
    )""",

     "INSERT INTO CATEGORY (CAT_NAME) VALUES ('Case')",
     "INSERT INTO CATEGORY (CAT_NAME) VALUES ('Cooler')",
     "INSERT INTO CATEGORY (CAT_NAME) VALUES ('Headset')",
     "INSERT INTO CATEGORY (CAT_NAME) VALUES ('Keyboard')",
     "INSERT INTO CATEGORY (CAT_NAME) VALUES ('Monitor')",
     "INSERT INTO CATEGORY (CAT_NAME) VALUES ('Motherboard')",
     "INSERT INTO CATEGORY (CAT_NAME) VALUES ('Mouse')",
     "INSERT INTO CATEGORY (CAT_NAME) VALUES ('Powersupply')",
     "INSERT INTO CATEGORY (CAT_NAME) VALUES ('Processor')",
     "INSERT INTO CATEGORY (CAT_NAME) VALUES ('Ram')",
     "INSERT INTO CATEGORY (CAT_NAME) VALUES ('Videocard')",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('Strix Helios Tempered Glass RGB USB 3.1 Mid Tower Case', 'ASUS', '',1)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('PowerBoost RGB Gaming Case', 'POWER BOOST', '',1)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('Hyper 212 Spectrum Rainbow LED', 'COOLER MASTER', '',2)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('ASUS ROG RYUO 240 RGB', 'ASUS', '',2)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('Corsair Void Elite RGB 7.1 Surround Black Gaming', 'CORSAIR', '',3)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('Razer Hammerhead True Wireless Headset', 'RAZER', '',3)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('XPG Summoner Cherry Mx Blue RGB Gaming Keyboard', 'XPG', '',4)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('Logitech G G512 GX Brown RGB Gaming Keyboard', 'LOGITECH', '',4)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('Alienware AW2521HF 240Hz FHD IPS Freesync G-sync Gaming Monitor', 'ALIENWARE', '',5)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('ASUS 27inch VG278QF 165Hz 0.5ms DVI-D Gaming Monitor', 'ASUS', '',5)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('ASUS PRIME B550M-A (WI-FI) 4600MHz(OC) DDR4 Motherboard', 'ASUS', '',6)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('GIGABYTE B450M S2H V2 3600MHz(OC) DDR4 Socket AM4', 'GIGABYTE', '',6)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('ASUS ROG GLADIUS II ORIGIN MS For Bundle Aura Sync Fps Gaming Mouse', 'ASUS', '',7)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('Steelseries Sensei Ten RGB Gaming Mouse', 'STEELSERIES', '',7)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('SHARKOON SHP650 V2 650W 80+ 120mm PSU', 'SHARKOON', '',8)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('SHARKOON WPM GOLD ZERO 650W 80+ Gold Moduler 140mm PSU', 'SHARKOON', '',8)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('INTEL Core i3 10100F 3.60GHz 1200 14nm', 'INTEL', '',9)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('AMD RYZEN 5 5600X 3.7GHz 32MB AM4 7nm Processor', 'AMD', '',9)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('XPG 8GB Gammix D30 Red 3000MHz CL16 DDR4 Single Kit Ram', 'XPG', '',10)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('HYPERX 16GB Fury RGB 3200MHz CL16 DDR4 Single Kit Ram', 'HYPERX', '',10)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('GIGABYTE GeForce RTX 3090 AORUS xtreme 24GB GDDR6X', 'GIGABYTE', '',11)",
     "INSERT INTO EQUIPMENT (EQ_NAME, EQ_BRAND, EQ_IMAGE, CAT_ID) VALUES ('SAPPHIRE RX 550 PULSE OC 4GB GDDR5 128Bit DX12', 'SAPPHIRE', '',11)",
     "INSERT INTO EQ_CASE (CASE_TYPE, HAS_AUDIO, IS_TRANSPARENT, HAS_PSU, EQ_ID) VALUES ('ATX Mid Tower','Yes','Yes',1)",
     "INSERT INTO EQ_CASE (CASE_TYPE, HAS_AUDIO, IS_TRANSPARENT, HAS_PSU, EQ_ID) VALUES ('ATX Mid Tower','Yes','No',2)",
     "INSERT INTO EQ_COOLER (COOLER_TYPE, COOLER_SIZE, LED_COLOR, EQ_ID) VALUES ('Air Cooler','120mm','Multi Color',3)",
     "INSERT INTO EQ_COOLER (COOLER_TYPE, COOLER_SIZE, LED_COLOR, EQ_ID) VALUES ('Liquid Cooling','120mm','Multi Color',4)",
     "INSERT INTO EQ_HEADSET (USAGE_AREA, HEADSET_TYPE, HAS_MIC, EQ_ID) VALUES ('Gaming','On-ear','Yes',5)",
     "INSERT INTO EQ_HEADSET (USAGE_AREA, HEADSET_TYPE, HAS_MIC, EQ_ID) VALUES ('Music & Entertainment','In-ear','Yes',6)",
     "INSERT INTO EQ_KEYBOARD (KEYBOARD_TYPE, KEY_SEQUENCE, IS_MECHANIC, IS_RGB, EQ_ID) VALUES ('Wired','Turkish Q','Yes', 'Yes',7)",
     "INSERT INTO EQ_KEYBOARD (KEYBOARD_TYPE, KEY_SEQUENCE, IS_MECHANIC, IS_RGB, EQ_ID) VALUES ('Wireless','Turkish Q','No', 'Yes',8)",
     "INSERT INTO EQ_MONITOR (SCREEN_SIZE, RESOLUTION, REFRESH_RATE, EQ_ID) VALUES ('24.5 inch','1920 x 1080','240 Hz',9)",
     "INSERT INTO EQ_MONITOR (SCREEN_SIZE, RESOLUTION, REFRESH_RATE, EQ_ID) VALUES ('27 inch','1920 x 1080','165 Hz',10)",
     "INSERT INTO EQ_MOTHERBOARD (RAM_TYPE, MAX_RAM, RAM_SLOT_NUMBER, SOCKET_TYPE, RAM_FRE_SPEED, EQ_ID) VALUES ('DDR4','128 GB',4,'AM4', '4600 MHz, 4400 MHz',11)",
     "INSERT INTO EQ_MOTHERBOARD (RAM_TYPE, MAX_RAM, RAM_SLOT_NUMBER, SOCKET_TYPE, RAM_FRE_SPEED, EQ_ID) VALUES ('DDR4','32 GB',2,'AM4', '3600 MHz, 3466 MHz',12)",
     "INSERT INTO EQ_MOUSE (MOUSE_TYPE, DPI, BUTTONS, EQ_ID) VALUES ('Wired','12000 Dpi',6,13)",
     "INSERT INTO EQ_MOUSE (MOUSE_TYPE, DPI, BUTTONS, EQ_ID) VALUES ('Wired','18000 Dpi',8,14)",
     "INSERT INTO EQ_POWERSUPPLY (POWER_W, POWER_TYPE, SATA_CONNECTION, EQ_ID) VALUES ('650W','ATX',4,15)",
     "INSERT INTO EQ_POWERSUPPLY (POWER_W, POWER_TYPE, SATA_CONNECTION, EQ_ID) VALUES ('650W','ATX',9,16)",
     "INSERT INTO EQ_PROCESSOR (MODEL, FRE_SPEED, CORE_NUMBER, EQ_ID) VALUES ('Core i3','3.6 GHz',4,17)",
     "INSERT INTO EQ_PROCESSOR (MODEL, FRE_SPEED, CORE_NUMBER, EQ_ID) VALUES ('Ryzen 5','3.7 GHz',6,18)",
     "INSERT INTO EQ_RAM (RAM_TYPE, CAPACITY, FRE_SPEED, EQ_ID) VALUES ('DDR4','8GB','3000 MHz',19)",
     "INSERT INTO EQ_RAM (RAM_TYPE, CAPACITY, FRE_SPEED, EQ_ID) VALUES ('DDR4','16GB','3200 MHz',20)",
     "INSERT INTO EQ_VIDEOCARD (MEMORY_SIZE, CORE_SPEED, GPU_MODEL, MANUFACTURER, EQ_ID) VALUES ('24GB','1695 MHz','GeForce RTX 3090', 'NVIDIA',21)",
     "INSERT INTO EQ_VIDEOCARD (MEMORY_SIZE, CORE_SPEED, GPU_MODEL, MANUFACTURER, EQ_ID) VALUES ('4GB','1206 MHz','Radeon RX 550', 'AMD',22)",
     "INSERT INTO ADDRESS (ADDRESS_NAME, COUNTRY, CITY, NEIGHBORHOOD, STREET, ADDRESS_NO, ZIPCODE, EXPLANATION) VALUES ('Home', 'Turkey', 'Kirikkale', 'Yeni Mahalle', 'Zafer Cad', 15, '71100', 'adress_1' )",
     "INSERT INTO ADDRESS (ADDRESS_NAME, COUNTRY, CITY, NEIGHBORHOOD, STREET, ADDRESS_NO, ZIPCODE, EXPLANATION) VALUES ('Home', 'Turkey', 'Ankara', 'Etlik', 'Halil Erkut Cad', 3, '06000', 'adress_2' )",
     "INSERT INTO CUSTOMER (CUSTOMER_NAME, SURNAME, USERNAME, IS_ACTIVE, EMAIL, PHONE, PASSWORD, ADDRESS_ID) VALUES ('Kerem Berk', 'Guclu', 'admin', TRUE, 'email1@itu.edu.tr', '2475245514', '$pbkdf2-sha256$29000$PIdwDqH03hvjXAuhlLL2Pg$B1K8TX6Efq3GzvKlxDKIk4T7yJzIIzsuSegjZ6hAKLk', 1)",
     "INSERT INTO CUSTOMER (CUSTOMER_NAME, SURNAME, USERNAME, IS_ACTIVE, EMAIL, PHONE, PASSWORD, ADDRESS_ID) VALUES ('Ahmet', 'Yilmaz', 'ahmet123', FALSE, 'email2@itu.edu.tr', '2475246514', '$pbkdf2-sha256$29000$PIdwDqH03hvjXAuhlLL2Pg$B1K8TX6Efq3GzvKlxDKIk4T7yJzIIzsuSegjZ6hAKLk', 2)",
     "INSERT INTO COMMENT (CUSTOMER_ID, EQ_ID, COMMENT_TITLE, COMMENT_STATEMENT, ADDED_TIME, UPDATED_TIME) VALUES (1, 1, 'Teslimat', 'Urun kargoya gec verildi.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
     "INSERT INTO COMMENT (CUSTOMER_ID, EQ_ID, COMMENT_TITLE, COMMENT_STATEMENT, ADDED_TIME, UPDATED_TIME) VALUES (2, 2, 'Mukemmel', 'Urun bekledigim gibiydi.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
     "INSERT INTO SUPPLIER (SUPPLIER_NAME, PHONE, SUPP_ADDRESS) VALUES ('MEDWAY', '5151223456', 'Osmanli Cad. 372/3. Sok. No:9 Meydan Mah. Kecioren, Ankara')",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 3, 999, 'Product explanation 1', TRUE, 1, 1)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 4, 999, 'Product explanation 2', TRUE, 1, 2)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 5, 999, 'Product explanation 3', TRUE, 1, 3)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 6, 999, 'Product explanation 4', FALSE, 1, 4)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 7, 999, 'Product explanation 5', TRUE, 1, 5)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 8, 999, 'Product explanation 6', TRUE, 1, 6)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 9, 999, 'Product explanation 7', TRUE, 1, 7)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 10, 999, 'Product explanation 8', TRUE, 1, 8)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 11, 999, 'Product explanation 9', FALSE, 1, 9)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 12, 999, 'Product explanation 10', TRUE, 1, 10)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 13, 999, 'Product explanation 11', TRUE, 1, 11)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 14, 999, 'Product explanation 12', TRUE, 1, 12)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 15, 999, 'Product explanation 13', TRUE, 1, 13)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 16, 999, 'Product explanation 14', TRUE, 1, 14)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 17, 999, 'Product explanation 15', FALSE, 1, 15)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 18, 999, 'Product explanation 16', TRUE, 1, 16)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 19, 999, 'Product explanation 17', TRUE, 1, 17)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 20, 999, 'Product explanation 18', FALSE, 1, 18)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 21, 999, 'Product explanation 19', TRUE, 1, 19)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 22, 999, 'Product explanation 20', TRUE, 1, 20)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 23, 999, 'Product explanation 21', TRUE, 1, 21)",
     "INSERT INTO PRODUCT (REMAINING, PRICE, NUMBER_OF_SELLS, EXPLANATION, IS_ACTIVE, SUPP_ID, EQ_ID) VALUES (999, 24, 999, 'Product explanation 22', TRUE, 1, 22)",
     "INSERT INTO TRANSACTION (CUSTOMER_ID) VALUES (1)",
     "INSERT INTO TRANSACTION (CUSTOMER_ID) VALUES (2)"
]

def initialize(url2):
    with dbapi2.connect(url2) as connection:
        with connection.cursor() as cursor:
            for statement in INIT_STATEMENTS:
                print("SQL Run:", statement)
                cursor.execute(statement)
            
if __name__ == "__main__":

    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)