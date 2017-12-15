# Programmeer Theorie - Space Freight

![CoverImage](/cover.JPG?raw=true)

### De raketjes
Marit Beerepoot - 10983430  
Jessy Bosman - 11056045  
Vincent Damen - 11034734  


## Vergelijking algoritmen en algemene uitleg algoritmen
[Deze wiki legt kort de voor- en nadelen van de gebruikte algoritmen uit](https://github.com/JessyBosman1/ProgrammeerTheorie/wiki/Algemene-beschrijving-algortimen)  
[Deze wiki gaat in op de vergelijking van de algoritmen (Experimentatie)](https://github.com/JessyBosman1/ProgrammeerTheorie/wiki/Experimentatie:-Vergelijking-algoritmen-A) 
[Deze wiki beschijft onze gemaakte keuzes en experimentatie bij vraag D en E](https://github.com/JessyBosman1/ProgrammeerTheorie/wiki/Keuzes-en-experimentatie-bij-D-en-E)

## Getting started
Om de scripts te runnen moet er in de commandline worden genavigeerd naar de map van de opdracht. Voor opdracht A dus naar de map A die in de map scripts staat etc. Door de scripts aan te roepen met python werken deze en printen deze een output.  
De bestanden main.py en preparation.py zijn bestanden met voorbereidingsfuncties en dataobjecten. Deze geven uit zichzelf geen output maar worden aangeroepen in andere bestanden.  
Om de visualisatie in werking te zien kan er worden genavigeerd naar de map vizualization en moet het bestand createLoadDistribution.py worden aangeroepen met python (deze opent 4 vensters, door het eerste venster te sluiten komt de 2e tevoorschijn etc.). Om deze visualisatie te kunnen zien moet matplotlib geinstalleerd zijn (zie hieronder voor meer informatie).

## Data structuur
Voor de data structuur is er gebruik gemaakt van classes. De datastructuur wordt gemaakt in de file main.py, in het mapje scripts.

### Visualization
De visualisaties kunnen gerund worden vanuit de map "visualization".

* htmlGenerate.py & htmlParcelScatterplot.py genereren de html code die de standaard info laat zien van hoe de parcels en hoe de spacecrafts verdeeld zijn. Deze kunnen worden geopend door het bijbehorende html bestand te openen. 

* createLoadDistribution.py opent momenteel de boxplots van de gevulde spacecrafts van de tot nu toe beste oplossing van 84, gevonden door de HillClimber. Het script kan ook zelf aparte data visualiseren als deze worden doorgestuurt naar het script. 



