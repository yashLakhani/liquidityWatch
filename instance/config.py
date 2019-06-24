API_KEYS = {'QUANDL_API_KEY':'cessVzF1i58n_sWoi-tV'}

POSTGRES_USER = 'lw_user'
POSTGRES_PWD = '1234'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_DB = 'referencedb'
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(user=POSTGRES_USER,
                                                                pw=POSTGRES_PWD,
                                                                host=POSTGRES_HOST,
                                                                port=POSTGRES_PORT,
                                                                db=POSTGRES_DB)
