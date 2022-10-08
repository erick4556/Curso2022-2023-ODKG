# -*- coding: utf-8 -*-
"""Task07.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1tV5j-DRcpPtoJGoMj8v2DSqR_9wyXeiE
**Task 07: Querying RDF(s)**
"""

#!pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/resources/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""
from rdflib.plugins.sparql import prepareQuery

ns = Namespace("http://somewhere#")
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  print(s)

q1 = prepareQuery('''
  SELECT ?subject WHERE { 
    ?x rdfs:subClassOf ns:Person. 
  }
  ''',
  initNs = { "ns": ns, "rdfs": RDFS}
)

for r in g.query(q1):
  print(r)
"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**"""

for s, p, o in g.triples((None, RDF.type, ns.Person)):
  print(f"{s}")
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s2,p2,o2 in g.triples((None, RDF.type, s)):
    print(s2)
q1 = prepareQuery('''
  SELECT 
    ?x 
  WHERE { 
    ?subclass rdfs:subClassOf* ns:Person.
    ?x rdf:type ?subclass. 
        }
  ''',
  initNs = {"rdfs":RDFS, "ns":ns, "rdf":RDF}
)

for r in g.query(q1):
  print(r.x)
"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**
"""
for s,r,o in g.triples((None,RDF.type, ns.Person)):
  for s2,r2,o2 in g.triples((s,None,None)):
    print(s,r2,o2)

for s,p,o in g.triples((None,RDFS.subClassOf,ns.Person)):
    for s2,p2,o2 in g.triples((None, RDF.type, s)):
       for s3,r3,o3 in g.triples((s2,None,None)):
          print(s,r3,o3)


q1 = prepareQuery('''
  SELECT 
    ?x ?prop ?val
  WHERE { 
?clase rdfs:subClassOf* ns:Person.
?x rdf:type ?clase.
?x ?prop ?val.
    }
  ''',
  initNs = {"ns":ns, "rdf":RDF, "rdfs":RDFS}
)

for r in g.query(q1):
  print(r.x,r.prop,r.val)