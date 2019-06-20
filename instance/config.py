API_KEYS = {'QUANDL_API_KEY':'cessVzF1i58n_sWoi-tV'}

POSTGRES_USER = 'postgres'
POSTGRES_PWD = 'Jskjsn1324'
POSTGRES_HOST = 'localhost'
POSTGRES_DB = 'marketdata'
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{host}/{db}'.format(user=POSTGRES_USER,
                                                                pw=POSTGRES_PWD,
                                                                host=POSTGRES_HOST,
                                                                db=POSTGRES_DB)

