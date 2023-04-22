import sqlite3

base = sqlite3.connect('PodPiwoon.db')
cur = base.cursor()

# Guilds table
base.execute("""CREATE TABLE IF NOT EXISTS guilds
                (
                    guild_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    owner TEXT NOT NULL                                                  
                )
            """)
base.commit()

# Channels table
base.execute("""CREATE TABLE IF NOT EXISTS channels
                (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT,
                    guild_id INTEGER,
                    FOREIGN KEY (guild_id) REFERENCES guilds(guild_id) ON DELETE CASCADE                         
                )
            """)
base.commit()

# Members table
base.execute("""CREATE TABLE IF NOT EXISTS members
                (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    nick TEXT,
                    cenz_int INTEGER,
                    guild_id INTEGER,
                    FOREIGN KEY (guild_id) REFERENCES guilds(guild_id) ON DELETE SET NULL                
                )
            """)
base.commit()