CREATE DATABASE IF NOT EXISTS seeworld;
USE seeworld;

DROP TABLE IF EXISTS t_focus;
DROP TABLE IF EXISTS t_comment;
DROP TABLE IF EXISTS t_message;
DROP TABLE IF EXISTS t_user;

 CREATE TABLE `t_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `password` varchar(20) DEFAULT NULL,
  `sex` varchar(5) DEFAULT NULL,
  `age` tinyint unsigned DEFAULT NULL,
  `profession` varchar(20) DEFAULT NULL,
  `nation` varchar(20) DEFAULT NULL,
  `introduction` varchar(128) DEFAULT NULL,
  `valid` tinyint DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) charset=utf8;

CREATE TABLE `t_message` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `p_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `title` varchar(20) DEFAULT NULL,
  `description` varchar(50) DEFAULT NULL,
  `detail` varchar(512) DEFAULT NULL,
  `type` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `t_message_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `t_user` (`id`)
) charset=utf8;

CREATE TABLE `t_comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `m_id` int NOT NULL,
  `p_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `content` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `m_id` (`m_id`),
  CONSTRAINT `t_comment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `t_user` (`id`),
  CONSTRAINT `t_comment_ibfk_2` FOREIGN KEY (`m_id`) REFERENCES `t_message` (`id`)
) charset=utf8;

CREATE TABLE `t_focus` (
  `id1` int DEFAULT NULL,
  `id2` int DEFAULT NULL,
  UNIQUE KEY `id1` (`id1`,`id2`),
  KEY `id2` (`id2`),
  CONSTRAINT `t_focus_ibfk_1` FOREIGN KEY (`id1`) REFERENCES `t_user` (`id`),
  CONSTRAINT `t_focus_ibfk_2` FOREIGN KEY (`id2`) REFERENCES `t_user` (`id`)
) charset=utf8;
