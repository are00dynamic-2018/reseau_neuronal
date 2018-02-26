# Simulation d'un réseau de neurones biologique après l'ajout de substances psychoactives

<img src="Annexes/Images/neurone_illustration.png" width="50%" align="middle">


##### Table of Contents  
[Headers](#membres)  
[Emphasis](#emphasis)  



<a name="membres"/>


**Membre du groupe de recherche :**
- L'HARIDON Nora
- WEBER Benajmin
- CAO Song Toan 
- PINTO VIDEIRA Michael

## Documents de références :
- Pour voir __notre modélisation mathématique__ dans son ensemble voir le doucement : [Modélisation mathématique](/Annexes/Documents/reseau-neuronal-biologique-theorie.pdf)
- Pour voir __nos travaux de recherches préalables__ (travaux de découverte du sujet) s'orienter vers le document : [Préambule des recherches](/Annexes/Documents/recherche_reseau_neurone.pdf)

## Présentation du sujet :
<img src="Annexes/Images/structure_neurone_biologique.png" width="50%" align="middle">

Un neurone est une unité fonctionnelle réalisant une sommation spatiale et temporelle de ses entrées (les dendrites) à tout instant. Si le résultat (alors sous la forme d'un potentiel électrique) est supérieur à un certain seuil, le neurone envoie un influx nerveux, aussi dit potentiel d'action via son axone. Les synapses permettent alors la conversion de ce signal électrique en un signal chimique perceptible par les autres neurones qui y sont connectés. 

## Modélisations d'un réseau neuronal biologique

### Première modélisation :
<img src="Annexes/Images/formule_model_simple.png" width="60%" align="middle">

Nous traduisons cette formule sous forme matricielle afin de simplifier les calculs par la suite :
<img src="Annexes/Images/formule_model_simple_matricielle.png" width="90%" align="middle">

### Deuxième Modélisation :
Dans cette modélisation, on prend en compte le temps de décroissance du potentiel après une dépolarisation du neurone considéré

<img src="Annexes/Images/formule_decroissance_temps.png" width="90%" align="middle">

### Troisième Modélisation :
Cette modélisation prend en compte l'efficacité des connexions entre neurone. Les seuls éléments à modifier par rapport à la modélisation précédente sont : 

<img src="Annexes/Images/formule_poids_connexions.png" width="60%" align="middle">

### Quatrième Modélisation :
Cette modélisation prend en compte la plasticité synaptique
### Plasticité à court terme :

<img src="Annexes/Images/plasticite_court_terme.png" width="75%" align="middle">

### Plasticité à long terme :
