# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 192.168.1.158 (MySQL 5.6.41-log)
# Database: urlooker
# Generation Time: 2019-09-12 03:16:29 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table event
# ------------------------------------------------------------

DROP TABLE IF EXISTS `event`;

CREATE TABLE `event` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `event_id` varchar(64) NOT NULL,
  `status` varchar(32) NOT NULL,
  `url` varchar(256) NOT NULL DEFAULT '',
  `ip` varchar(32) NOT NULL DEFAULT '',
  `strategy_id` int(11) DEFAULT NULL,
  `event_time` int(11) DEFAULT NULL,
  `resp_time` int(6) DEFAULT NULL,
  `resp_code` varchar(3) DEFAULT NULL,
  `result` int(1) NOT NULL DEFAULT '0' COMMENT '0:no error, 1:timeout, 2:expect code err, 3,keyword unmatch 4:dns err',
  `current_step` int(1) DEFAULT NULL,
  `max_step` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_strategy_id` (`strategy_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table item_status00
# ------------------------------------------------------------

DROP TABLE IF EXISTS `item_status00`;

CREATE TABLE `item_status00` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sid` int(10) unsigned NOT NULL,
  `ip` varchar(32) NOT NULL DEFAULT '',
  `resp_time` int(6) DEFAULT NULL,
  `resp_code` varchar(3) DEFAULT NULL,
  `push_time` int(10) DEFAULT NULL,
  `result` int(1) NOT NULL DEFAULT '0' COMMENT '0:no error, 1:timeout, 2:expect code err, 3,keyword unmatch 4:dns err',
  PRIMARY KEY (`id`),
  KEY `idx_ip` (`ip`),
  KEY `idx_sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table rel_sid_ip
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rel_sid_ip`;

CREATE TABLE `rel_sid_ip` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sid` int(10) unsigned NOT NULL,
  `ip` varchar(32) NOT NULL DEFAULT '',
  `ts` int(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_sid_ip` (`sid`,`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table rel_team_user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `rel_team_user`;

CREATE TABLE `rel_team_user` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `tid` bigint(20) unsigned NOT NULL,
  `uid` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_rel_tid` (`tid`),
  KEY `idx_rel_uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table strategy
# ------------------------------------------------------------

DROP TABLE IF EXISTS `strategy`;

CREATE TABLE `strategy` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(1024) COLLATE utf8_unicode_ci DEFAULT '',
  `keywords` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `except_keywords` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `timeout` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `creator` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `data` varchar(1024) COLLATE utf8_unicode_ci DEFAULT '',
  `ip` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `expect_code` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `tag` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `note` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `max_step` int(4) DEFAULT '3',
  `times` int(4) DEFAULT '3',
  `teams` varchar(32) COLLATE utf8_unicode_ci DEFAULT '',
  `ops_cp_app_id` int(11) DEFAULT NULL,
  `environment` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `idc` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



# Dump of table strategy_copy
# ------------------------------------------------------------

DROP TABLE IF EXISTS `strategy_copy`;

CREATE TABLE `strategy_copy` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(1024) COLLATE utf8_unicode_ci DEFAULT '',
  `keywords` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `except_keywords` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `timeout` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `creator` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `data` varchar(1024) COLLATE utf8_unicode_ci DEFAULT '',
  `ip` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `expect_code` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `tag` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `note` varchar(255) COLLATE utf8_unicode_ci DEFAULT '',
  `max_step` int(4) DEFAULT '3',
  `times` int(4) DEFAULT '3',
  `teams` varchar(32) COLLATE utf8_unicode_ci DEFAULT '',
  `ops_cp_app_id` int(11) DEFAULT NULL,
  `env` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `environment` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `idc` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



# Dump of table team
# ------------------------------------------------------------

DROP TABLE IF EXISTS `team`;

CREATE TABLE `team` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `resume` varchar(255) NOT NULL DEFAULT '',
  `creator` bigint(20) unsigned NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_team_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `cnname` varchar(64) NOT NULL DEFAULT '',
  `password` varchar(32) NOT NULL,
  `email` varchar(1024) NOT NULL DEFAULT '',
  `phone` varchar(16) NOT NULL DEFAULT '',
  `wechat` varchar(255) NOT NULL DEFAULT '',
  `role` tinyint(4) NOT NULL DEFAULT '0',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_user_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
