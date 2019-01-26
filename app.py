from string import Template
from flask import Flask, url_for, render_template, request, send_file
from wikidataintegrator import wdi_core
app = Flask(__name__)


# Send SPARQL Query; Use substitute() to introduce variables.
def send_sparql(id):
    query = """
    SELECT * WHERE {
    {SELECT ?item (COUNT(DISTINCT ?wdLang) as ?WDTranslations) (GROUP_CONCAT(DISTINCT ?wdLang) as ?wdlanguages ) WHERE {
       ?item $id ?doid ;
             rdfs:label ?label .
       BIND (lang(?label) AS ?wdLang)
    }
    GROUP BY ?item ?itemLabel
    }

    {SELECT ?item ?itemLabel (COUNT(DISTINCT ?wpLang) as ?WPTranslations) (GROUP_CONCAT(DISTINCT ?wpLang) as ?wplanguages ) WHERE {
       ?item wdt:P699 ?doid .
       ?article schema:about ?item ;
                schema:inLanguage ?wpLang .
       # BIND (lang(?label) AS ?lang)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    GROUP BY ?item ?itemLabel

    }
    #FILTER (?WDTranslations != ?WPTranslations)
    BIND ((?WDTranslations - ?WPTranslations) as ?difference )
    }
    ORDER BY DESC(?WDTranslations)
    """
    query = Template(query).substitute({'id': id})

    df = wdi_core.WDItemEngine.execute_sparql_query(query, as_dataframe=True)

    # Here we only pass first 6 results for rendering
    return df.head(n=10)


# Convert header to table format
def make_header_string(row):
    base_str = ""
    for item in row:
        cell = "<th>{}</th>".format(item)
        base_str += cell

    return "<tr>{}</tr>".format(base_str)


# Convert results to table format
def make_row_string(row):
    base_str = ""
    for item in row:
        cell = "<th>{}</th><th><input type='text' name='wdname-{}'></th><th><input type='text' name='wpname-{}'></th>".format(item, item, item)
        base_str += cell

    return "<tr>{}</tr>".format(base_str)


# Main page
@app.route('/')
def default():
    return render_template('index.html')


# Results page
@app.route('/input')
def input():

    TAR = request.args['lang']
    ITEM = "itemLabel"
    wdLANGS = "wdlanguages"
    wpLANGS = "wplanguages"

    # Get user selection
    id = request.args['id']
    # Send with SPARQL query
    data = send_sparql(id)
    # Get header
    headers = [ITEM, wdLANGS, wpLANGS]
    # Print header
    str = make_header_string(headers)
    # # Print content
    # for index, row in data.iterrows():
    #     cells = []
    #     for head in headers:
    #         cells.append(row[head])
    #
    #     str += make_row_string(cells)
    item_list = []
    for index, row in data.iterrows():
        wdlang_list = row[wdLANGS].split()
        wplang_list = row[wpLANGS].split()
        flags = [0, 0]
        for l in wplang_list:
            if (l != TAR):
                continue
            else:
                flags[0] = 1
        for l in wplang_list:
            if (l != TAR):
                continue
            else:
                flags[1] = 1
        if (flags[0] == 0 or flags[1] == 0):
            str += make_row_string([row[ITEM]])
            item_list.append(row[ITEM])
    table_string = "<table>{}</table>".format(str)
    return render_template('results.html', table=table_string, item_list=item_list)


@app.route('/test')
def test():
    data = request.args
    is_wd = True
    with open('./out.csv', 'w') as file:
        name = ''
        wd_input = ''
        for k, v in data.items():
            print('{}: {}'.format(k, v))
            if is_wd:
                name = k.split('-')[1]
                wd_input = v
            else:
                wp_input = v
                file.write('{},{},{}\n'.format(name, wd_input, wp_input))
                print(f'write line {name},{wd_input},{wp_input}')
            is_wd = not is_wd
    return send_file('./out.csv', as_attachment=True, attachment_filename='input.csv')


# Allocate port 8000.
if __name__ == "__main__":
    app.run(port=8000, debug=True)
