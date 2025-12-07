#!/usr/bin/env python3
"""
Script de renommage des dossiers Pokemon anglais vers français
"""

from pathlib import Path

# Dictionnaire de mapping anglais → français (Génération 1)
POKEMON_MAPPING = {
    "Bulbasaur": "Bulbizarre",
    "Ivysaur": "Herbizarre",
    "Venusaur": "Florizarre",
    "Charmander": "Salamèche",
    "Charmeleon": "Reptincel",
    "Charizard": "Dracaufeu",
    "Squirtle": "Carapuce",
    "Wartortle": "Carabaffe",
    "Blastoise": "Tortank",
    "Caterpie": "Chenipan",
    "Metapod": "Chrysacier",
    "Butterfree": "Papilusion",
    "Weedle": "Aspicot",
    "Kakuna": "Coconfort",
    "Beedrill": "Dardargnan",
    "Pidgey": "Roucool",
    "Pidgeotto": "Roucoups",
    "Pidgeot": "Roucarnage",
    "Rattata": "Rattata",
    "Raticate": "Rattatac",
    "Spearow": "Piafabec",
    "Fearow": "Rapasdepic",
    "Ekans": "Abo",
    "Arbok": "Arbok",
    "Pikachu": "Pikachu",
    "Raichu": "Raichu",
    "Sandshrew": "Sabelette",
    "Sandslash": "Sablaireau",
    "Nidoran♀": "Nidoran♀",
    "Nidoran-f": "Nidoran♀",  # Variante avec tiret
    "NidoranF": "Nidoran♀",   # Variante sans espace
    "Nidorina": "Nidorina",
    "Nidoqueen": "Nidoqueen",
    "Nidoran♂": "Nidoran♂",
    "Nidoran-m": "Nidoran♂",  # Variante avec tiret
    "NidoranM": "Nidoran♂",   # Variante sans espace
    "Nidorino": "Nidorino",
    "Nidoking": "Nidoking",
    "Clefairy": "Mélofée",
    "Clefable": "Mélodelfe",
    "Vulpix": "Goupix",
    "Ninetales": "Feunard",
    "Jigglypuff": "Rondoudou",
    "Wigglytuff": "Grodoudou",
    "Zubat": "Nosferapti",
    "Golbat": "Nosferalto",
    "Oddish": "Mystherbe",
    "Gloom": "Ortide",
    "Vileplume": "Rafflesia",
    "Paras": "Paras",
    "Parasect": "Parasect",
    "Venonat": "Mimitoss",
    "Venomoth": "Aéromite",
    "Diglett": "Taupiqueur",
    "Dugtrio": "Triopikeur",
    "Meowth": "Miaouss",
    "Persian": "Persian",
    "Psyduck": "Psykokwak",
    "Golduck": "Akwakwak",
    "Mankey": "Férosinge",
    "Primeape": "Colossinge",
    "Growlithe": "Caninos",
    "Arcanine": "Arcanin",
    "Poliwag": "Ptitard",
    "Poliwhirl": "Têtarte",
    "Poliwrath": "Tartard",
    "Abra": "Abra",
    "Kadabra": "Kadabra",
    "Alakazam": "Alakazam",
    "Machop": "Machoc",
    "Machoke": "Machopeur",
    "Machamp": "Mackogneur",
    "Bellsprout": "Chétiflor",
    "Weepinbell": "Boustiflor",
    "Victreebel": "Empiflor",
    "Tentacool": "Tentacool",
    "Tentacruel": "Tentacruel",
    "Geodude": "Racaillou",
    "Graveler": "Gravalanch",
    "Golem": "Grolem",
    "Ponyta": "Ponyta",
    "Rapidash": "Galopa",
    "Slowpoke": "Ramoloss",
    "Slowbro": "Flagadoss",
    "Magnemite": "Magnéti",
    "Magneton": "Magnéton",
    "Farfetch'd": "Canarticho",
    "Farfetchd": "Canarticho",  # Sans apostrophe
    "Doduo": "Doduo",
    "Dodrio": "Dodrio",
    "Seel": "Otaria",
    "Dewgong": "Lamantine",
    "Grimer": "Tadmorv",
    "Muk": "Grotadmorv",
    "Shellder": "Kokiyas",
    "Cloyster": "Crustabri",
    "Gastly": "Fantominus",
    "Haunter": "Spectrum",
    "Gengar": "Ectoplasma",
    "Onix": "Onix",
    "Drowzee": "Soporifik",
    "Hypno": "Hypnomade",
    "Krabby": "Krabby",
    "Kingler": "Krabboss",
    "Voltorb": "Voltorbe",
    "Electrode": "Électrode",
    "Exeggcute": "Noeunoeuf",
    "Exeggutor": "Noadkoko",
    "Cubone": "Osselait",
    "Marowak": "Ossatueur",
    "Hitmonlee": "Kicklee",
    "Hitmonchan": "Tygnon",
    "Lickitung": "Excelangue",
    "Koffing": "Smogo",
    "Weezing": "Smogogo",
    "Rhyhorn": "Rhinocorne",
    "Rhydon": "Rhinoféros",
    "Chansey": "Leveinard",
    "Tangela": "Saquedeneu",
    "Kangaskhan": "Kangourex",
    "Horsea": "Hypotrempe",
    "Seadra": "Hypocéan",
    "Goldeen": "Poissirène",
    "Seaking": "Poissoroy",
    "Staryu": "Stari",
    "Starmie": "Staross",
    "Mr. Mime": "M.Mime",
    "Mr.Mime": "M.Mime",  # Sans espace
    "Scyther": "Insécateur",
    "Jynx": "Lippoutou",
    "Electabuzz": "Élektek",
    "Magmar": "Magmar",
    "Pinsir": "Scarabrute",
    "Tauros": "Tauros",
    "Magikarp": "Magicarpe",
    "Gyarados": "Léviator",
    "Lapras": "Lokhlass",
    "Ditto": "Métamorph",
    "Eevee": "Évoli",
    "Vaporeon": "Aquali",
    "Jolteon": "Voltali",
    "Flareon": "Pyroli",
    "Porygon": "Porygon",
    "Omanyte": "Amonita",
    "Omastar": "Amonistar",
    "Kabuto": "Kabuto",
    "Kabutops": "Kabutops",
    "Aerodactyl": "Ptéra",
    "Snorlax": "Ronflex",
    "Articuno": "Artikodin",
    "Zapdos": "Électhor",
    "Moltres": "Sulfura",
    "Dratini": "Minidraco",
    "Dragonair": "Draco",
    "Dragonite": "Dracolosse",
    "Mewtwo": "Mewtwo",
    "Mew": "Mew",
    # Formes Alola
    "Alolan Sandshrew": "Sabelette d'Alola",
    "Alolan Sandslash": "Sablaireau d'Alola",
    "Alolan Vulpix": "Goupix d'Alola",
    "Alolan Ninetales": "Feunard d'Alola",
    "Alolan Diglett": "Taupiqueur d'Alola",
    "Alolan Dugtrio": "Triopikeur d'Alola",
    "Alolan Meowth": "Miaouss d'Alola",
    "Alolan Persian": "Persian d'Alola",
    "Alolan Geodude": "Racaillou d'Alola",
    "Alolan Graveler": "Gravalanch d'Alola",
    "Alolan Golem": "Grolem d'Alola",
    "Alolan Grimer": "Tadmorv d'Alola",
    "Alolan Muk": "Grotadmorv d'Alola",
    "Alolan Exeggutor": "Noadkoko d'Alola",
    "Alolan Marowak": "Ossatueur d'Alola",
    "Alolan Raichu": "Raichu d'Alola",
}


def rename_folders(base_path: str = "PokemonData", dry_run: bool = True):
    """
    Renomme les dossiers Pokemon anglais en français

    Args:
        base_path: Chemin vers le dossier contenant les sous-dossiers Pokemon
        dry_run: Si True, affiche uniquement ce qui serait fait sans renommer
    """
    base_path = Path(base_path)

    if not base_path.exists():
        print(f"❌ Le dossier {base_path} n'existe pas!")
        return

    print(f"{'🔍 SIMULATION' if dry_run else '🚀 RENOMMAGE'} des dossiers Pokemon...")
    print(f"Dossier cible: {base_path.absolute()}\n")

    renamed_count = 0
    not_found_count = 0
    already_french = 0

    # Liste tous les sous-dossiers
    folders = [f for f in base_path.iterdir() if f.is_dir()]

    for folder in sorted(folders):
        folder_name = folder.name

        # Vérifie si le dossier est déjà en français
        if folder_name in POKEMON_MAPPING.values():
            already_french += 1
            print(f"✓ {folder_name:<30} (déjà en français)")
            continue

        # Cherche la traduction
        if folder_name in POKEMON_MAPPING:
            french_name = POKEMON_MAPPING[folder_name]
            new_path = folder.parent / french_name

            if dry_run:
                print(f"→ {folder_name:<30} → {french_name}")
            else:
                try:
                    folder.rename(new_path)
                    print(f"✅ {folder_name:<30} → {french_name}")
                    renamed_count += 1
                except Exception as e:
                    print(f"❌ Erreur pour {folder_name}: {e}")
        else:
            print(f"⚠️  {folder_name:<30} (pas dans le dictionnaire)")
            not_found_count += 1

    # Résumé
    print("\n" + "="*60)
    if dry_run:
        print("📊 RÉSUMÉ (SIMULATION)")
    else:
        print("📊 RÉSUMÉ")
    print("="*60)
    print(f"Dossiers à renommer: {renamed_count if dry_run else 'N/A'}")
    print(f"Dossiers renommés: {renamed_count if not dry_run else 'N/A'}")
    print(f"Déjà en français: {already_french}")
    print(f"Non trouvés dans le dictionnaire: {not_found_count}")
    print(f"Total: {len(folders)}")

    if dry_run:
        print("\n💡 Pour effectuer le renommage, lancez:")
        print("   python rename_pokemon_folders.py --execute")


if __name__ == "__main__":
    import sys

    # Par défaut, mode simulation
    dry_run = True

    # Si --execute est passé, exécute réellement
    if "--execute" in sys.argv or "-e" in sys.argv:
        dry_run = False
        print("⚠️  MODE EXÉCUTION ACTIVÉ - Les dossiers vont être renommés!\n")
        response = input("Continuer? (oui/non): ")
        if response.lower() not in ["oui", "yes", "y", "o"]:
            print("Annulé.")
            sys.exit(0)

    rename_folders(dry_run=dry_run)
