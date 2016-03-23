SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `tp_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `tp_db` ;

-- -----------------------------------------------------
-- Table `tp_db`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tp_db`.`User` (
  `idUser` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255),
  `email` VARCHAR(255) NOT NULL,
  `name` CHAR(32) COMMENT '	',
  `about` TEXT,
  `isAnonymous` TINYINT(1) NULL DEFAULT false,
  PRIMARY KEY (`idUser`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tp_db`.`Forum`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tp_db`.`Forum` (
  `idForum` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL COMMENT 'str forum name',
  `short_name` VARCHAR(255) NOT NULL COMMENT 'str forum slug',
  `idFounder` INT NOT NULL COMMENT 'founder email',
  UNIQUE INDEX `user_UNIQUE` (`idForum` ASC),
  UNIQUE INDEX `short_name_UNIQUE` (`short_name` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC),
  PRIMARY KEY (`idForum`),
  INDEX `id_idx` (`idFounder` ASC),
    FOREIGN KEY (`idFounder`)
    REFERENCES `tp_db`.`User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tp_db`.`Forum_User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tp_db`.`Forum_User` (
  `idForum_User` INT NOT NULL AUTO_INCREMENT,
  `idForum` INT NOT NULL,
  `idUser` INT NOT NULL,
  PRIMARY KEY (`idForum_User`),
  INDEX `idForum_idx` (`idForum` ASC),
  INDEX `idUser_idx` (`idUser` ASC),
    FOREIGN KEY (`idForum`)
    REFERENCES `tp_db`.`Forum` (`idForum`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    FOREIGN KEY (`idUser`)
    REFERENCES `tp_db`.`User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tp_db`.`Thread`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tp_db`.`Thread` (
  `idThread` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `message` TEXT NOT NULL,
  `slug` VARCHAR(255) NOT NULL,
  `date` DATETIME NOT NULL,
  `isClosed` TINYINT(1) NOT NULL DEFAULT false,
  `isDeleted` TINYINT(1) NULL DEFAULT false,
  `idForum` INT NOT NULL,
  `idAuthor` INT NOT NULL,
  `likes` INT NOT NULL,
  `dislikes` INT NOT NULL,
  PRIMARY KEY (`idThread`),
  INDEX `idForum_idx` (`idForum` ASC),
  INDEX `idUser_idx` (`idAuthor` ASC),
    FOREIGN KEY (`idForum`)
    REFERENCES `tp_db`.`Forum` (`idForum`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    FOREIGN KEY (`idAuthor`)
    REFERENCES `tp_db`.`User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tp_db`.`Post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tp_db`.`Post` (
  `idPost` INT NOT NULL AUTO_INCREMENT,
  `parent` INT NULL DEFAULT NULL,
  `isApproved` TINYINT(1) NULL DEFAULT FALSE,
  `isHighlighted` TINYINT(1) NULL DEFAULT FALSE,
  `isEdited` TINYINT(1) NULL DEFAULT FALSE,
  `isSpam` TINYINT(1) NULL DEFAULT FALSE,
  `isDeleted` TINYINT(1) NULL DEFAULT FALSE,
  `likes` INT NOT NULL,
  `dislikes` INT NOT NULL,
  `date` DATETIME NOT NULL,
  `message` TEXT NOT NULL,
  `idForum` INT NOT NULL,
  `idThread` INT NOT NULL,
  `idAuthor` INT NOT NULL,
  PRIMARY KEY (`idPost`),
  INDEX `idForum_idx` (`idForum` ASC),
  INDEX `idUser_idx` (`idAuthor` ASC),
  INDEX `idThread_idx` (`idThread` ASC),
    FOREIGN KEY (`idForum`)
    REFERENCES `tp_db`.`Forum` (`idForum`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    FOREIGN KEY (`idAuthor`)
    REFERENCES `tp_db`.`User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    FOREIGN KEY (`idThread`)
    REFERENCES `tp_db`.`Thread` (`idThread`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tp_db`.`Subscription`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tp_db`.`Subscription` (
  `idUser` INT NOT NULL,
  `idThread` INT NOT NULL,
  PRIMARY KEY (`idUser`, `idThread`),
  INDEX `idThread_idx` (`idThread` ASC),
    FOREIGN KEY (`idUser`)
    REFERENCES `tp_db`.`User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    FOREIGN KEY (`idThread`)
    REFERENCES `tp_db`.`Thread` (`idThread`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tp_db`.`Follower`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tp_db`.`Follower` (
  `idfollower` INT NOT NULL,
  `idfollowing` INT NOT NULL,
  PRIMARY KEY (`idfollower`, `idfollowing`),
  INDEX `idUser_idx` (`idfollowing` ASC),
    FOREIGN KEY (`idfollower`)
    REFERENCES `tp_db`.`User` (`idUser`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
    FOREIGN KEY (`idfollowing`)
    REFERENCES `tp_db`.`User` (`idUser`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
