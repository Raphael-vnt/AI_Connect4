# AI_Connect4
## Abstrait

Le jeu du puissance 4 étant un jeu à somme nul, autrement dit les pertes d'un joueur sont égales aux gains de l'autre, je me suis librement inspiré de l'algorithme MinMax. 
## Algorithme Minimax et étalage alpha-beta

L'algorithme minimax visite l'arbre de jeu pour faire remonter à la racine une valeur de jeu **f(p)** qui est calculée récursivement de la façon suivante :

- **minimax(p) = f(p)** si `p` est une feuille de l'arbre où `f` est une fonction d’évaluation de la position du jeu ;
- **minimax(p) = max(minimax(O₁), …, minimax(Oₙ))** si `p` est un nœud Joueur avec fils `O₁, …, Oₙ` ;
- **minimax(p) = min(minimax(O₁), …, minimax(Oₙ))** si `p` est un nœud Opposant avec fils `O₁, …, Oₙ`.

La valeur de jeu est déterminer via l'élaboration d'une fonction heuristique évaluant le plateau et l'avantage de chacun des joueurs. La fonction heuristique implémentée dans ce code attribue un score positif lorsque l'avantage est au premier joueur et négatif pour le second joeur. 

De manière simplifiée, l'heuristque récompense les alignements de jetons d'un joueur à condition que l'autre joueur ne le bloque pas (matrice heuri). 
Par la suite on compte le nombre de menaces du joueur, c'est à dire lorsque ce dernier à 3 jetons alignés non bloqués. Si le joueur possède 2 menaces permettant de gagner au prochain tour, l'autre joueur ne peut pas bloquer les 2 au tour suivant et donc le joueur obtient une très forte récompense. De manière triviale, la récompense est maximale lorsque 4 jetons sont alignés. 

Enfin de réduire l'espace d'exploration des noeuds de l'arbre, nous utilisons l'étalage alpha-beta. Cette méthode permet d'optimiser grandement l'algorithme minimax sans en modifier le résultat. 


