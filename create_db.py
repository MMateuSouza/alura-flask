import MySQLdb

conn = MySQLdb.connect(user="root", passwd="toor", host="127.0.0.1", port=3306)

conn.cursor().execute("DROP DATABASE `jogoteca`;")
conn.commit()

create_tables = """
SET NAMES utf8;

CREATE DATABASE `jogoteca` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;

USE `jogoteca`;

CREATE TABLE `game` (
    `pk` INTEGER NOT NULL AUTO_INCREMENT,
    `name` varchar(50) COLLATE utf8_bin NOT NULL,
    `category` varchar(40) COLLATE utf8_bin NOT NULL,
    `console` varchar(20) NOT NULL,
    PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `user` (
    `pk` INTEGER NOT NULL AUTO_INCREMENT,
    `username` varchar(20) COLLATE utf8_bin NOT NULL,
    `password` varchar(8) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
"""

conn.cursor().execute(create_tables)

cursor = conn.cursor()
cursor.executemany(
      "INSERT INTO jogoteca.user (username, password) VALUES (%s, %s)",
      [
            ("admin", "admin"),
            ("mateus", "123456"),
      ])

cursor.executemany(
      "INSERT INTO jogoteca.game (name, category, console) VALUES (%s, %s, %s)",
      [
            ("God of War 4", "Acao", "PS4"),
            ("NBA 2k18", "Esporte", "Xbox One"),
            ("Rayman Legends", "Indie", "PS4"),
            ("Super Mario RPG", "RPG", "SNES"),
            ("Super Mario Kart", "Corrida", "SNES"),
            ("Fire Emblem Echoes", "Estrategia", "3DS"),
      ])

conn.commit()
cursor.close()