-- MySQL dump 10.13  Distrib 5.5.47, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: tp_db
-- ------------------------------------------------------
-- Server version	5.5.47-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Follower`
--

DROP TABLE IF EXISTS `Follower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Follower` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `idfollower` int(11) NOT NULL,
  `idfollowing` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `follower_following` (`idfollower`,`idfollowing`),
  KEY `followee_follower` (`idfollowing`,`idfollower`),
  KEY `idUser_idx` (`idfollowing`),
  CONSTRAINT `Follower_ibfk_1` FOREIGN KEY (`idfollower`) REFERENCES `User` (`idUser`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `Follower_ibfk_2` FOREIGN KEY (`idfollowing`) REFERENCES `User` (`idUser`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Forum`
--

DROP TABLE IF EXISTS `Forum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Forum` (
  `idForum` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(50) NOT NULL COMMENT 'str forum name',
  `short_name` varchar(255) NOT NULL COMMENT 'str forum slug',
  `idFounder` int(11) NOT NULL COMMENT 'founder email',
  PRIMARY KEY (`idForum`),
  UNIQUE KEY `user_UNIQUE` (`idForum`),
  UNIQUE KEY `short_name_UNIQUE` (`short_name`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  KEY `id_idx` (`idFounder`),
  CONSTRAINT `Forum_ibfk_1` FOREIGN KEY (`idFounder`) REFERENCES `User` (`idUser`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Forum_User`
--

DROP TABLE IF EXISTS `Forum_User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Forum_User` (
  `idForum_User` int(11) NOT NULL AUTO_INCREMENT,
  `idForum` int(11) NOT NULL,
  `idUser` int(11) NOT NULL,
  PRIMARY KEY (`idForum_User`),
  UNIQUE KEY `user_tID` (`idUser`,`idForum`),
  KEY `idForum` (`idForum`),
  CONSTRAINT `Forum_User_ibfk_1` FOREIGN KEY (`idForum`) REFERENCES `Forum` (`idForum`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Forum_User_ibfk_2` FOREIGN KEY (`idUser`) REFERENCES `User` (`idUser`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Post`
--

DROP TABLE IF EXISTS `Post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Post` (
  `idPost` int(11) NOT NULL AUTO_INCREMENT,
  `parent` int(11) DEFAULT NULL,
  `isApproved` tinyint(1) DEFAULT '0',
  `isHighlighted` tinyint(1) DEFAULT '0',
  `isEdited` tinyint(1) DEFAULT '0',
  `isSpam` tinyint(1) DEFAULT '0',
  `isDeleted` tinyint(1) DEFAULT '0',
  `likes` int(11) NOT NULL,
  `dislikes` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `message` text NOT NULL,
  `idForum` int(11) NOT NULL,
  `idThread` int(11) NOT NULL,
  `idAuthor` int(11) NOT NULL,
  PRIMARY KEY (`idPost`),
  KEY `user_date` (`idAuthor`,`date`),
  KEY `forum_date` (`idForum`,`date`),
  KEY `thread_date` (`idThread`,`date`),
  KEY `idForum_idx` (`idForum`),
  KEY `idUser_idx` (`idAuthor`),
  KEY `idThread_idx` (`idThread`),
  CONSTRAINT `Post_ibfk_1` FOREIGN KEY (`idForum`) REFERENCES `Forum` (`idForum`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Post_ibfk_2` FOREIGN KEY (`idAuthor`) REFERENCES `User` (`idUser`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Post_ibfk_3` FOREIGN KEY (`idThread`) REFERENCES `Thread` (`idThread`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=547 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Subscription`
--

DROP TABLE IF EXISTS `Subscription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Subscription` (
  `idUser` int(11) NOT NULL,
  `idThread` int(11) NOT NULL,
  PRIMARY KEY (`idUser`,`idThread`),
  KEY `idThread_idx` (`idThread`),
  CONSTRAINT `Subscription_ibfk_1` FOREIGN KEY (`idUser`) REFERENCES `User` (`idUser`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Subscription_ibfk_2` FOREIGN KEY (`idThread`) REFERENCES `Thread` (`idThread`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Thread`
--

DROP TABLE IF EXISTS `Thread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Thread` (
  `idThread` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `slug` char(50) NOT NULL,
  `date` datetime NOT NULL,
  `isClosed` tinyint(1) NOT NULL DEFAULT '0',
  `isDeleted` tinyint(1) DEFAULT '0',
  `idForum` int(11) NOT NULL,
  `idAuthor` int(11) NOT NULL,
  `likes` int(11) NOT NULL,
  `dislikes` int(11) NOT NULL,
  PRIMARY KEY (`idThread`),
  KEY `user_date` (`idAuthor`,`date`),
  KEY `forum_date` (`idForum`,`date`),
  KEY `idForum_idx` (`idForum`),
  KEY `idUser_idx` (`idAuthor`),
  CONSTRAINT `Thread_ibfk_1` FOREIGN KEY (`idForum`) REFERENCES `Forum` (`idForum`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Thread_ibfk_2` FOREIGN KEY (`idAuthor`) REFERENCES `User` (`idUser`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `idUser` int(11) NOT NULL AUTO_INCREMENT,
  `username` char(30) DEFAULT NULL,
  `email` char(30) NOT NULL,
  `name` char(32) DEFAULT NULL,
  `about` text,
  `isAnonymous` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`email`),
  UNIQUE KEY `id` (`idUser`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-05-01 22:38:13
