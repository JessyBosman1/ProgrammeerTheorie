# Algoritmes en experimentatie bij B
Aangezien er bij A uitkwam dat het hoogste aantal parcel door ons gevonden uitkwam op 84, hebben wij bij B enkel de kosten berekend die hier bij horen. Door de hillclimber van A zijn er 308 verschillende combinaties van parcels gevonden die op 84 parcels totaal uitkwamen. De laagste kosten hiervan waren: $1682797850 met de algemene fuel to weight waardes en $1687870000. 

# Algoritmes en experimentatie bij C
Bij C doe je eigenlijk hetzelfde als bij A en B, alleen met een andere cargolist. Hierdoor leek het ons logisch om alleen de hoogst uitgekomen algoritmes van A te testen. Wij hebben hierom de random en de hillclimber getest. Het random algoritme kwam uit op dat er 64 parcels mee kunnen. De hillclimber kwam uit op dat er 74 parcels mee kunnen. De kosten die hierbij horen zijn: $1699122250 en met de algemene fuel to weight waardes: $1704875900.

# Algoritmes en experimentatie bij D
Bij D hebben we eerst een random algoritme gescreven, om te kijken hoe de kosten vallen als de schepen random ingedeeld worden. Daarna hebben wij de hillclimber aangepast dat deze optimaler runt voor vraag D, aangezien wij dachten dat dit een betere oplossing kan geven. Er zijn in totaal 2 aanpassingen op de hillclimber geschreven. Echter heeft een nooit een antwoord op geleverd, ondanks dat deze 48 uur gerunt heeft. Deze resultaten kunnen wij dus niet met elkaar vergelijken.
Momenteel komt de hillclimber het goedkoopst uit:
* Random: 10 x 6 schepen sturen en 1 x 2 schepen sturen (4 schepen vliegen dus 10 keer en 2 schepen 11 keer)
* HillClimber: 8 x 6 schepen sturen en 1 x 4 schepen sturen (4 schepen vliegen 9 keer en 2 vliegen 8)
De kosten van de random zijn $33801710600.  
De kosten van de random zijn $30186023600.


# Algoritmes en experimentatie bij E
Bij E dachten wij: _wat nou als het het goedkoopste/meestoptimaal vulbare spacecraft alleen maar stuurt, en de rest niet stuurt? Zal dit goedkoper zijn?_  
Hiervoor is het algoritme randomSingleCraft.py geschreven, die berekend hoe duur het is om een spacecraft te blijven sturen, totdat de parcellist leeg is. Het bleek goedkoper te zijn dan bij vraag D.

Hierna dachten wij _wat als je probeert combinaties van schepen random stuurt?_  
Hiervoor is een algoritme geschreven dat telkens een random schip neemt, deze vult op een random manier, om vervolgens weer een random schip te vullen en zo door te gaan.

Beide algoritmes kwamen goedkoper uit als de scores bij D. 
Bij het telkens sturen van een schip werd een schip 54 keer gestuurd en waren de kosten $25893000000.  
Bij het random versturen van schepen werden er 64 schepen gestuurd die samen $31527795050 kosten.


