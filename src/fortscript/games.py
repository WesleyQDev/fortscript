"""
Pre-defined list of popular games and heavy applications with their process names.
"""

GAMES = [
    # Battle Royale / Shooter
    {"name": "Fortnite", "process": "fortnite"},
    {"name": "Fortnite", "process": "fortniteclient-win64-shipping"},
    {"name": "Apex Legends", "process": "r5apex"},
    {"name": "PUBG", "process": "tslgame"},
    {"name": "Call of Duty: Warzone", "process": "modernwarfare"},
    {"name": "Call of Duty: Warzone", "process": "warzone"},
    {"name": "Call of Duty: Modern Warfare", "process": "codmw"},
    {"name": "Call of Duty: Black Ops", "process": "blackops"},
    
    # FPS Competitivo
    {"name": "Counter-Strike 2", "process": "cs2"},
    {"name": "CS:GO", "process": "csgo"},
    {"name": "Valorant", "process": "valorant"},
    {"name": "Valorant", "process": "valorant-win64-shipping"},
    {"name": "Rainbow Six Siege", "process": "rainbowsix"},
    {"name": "Rainbow Six Siege", "process": "rainbowsix_vulkan"},
    {"name": "Overwatch", "process": "overwatch"},
    {"name": "Overwatch 2", "process": "overwatch2"},
    
    # MOBA
    {"name": "League of Legends", "process": "league of legends"},
    {"name": "League of Legends", "process": "leagueclient"},
    {"name": "Dota 2", "process": "dota2"},
    
    # Sandbox / Survival
    {"name": "Minecraft", "process": "minecraft"},
    {"name": "Minecraft Java", "process": "javaw"},
    {"name": "Roblox", "process": "robloxplayerbeta"},
    {"name": "Roblox Studio", "process": "robloxstudiobeta"},
    {"name": "Terraria", "process": "terraria"},
    {"name": "Rust", "process": "rustclient"},
    {"name": "Rust", "process": "rust"},
    {"name": "ARK: Survival Evolved", "process": "shootergame"},
    {"name": "ARK", "process": "ark"},
    {"name": "Valheim", "process": "valheim"},
    {"name": "7 Days to Die", "process": "7daystodie"},
    
    # RPG / Open World
    {"name": "GTA V", "process": "gta5"},
    {"name": "GTA V", "process": "gtav"},
    {"name": "Red Dead Redemption 2", "process": "rdr2"},
    {"name": "Cyberpunk 2077", "process": "cyberpunk2077"},
    {"name": "The Witcher 3", "process": "witcher3"},
    {"name": "Skyrim", "process": "tesv"},
    {"name": "Skyrim Special Edition", "process": "skyrimse"},
    {"name": "Elden Ring", "process": "eldenring"},
    {"name": "Dark Souls 3", "process": "darksouls3"},
    {"name": "Sekiro", "process": "sekiro"},
    {"name": "Fallout 4", "process": "fallout4"},
    {"name": "Fallout 76", "process": "fallout76"},
    {"name": "Starfield", "process": "starfield"},
    {"name": "Hogwarts Legacy", "process": "hogwartslegacy"},
    {"name": "Assassin's Creed", "process": "assassinscreed"},
    
    # MMO
    {"name": "World of Warcraft", "process": "wow"},
    {"name": "World of Warcraft", "process": "worldofwarcraft"},
    {"name": "Final Fantasy XIV", "process": "ffxiv"},
    {"name": "Final Fantasy XIV", "process": "ffxiv_dx11"},
    {"name": "Black Desert Online", "process": "blackdesert"},
    {"name": "Black Desert Online", "process": "blackdesert64"},
    {"name": "New World", "process": "newworld"},
    {"name": "Lost Ark", "process": "lostark"},
    {"name": "Guild Wars 2", "process": "guildwars2"},
    {"name": "Elder Scrolls Online", "process": "elderscrollsonline"},
    
    # Esportes
    {"name": "FIFA", "process": "fifa"},
    {"name": "FIFA 23", "process": "fifa23"},
    {"name": "FIFA 24", "process": "fifa24"},
    {"name": "FC 24", "process": "fc24"},
    {"name": "Rocket League", "process": "rocketleague"},
    {"name": "NBA 2K", "process": "nba2k"},
    {"name": "Madden NFL", "process": "madden"},
    {"name": "F1", "process": "f1"},
    
    # Estratégia
    {"name": "StarCraft II", "process": "sc2"},
    {"name": "StarCraft", "process": "starcraft"},
    {"name": "Age of Empires", "process": "ageofempires"},
    {"name": "Age of Empires IV", "process": "aoe4"},
    {"name": "Civilization VI", "process": "civilizationvi"},
    {"name": "Civilization VI", "process": "civ6"},
    {"name": "Total War", "process": "totalwar"},
    {"name": "XCOM 2", "process": "xcom2"},
    
    # Horror
    {"name": "Resident Evil Village", "process": "re8"},
    {"name": "Resident Evil 4", "process": "re4"},
    {"name": "Dead by Daylight", "process": "deadbydaylight"},
    {"name": "Outlast", "process": "outlast"},
    {"name": "Phasmophobia", "process": "phasmophobia"},
    {"name": "Lethal Company", "process": "lethalcompany"},
    
    # Simulação
    {"name": "Euro Truck Simulator 2", "process": "eurotrucks2"},
    {"name": "Truck Simulator", "process": "trucksimulator"},
    {"name": "Microsoft Flight Simulator", "process": "flightsimulator"},
    {"name": "Microsoft Flight Simulator", "process": "msfs"},
    {"name": "Farming Simulator", "process": "farming simulator"},
    {"name": "The Sims 4", "process": "thesims4"},
    
    # Indie / Popular
    {"name": "Among Us", "process": "among us"},
    {"name": "Among Us", "process": "amongus"},
    {"name": "Stardew Valley", "process": "stardewvalley"},
    {"name": "Hollow Knight", "process": "hollowknight"},
    {"name": "Cuphead", "process": "cuphead"},
    {"name": "Undertale", "process": "undertale"},
    {"name": "Deltarune", "process": "deltarune"},
    {"name": "Celeste", "process": "celeste"},
    {"name": "Hades", "process": "hades"},
    {"name": "Dead Cells", "process": "deadcells"},
    {"name": "The Binding of Isaac", "process": "isaac"},
    {"name": "Risk of Rain 2", "process": "riskofrain2"},
    {"name": "Deep Rock Galactic", "process": "deeprockgalactic"},
    {"name": "Don't Starve", "process": "dont starve"},
    
    # Card Games
    {"name": "Hearthstone", "process": "hearthstone"},
    {"name": "Magic: The Gathering Arena", "process": "mtga"},
    {"name": "Gwent", "process": "gwent"},
    
    # Fighting
    {"name": "Tekken", "process": "tekken"},
    {"name": "Street Fighter", "process": "streetfighter"},
    {"name": "Street Fighter 6", "process": "sf6"},
    {"name": "Mortal Kombat", "process": "mortalkombat"},
    {"name": "Mortal Kombat 11", "process": "mk11"},
    {"name": "Super Smash Bros", "process": "smashbros"},
    {"name": "Guilty Gear", "process": "guilty gear"},
    
    # Racing
    {"name": "Forza Horizon", "process": "forzahorizon"},
    {"name": "Forza Horizon 5", "process": "forzahorizon5"},
    {"name": "Need for Speed", "process": "needforspeed"},
    {"name": "Assetto Corsa", "process": "assetocorsa"},
    {"name": "Project Cars", "process": "projectcars"},
    {"name": "GRID", "process": "grid"},
    {"name": "DiRT", "process": "dirt"},
    
    # Co-op / Party
    {"name": "Palworld", "process": "palworld"},
    {"name": "Enshrouded", "process": "enshrouded"},
    {"name": "Satisfactory", "process": "satisfactory"},
    {"name": "Raft", "process": "raftgame"},
    {"name": "Raft", "process": "raft"},
    {"name": "Grounded", "process": "grounded"},
    {"name": "Sea of Thieves", "process": "seaofthieves"},
    {"name": "Human Fall Flat", "process": "humanfallflat"},
    {"name": "Fall Guys", "process": "fallguys"},
    {"name": "Overcooked", "process": "overcooked"},
]