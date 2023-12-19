from psycopg import Connection

from virtual_school_backend.config import DSN


CREATE_ENUM_USERROLE = """
    CREATE TYPE UserRole 
        AS ENUM (
            'admin',
            'teacher',
            'user'
    );
""", 'creating enum UserRole...'

CREATE_LOGIN_TABLE = """
    CREATE TABLE login (
        id serial,
        user_id integer,
        role UserRole NOT NULL,
        email text NOT NULL,
        password text NOT NULL,
        created timestamptz,
        last_activity timestamptz,

        PRIMARY KEY ( id ),
        UNIQUE ( email )
    );
""", 'creating login table...'

CREATE_TOKENS_TABLE = """
    CREATE TABLE tokens (
        login_id bigserial,
        token text NOT NULL,

        PRIMARY KEY ( login_id, token ),
        FOREIGN KEY ( login_id ) REFERENCES login ( id ),
        CONSTRAINT token_not_empty CHECK ( trim( token ) <> '' )
    );
""", 'creating tokens table'

CREATE_ENUM_USERSTATE = """
    CREATE TYPE UserState
        AS ENUM (
            'new',
            'activated',
            'deleted',
            'blocked'
    );
""", 'creating enum UserState...'

CREATE_CLASSNUM_DOMAIN = """
    CREATE DOMAIN ClassNum
        AS numeric( 2 ) CHECK ( VALUE IS NOT NULL AND VALUE BETWEEN 1 AND 11);
""", 'creating ClassNum domain...'

CREATE_USER_ACCOUNT_TABLE = """
    CREATE TABLE user_account (
        id serial,
        login_id integer,
        state UserState,
        name varchar( 24 ) NOT NULL,
        secondname varchar( 24 ) NOT NULL,
        patronymic varchar( 24 ),
        phone varchar( 16 ) UNIQUE NOT NULL,
        class ClassNum,

        PRIMARY KEY ( id ),
        FOREIGN KEY ( login_id ) REFERENCES login ( id )
    );
""", 'creating user_account table...'

ALTER_LOGIN_TABLE = """
    ALTER TABLE login
        ADD FOREIGN KEY ( user_id ) REFERENCES user_account ( id );
""", 'altering login table...'

CREATE_ENUM_ATTESTATIONSUBJECT = """
    CREATE TYPE AttestationSubject
        AS ENUM (
            'russian_language', 'english_language',
            'mathematics', 'history', 'informatics',
            'music', 'physical_culture', 'literature',
            'chemestry', 'physics', 'geography'
    );
""", 'creating enum AttestationSubject...'

CREATE_ATTESTATION_TABLE = """
    CREATE TABLE attestation (
        id serial,
        subject AttestationSubject NOT NULL,
        class ClassNum,
        tests jsonb,
        created timestamptz,
        updated timestamptz,

        PRIMARY KEY ( id )
    );
""", 'creating attestation table...'

CREATE_ESTIMATION_TABLE = """
    CREATE TABLE estimation (
        id serial,
        user_id integer,
        subject AttestationSubject NOT NULL,
        class ClassNum,
        estimate numeric( 3 ),
        estimated timestamptz,

        PRIMARY KEY ( id ),
        FOREIGN KEY ( user_id ) REFERENCES user_account ( id ),
        UNIQUE ( user_id, subject, class ),
        CONSTRAINT estimate_value_check CHECK ( estimate BETWEEN 0 AND 100 )
    );
""", 'creating estimation table...'

CREATE_NOTIFICATION_TABLE = """
    CREATE TABLE notification (
        id bigserial,
        creator_id integer,
        title varchar( 128 ) NOT NULL,
        description varchar( 256 ) NOT NULL,
        body varchar( 1024 ),
        created timestamptz,
        updated timestamptz,

        PRIMARY KEY ( id ),
        FOREIGN KEY ( creator_id ) REFERENCES login ( id ),
        CONSTRAINT title_not_empty CHECK ( trim( title ) <> '' ),
        CONSTRAINT description_not_empty CHECK ( trim( description ) <> '' )
    );
""", 'creating notification table...'

CREATE_USER_NOTIFICATON_TABLE = """
    CREATE TABLE user_notification (
        id bigserial,
        user_id integer,
        notification_id bigint,
        class ClassNum,

        PRIMARY KEY ( id ),
        FOREIGN KEY ( user_id ) REFERENCES user_account ( id ),
        FOREIGN KEY ( notification_id ) REFERENCES notification ( id )
    );
""", 'creating user_notification table...'

CREATE_NEWS_TABLE = """
    CREATE TABLE news (
        id bigserial,
        creator_id integer,
        title varchar( 128 ) NOT NULL,
        description varchar( 256 ) NOT NULL,
        body varchar( 1024 ),
        image_path text,
        created timestamptz,
        updated timestamptz,

        PRIMARY KEY ( id ),
        FOREIGN KEY ( creator_id ) REFERENCES login ( id ),
        CONSTRAINT title_not_empty CHECK ( trim( title ) <> '' ),
        CONSTRAINT description_not_empty CHECK ( trim( description ) <> '' )
    );
""", 'creating news table...'


commands = [
    CREATE_ENUM_USERROLE,
    CREATE_LOGIN_TABLE,
    CREATE_TOKENS_TABLE,
    CREATE_ENUM_USERSTATE,
    CREATE_CLASSNUM_DOMAIN,
    CREATE_USER_ACCOUNT_TABLE,
    ALTER_LOGIN_TABLE,
    CREATE_ENUM_ATTESTATIONSUBJECT,
    CREATE_ATTESTATION_TABLE,
    CREATE_ESTIMATION_TABLE,
    CREATE_NOTIFICATION_TABLE,
    CREATE_USER_NOTIFICATON_TABLE,
    CREATE_NEWS_TABLE,
]

def main():
    with Connection.connect(DSN) as conn:
        with conn.cursor() as cur:
            
            for command, desc in commands:
                #  TODO: add logging!!
                print(desc)
                cur.execute(command)
    
        conn.commit()
