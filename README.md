On remplit les cases vide dans la colonne acces_pied par le type de route 
```
Nature de route      ==>  acces pied
bretelle				Impossible
chemin				Libre
escalier				Libre
piste cyclable			Libre
rond point 				Libre
route à 1 chaussee			Libre
route à 2 chaussees 		Libre
route empierre 			Libre
sentier 				Libre
type auto routier			Impossible

````
On utilise différente valeur pour présenter différente de modes de transport
````
transport modes			           value

piéton uniquement			001
velo	 uniquement			010
vehicule uniquement			100

velo ,  vehicule, non pieton		110
pieton, vericule, non velo		101
pieton, velo ,    non véhicule		011

pieton, velo, et vehicule			111
````
