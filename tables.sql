CREATE SCHEMA IF NOT EXISTS `pp_music` DEFAULT CHARACTER SET utf8 ;
USE `pp_music` ;

CREATE TABLE `user` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `userName` varchar(20) NOT NULL,
  `firstName` varchar(20) NOT NULL,
  `lastName` varchar(25) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `userStatus` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `song` (
  `songId` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `productionYear` int DEFAULT NULL,
  `length` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`songId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `playlist` (
  `playlistId` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`playlistId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `playlistssongs` (
  `songId` int NOT NULL,
  `playlistId` int NOT NULL,
  PRIMARY KEY (`songId`,`playlistId`),
  KEY `playlistId` (`playlistId`),
  CONSTRAINT `playlistssongs_ibfk_1` FOREIGN KEY (`playlistId`) REFERENCES `playlist` (`playlistId`),
  CONSTRAINT `playlistssongs_ibfk_2` FOREIGN KEY (`songId`) REFERENCES `song` (`songId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `privateplaylist` (
  `privateplaylistId` int NOT NULL AUTO_INCREMENT,
  `playlistId` int DEFAULT NULL,
  `Id` int DEFAULT NULL,
  PRIMARY KEY (`privateplaylistId`),
  KEY `Id` (`Id`),
  KEY `playlistId` (`playlistId`),
  CONSTRAINT `privateplaylist_ibfk_1` FOREIGN KEY (`Id`) REFERENCES `user` (`Id`),
  CONSTRAINT `privateplaylist_ibfk_2` FOREIGN KEY (`playlistId`) REFERENCES `playlist` (`playlistId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;