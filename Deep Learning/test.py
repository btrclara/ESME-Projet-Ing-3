import pandas as pd

# Définir la taille du DataFrame
n = 90

# Initialiser le DataFrame avec une colonne de zéros
df = pd.DataFrame({'colonne_1': [0] * n})

# Initialiser un compteur pour alterner entre les valeurs 1 et 0
count = 0

# Créer une nouvelle colonne en alternant les valeurs 1 et 0 toutes les 30 lignes
df['colonne_0'] = [count if i % 30 != 0 else 1 - count for i in range(1, n+1)]
count = 1 - count

# Afficher le DataFrame
print(df)

import pandas as pd
import math

# Créez un exemple de dataframe avec des valeurs aléatoires
df = pd.DataFrame({'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
# Ajoutez une nouvelle colonne "B" avec les 30 premières lignes égales à 1, les 30 suivantes à 2, etc.
df = df.assign(B=lambda x: [math.floor(i/30)+1 for i in range(len(df))])

# Affichez le dataframe avec la nouvelle colonne
print(df)