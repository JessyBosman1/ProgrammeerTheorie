# State space
## A, B, C
100 parcels -> 100! -> 9.33E+157 mogelijkheden. Neem een bruteforce, er tussen 100! verschillende volgordes worden gevormd, waarop de parcels in de schepen kunnen worden gestopt.

## D
Bij een bruteforce, waar telkens de schepen dezelfde volgorde aanhouden, zijn er 1250! = 1.648115996E+3330 mogelijkheden waarop de parcels in de spacecraft kunnen worden gedaan.

## E 
De state space is gigantisch. nPr(1250 + 6-1), gesimplificeerd (geen verschil in parcels en schepen). Ervan uitgaand dat een schip 0 of meer parcels vervoert en dat er geen massalimiet per schip is en dat de schepen niet onderscheidbaar zijn en dat de parcels niet onderscheidbaar zijn.

# Conclusies
### A
_Verdeel de parcels van cargolist 1 over de vier spacecrafts. Is het mogelijk om 97 parcels mee te nemen?_  
Het hoogst door ons gevonden aantal parcels wat mee kan, is 84. Dus nee, wij hebben niet kunnen vinden dat er 97 parcels mee kunnen.

### B
_Wat is de grootste set van parcels van cargolist 1 dat kan worden verdeeld over de vier spacecrafts? Geef een zo goedkoop mogelijke verdeling als er meerdere sets van maximale grootte mogelijk zijn. Doe dit eerst met waarde FtW=0.73 voor alle spacecrafts en doe dit daarna met de FtW waarden uit de tabel_  
De Hillclimber vond 308 verschillende parcel combinaties waarbij er in totaal 84 parcels mee konsen. De kosten hiervan zijn afgerond $1682797850 miljard met de echte fuel to weight ratio en $1687870000 met de algemene.

### C
_Hetzelfde voor cargolist 2. Wat is de grootste set van parcels van cargolist 2 dat kan worden verdeeld over de vier spacecrafts? Geef een zo goedkoop mogelijke verdeling als er meerdere sets van maximale grootte mogelijk zijn. Doe dit eerst met waarde FtW=0.73 voor alle spacecrafts en doe dit daarna met de FtW waarden uit de tabel._  
De hillclimber vond 2 combinaties met 74 parcel, kosten hiervan zijn $1699122250 met de echte fuel to weight waarde en $1704875900 met de algemene fuel to weight waarde.

### D
_Stel een transportvloot samen voor de kolossale cargolijst 3 en verdeel de parcels over de vloot. Hoe goedkoper het transport, hoe beter._  
De hillclimber vond 8 x 6 en 1 x 4 schepen laten vliegen het goedkoopste was, met een bedrag van $30186023600.

### E
 _Negeer de politieke constraint over de verdeling van de spacecrafts en stel een vloot zonder deze constraint samen. Lukt het om het transport goedkoper te maken?_  
Ja! Beide geschreven algoritmen kwamen lager uit, namelijk bij $26 miljard.
