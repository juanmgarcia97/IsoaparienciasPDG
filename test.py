from difflib import SequenceMatcher

string1 = 'agua ligera;AGUA;MINERAL NATURAL;FONTECELTA;ENRIQUECIDA CON SOLIDARIDAD;Donamos a Aldeas Infantiles parte;del precio de la botella que ud. compra.'
string3 = 'donamos a Aldeas Infantiles parte;MINERAL NATURAL;FONTECELTA;ENRIQUECIDA CON SOLIDARIDAD;agua ligera;AGUA;del precio de la botella que ud. compra.'
string2 = 'viel;agua con colágeno;pepino y limón;635 ml / 21 oz;Bebida de agua con colágeno;y extracto de pepino sabor a limon'

print(SequenceMatcher(None, string1, string3).ratio())