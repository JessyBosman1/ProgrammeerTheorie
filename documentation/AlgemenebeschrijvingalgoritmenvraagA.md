## Brute force (bruteForceA.py)

Dit algoritme is simpelweg een brute force algoritme. Alle mogelijke volgordes worden afgegaan en de hoogst gevonden score wordt steeds opgeslagen totdat er een hoger aantal pakketten is gevonden.

Voordelen:
* Het meest optimale antwoord wordt ooit gevonden.

Nadelen:
* De hele state space doorrekenen duurt ontzettend lang.

## Random (randomA.py)

Er wordt gebruikt gemaakt van een random verdeling. Er wordt een willekeurige volgorde gegenereerd van het aantal parcels, en deze wordt over de spacecrafts verdeeld. De gegenereerde volgorde wordt toegevoegd aan iedere mogelijke volgorde van spacecrafts voordat er een nieuwe willekeurige volgorde parcels wordt gegenereerd. 

Voordelen:
* het algoritme vindt sneller een hoger antwoord dan het brute force algoritme.

Nadelen:
* Het is mogelijk dat het optimale antwoord nooit/na hele lange tijd pas wordt gevonden.
* Er is geen garantie het hoogste antwoord dat het algoritme vindt na x aantal iteraties het optimale antwoord is. 


## Random met hervulling cygnus & dragon (randomLogicA.py)

Dit algoritme is een uitbreiding op het random algoritme. In plaats van opnieuw te beginnen na elke random lijst met parcels afgewerkt te hebben gaat dit algoritme door met rekenen. De  minst "goed" gevulde schepen (de schepen met een scheve verdeling) worden leeggemaakt en de parcels uit deze schepen worden terug in de pool met nog niet gevulde parcels gestopt. Vervolgens worden deze schepen weer een x aantal keer random gevuld met de beschikbare parcels. De minst gevulde schepen zijn over het algemeen Cygnus en Dragon. 

Voordelen:
* Vindt (over het algemeen) sneller hoge antwoorden dan Random.

Nadelen:
* Geen garantie dat het hoogst mogelijke antwoord gevonden is.
* Als het algoritme doorrekent op de 1e random rotatie is het niet per definitie mogelijk dat er een beter antwoord uit kan komen, waardoor het algoritme mogelijk nutteloos aan het rekenen is.

## Vector gebasseerd (vectorBasedA.py)

Dit algoritme vult de schepen aan de hand van een berekende vector uit het gewicht en het volume. Het matcht de vector van een parcel met de vector van het schip, en vult het schip dus aan de hand van een verhouding.

Voordelen:
* Algoritme vindt slechts een antwoord

Nadelen:
* Vector hoeft niet de optimale manier van het vullen van schepen te zijn.


## 'Logica gebasseerd'/Greedy (logicalSolutionA.py)

Dit algoritme kijkt na het toevoegen van elke parcel naar het percentage weight en het percentage volume dat het schip nog vrij heeft. Het algoritme probeert de schepen zo te vullen dat deze percentages gelijk op lopen. Wanneer er bijvoorbeeld meer volume vrij is dan weight, wordt er een pakketje met een hoger volume toegevoegt.

Voordelen:
* Test de assumptie dat een schip optimaal gevuld kan worden door het toegevoegde percentage volume en weight gelijk te proberen houden

Nadelen:
* Dit hoeft niet de optimale verdeling te zijn

## Hill climber (hillClimber.py)

Dit algoritme neemt als startpunt de uitkomst van SolutionA.py. Hierna maakt het steeds kleine aanpassingen door een aantal parcels uit de spacecrafts te halen en de vrijgekomen ruimte opnieuw te vullen. Wanneer het totaal aantal parcels of het percentage van hoe vol de spacecrafts hoger is dan de vorige iteratie, neemt het algoritme deze als beginpunt voor de volgende aanpasing.

Voordelen:
* Vind sneller een antwoord dan een brute force of random algoritme

Nadeel:
* Niet mogelijk om alle mogelijkheden langs te gaan

