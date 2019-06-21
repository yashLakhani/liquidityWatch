import csv
from io import StringIO


def psql_insert_copy(table, conn, keys, data_iter):
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)


'''
from flask import jsonify
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = 'Butter'
    #search = request.args.get('q')
    some_engine = create_engine(DB_URL)

    # create a configured "Session" class
    Session = sessionmaker(bind=some_engine)

    # create a Session
    session = Session()
    q = session.query(Instrument).filter(Instrument.name.contains(search))
    print(q.all())
    results = [(mv.code, mv.name) for mv in q.all()]
    print(q.all())
    return jsonify(matching_results=results)
'''

'''
@app.route('/index', methods=['GET', 'POST'])
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # request was a POST
        app.vars['ticker'] = request.form['ticker'].upper()
        app.vars['start_year'] = request.form['year']
        try:
            int(app.vars['start_year'])
            app.vars['tag'] = 'Start year specified as %s' % app.vars['start_year']
        except ValueError:
            app.vars['start_year'] = ''
            app.vars['tag'] = 'Start year not specified/recognized'
        app.vars['select'] = [feat[q] for q in range(3) if feat[q] in request.form.values()]
        return redirect('/graph')
'''

