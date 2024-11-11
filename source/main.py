# main.py

from PAC4.funciones import*

if __name__== '__main__':
  # Exercici 1
    print("Exercici 1: Descomprimir TMDB.zip")
    ex1_1('TMDB.zip')

    # Exercici 1.2
    print("\nExercici 1.2: Carregar dades CSV i integrar-les (DataFrame)")
    id = 'TMDB_info'
    rutes_csv = ['TMDB_info.csv', 'TMDB_overview.csv', 'TMDB_distribution.csv']
    df_integrat = ex1_2(rutes_csv, id)

    # Exercici 1.3
    print("\nExercici 1.3: Carregar dades CSV i integrar-les(Diccionari)")
    ex1_3(rutes_csv, id)

    # Exercici 2.1
    print("\nExercici 2.1: Calcular i mostrar la durada de les sèries")
    ex2_1(df_integrat)

    # Exercici 2.2
    print("\nExercici 2.2: Crear un diccionari amb informació de les sèries")
    ex2_2(df_integrat)

    # Exercici 3.1
    print("\nExercici 3.1: Filtrar i mostrar les sèries de crimen i misteri en anglès")
    ex3_1(df_integrat)

    # Exercici 3.2
    print("\nExercici 3.2: Filtrar i mostrar les sèries que han començat el 2023 i han estat cancel·lades")
    ex3_2(df_integrat)

    # Exercici 3.3
    print("\nExercici 3.3: Filtrar i mostrar les sèries en japonès")
    ex3_3(df_integrat)

    # Exercici 4.1
    print("\nExercici 4.1: Mostrar distribució de l'idioma original de les sèries")
    ex4_1(df_integrat)

    # Exercici 4.2
    print("\nExercici 4.2: Mostrar els gèneres més comuns de les sèries")
    ex4_2(df_integrat)

    # Exercici 4.3
    print("\nExercici 4.3: Mostrar '%' de les diferents categories de les sèries")
    ex4_3(df_integrat)


if __name__ == "__main__":
    main()