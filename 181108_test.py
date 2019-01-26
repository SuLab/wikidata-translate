from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

language = 'english'
abbre = 'en'

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
# From https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples#Cats

# sparql.setQuery("""
# SELECT DISTINCT ?doid ?item ?label ?wpLang
# WHERE {
#    ?item wdt:P699 ?doid ;
#          rdfs:label ?label ;
#          rdfs:label ?%(a)s .
#    ?article schema:about ?item ;
#             schema:inLanguage ?wpLang .
#    FILTER (lang(?label) = ?wpLang)
#    FILTER (lang(?%(a)s) = "%(b)s")
# }
# """ % {'a': language, 'b': abbre})

sparql.setQuery("""
SELECT DISTINCT ?doid ?item ?label ?wpLang
WHERE {{
   ?item wdt:P699 ?doid ;
         rdfs:label ?label ;
         rdfs:label ?{0} .
   ?article schema:about ?item ;
            schema:inLanguage ?wpLang .
   FILTER (lang(?label) = ?wpLang)
   FILTER (lang(?{0}) = "{1}")
}}
""".format(language, abbre))


sparql.setReturnFormat(JSON)
results = sparql.query().convert()

results_df = pd.io.json.json_normalize(results['results']['bindings'])
results_df[['doid.value', 'item.value', 'label.value', 'wpLang.value']].head()





import sparql_dataframe

endpoint = "https://query.wikidata.org/sparql"

q = """
    SELECT DISTINCT ?doid ?item ?label ?wpLang

WHERE {
   ?item wdt:P699 ?doid ;
         rdfs:label ?label ;
         rdfs:label ?english .

   ?article schema:about ?item ;
            schema:inLanguage ?wpLang .
   FILTER (lang(?label) = ?wpLang)
   FILTER (lang(?english) = "en")
}
"""

df = sparql_dataframe.get(endpoint, q)
df
