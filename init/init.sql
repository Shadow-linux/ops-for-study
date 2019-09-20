# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 192.168.1.158 (MySQL 5.6.41-log)
# Database: shadow_ops
# Generation Time: 2019-05-15 14:30:35 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table app_detail
# ------------------------------------------------------------

DROP TABLE IF EXISTS `app_detail`;

CREATE TABLE `app_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(100) DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `updated` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `internal_check_api` varchar(128) DEFAULT NULL,
  `external_check_api` varchar(128) DEFAULT NULL,
  `chose_agent` varchar(512) DEFAULT NULL,
  `internal_check_api_env` varchar(256) DEFAULT NULL,
  `is_external_check_api` tinyint(1) NOT NULL,
  `is_internal_check_api` tinyint(1) NOT NULL,
  `is_launch` tinyint(1) NOT NULL,
  `is_publish` tinyint(1) NOT NULL,
  `service` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table app_host_rel
# ------------------------------------------------------------

DROP TABLE IF EXISTS `app_host_rel`;

CREATE TABLE `app_host_rel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) DEFAULT NULL,
  `host_id` int(11) DEFAULT NULL,
  `owner` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table app_user_rel
# ------------------------------------------------------------

DROP TABLE IF EXISTS `app_user_rel`;

CREATE TABLE `app_user_rel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table auth_group
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table auth_group_permissions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table auth_permission
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table business_access_alarm_result
# ------------------------------------------------------------

DROP TABLE IF EXISTS `business_access_alarm_result`;

CREATE TABLE `business_access_alarm_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `work_order` varchar(128) DEFAULT NULL,
  `alarm_strategy` varchar(1024) DEFAULT NULL,
  `where_condition` varchar(1024) DEFAULT NULL,
  `match_count` int(11) DEFAULT NULL,
  `result_set` varchar(256) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `latest_time` int(11),
  PRIMARY KEY (`id`),
  UNIQUE KEY `work_order` (`work_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table business_access_alarm_strategy
# ------------------------------------------------------------

DROP TABLE IF EXISTS `business_access_alarm_strategy`;

CREATE TABLE `business_access_alarm_strategy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alarm_name` varchar(128) DEFAULT NULL,
  `work_order` varchar(128) DEFAULT NULL,
  `where_condition` varchar(1024) DEFAULT NULL,
  `alarm_strategy` varchar(1024) DEFAULT NULL,
  `latest_time` int(11) DEFAULT NULL,
  `is_mail` tinyint(1) NOT NULL,
  `is_message` tinyint(1) NOT NULL,
  `is_wechat` tinyint(1) NOT NULL,
  `send_user_id` varchar(256) NOT NULL,
  `is_alarm` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `work_order` (`work_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table cmdb_cloud_aliyun_ecs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `cmdb_cloud_aliyun_ecs`;

CREATE TABLE `cmdb_cloud_aliyun_ecs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(100) DEFAULT NULL,
  `serial_number` varchar(100) DEFAULT NULL,
  `cpu` int(11) DEFAULT NULL,
  `memory` int(11) DEFAULT NULL,
  `os_type` varchar(20) DEFAULT NULL,
  `os_name` varchar(50) DEFAULT NULL,
  `disk` varchar(500) DEFAULT NULL,
  `private_ip` varchar(200) DEFAULT NULL,
  `public_ip` varchar(100) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `environment` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `ssh_port` int(11) DEFAULT NULL,
  `ac_key_id` int(11) DEFAULT NULL,
  `zone_id` varchar(50) DEFAULT NULL,
  `region_id` varchar(50) DEFAULT NULL,
  `created` datetime(6) DEFAULT NULL,
  `expired_time` datetime(6) DEFAULT NULL,
  `instance_type` varchar(50) DEFAULT NULL,
  `instance_name` varchar(100) DEFAULT NULL,
  `instance_id` varchar(100) DEFAULT NULL,
  `instance_charge_type` varchar(20) DEFAULT NULL,
  `disk_id` varchar(1024) DEFAULT NULL,
  `ssh_ip` varchar(50) DEFAULT NULL,
  `swap` int(11) DEFAULT NULL,
  `is_ansible` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_hostname` (`hostname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table cmdb_cloud_aliyun_keys
# ------------------------------------------------------------

DROP TABLE IF EXISTS `cmdb_cloud_aliyun_keys`;

CREATE TABLE `cmdb_cloud_aliyun_keys` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `key_name` varchar(150) DEFAULT NULL,
  `access_key` varchar(100) DEFAULT NULL,
  `access_secret` varchar(100) DEFAULT NULL,
  `region_id` varchar(50) DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table cmdb_native_host
# ------------------------------------------------------------

DROP TABLE IF EXISTS `cmdb_native_host`;

CREATE TABLE `cmdb_native_host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(100) DEFAULT NULL,
  `serial_number` varchar(100) DEFAULT NULL,
  `idc` varchar(50) DEFAULT NULL,
  `cpu` int(11) DEFAULT NULL,
  `memory` int(11) DEFAULT NULL,
  `os_type` varchar(20) DEFAULT NULL,
  `os_name` varchar(50) DEFAULT NULL,
  `disk` varchar(500) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `private_ip` varchar(200) DEFAULT NULL,
  `public_ip` varchar(100) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `environment` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `updated` datetime(6) DEFAULT NULL,
  `ssh_port` int(11) DEFAULT NULL,
  `ssh_ip` varchar(50) DEFAULT NULL,
  `swap` int(11) DEFAULT NULL,
  `is_ansible` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_hostname` (`hostname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table cmdb_tags
# ------------------------------------------------------------

DROP TABLE IF EXISTS `cmdb_tags`;

CREATE TABLE `cmdb_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_key` varchar(100) DEFAULT NULL,
  `tag_value` varchar(200) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table cmdb_tags_aliyunecs_rel
# ------------------------------------------------------------

DROP TABLE IF EXISTS `cmdb_tags_aliyunecs_rel`;

CREATE TABLE `cmdb_tags_aliyunecs_rel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_id` int(11) DEFAULT NULL,
  `target_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table cmdb_tags_app_rel
# ------------------------------------------------------------

DROP TABLE IF EXISTS `cmdb_tags_app_rel`;

CREATE TABLE `cmdb_tags_app_rel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_id` int(11) DEFAULT NULL,
  `target_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table cmdb_tags_nativehost_rel
# ------------------------------------------------------------

DROP TABLE IF EXISTS `cmdb_tags_nativehost_rel`;

CREATE TABLE `cmdb_tags_nativehost_rel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_id` int(11) DEFAULT NULL,
  `target_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table common_setting_conf
# ------------------------------------------------------------

DROP TABLE IF EXISTS `common_setting_conf`;

CREATE TABLE `common_setting_conf` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner` varchar(50) DEFAULT NULL,
  `is_mail` tinyint(1) NOT NULL,
  `is_inner` tinyint(1) NOT NULL,
  `message_setting` varchar(1024) DEFAULT NULL,
  `cmdb_setting` varchar(1024) DEFAULT NULL,
  `app_setting` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table django_content_type
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table django_migrations
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table django_session
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table message_inner
# ------------------------------------------------------------

DROP TABLE IF EXISTS `message_inner`;

CREATE TABLE `message_inner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `work_order` varchar(100) NOT NULL,
  `user_id` longtext NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `is_succeed` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `status` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_work_order` (`work_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table message_mail
# ------------------------------------------------------------

DROP TABLE IF EXISTS `message_mail`;

CREATE TABLE `message_mail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `work_order` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL,
  `receiver` longtext NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `is_succeed` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_work_order` (`work_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table message_push
# ------------------------------------------------------------

DROP TABLE IF EXISTS `message_push`;

CREATE TABLE `message_push` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `work_order` varchar(100) NOT NULL,
  `title` varchar(100) NOT NULL,
  `content` longtext NOT NULL,
  `user_id_list` varchar(500) NOT NULL,
  `send_type_list` varchar(500) NOT NULL,
  `created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_work_order` (`work_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table operation_global_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `operation_global_log`;

CREATE TABLE `operation_global_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(150) NOT NULL,
  `uri` varchar(100) NOT NULL,
  `method` varchar(10) NOT NULL,
  `data` longtext NOT NULL,
  `description` varchar(200) NOT NULL,
  `time` datetime(6) NOT NULL,
  `is_succeed` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table permissions_all
# ------------------------------------------------------------

DROP TABLE IF EXISTS `permissions_all`;

CREATE TABLE `permissions_all` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) DEFAULT NULL,
  `page_permission` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table users_account
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users_account`;

CREATE TABLE `users_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `real_name` varchar(100) NOT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `position` varchar(100) NOT NULL,
  `department` varchar(100) NOT NULL,
  `login_position` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table users_account_groups
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users_account_groups`;

CREATE TABLE `users_account_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usersaccount_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_account_groups_usersaccount_id_group_id_00847c56_uniq` (`usersaccount_id`,`group_id`),
  KEY `users_account_groups_group_id_4595c4cc_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_account_groups_group_id_4595c4cc_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_account_groups_usersaccount_id_e5cfeae3_fk_users_acc` FOREIGN KEY (`usersaccount_id`) REFERENCES `users_account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table users_account_user_permissions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users_account_user_permissions`;

CREATE TABLE `users_account_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usersaccount_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_account_user_permi_usersaccount_id_permissi_a1945212_uniq` (`usersaccount_id`,`permission_id`),
  KEY `users_account_user_p_permission_id_b8b3cc4a_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_account_user_p_permission_id_b8b3cc4a_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_account_user_p_usersaccount_id_3e360684_fk_users_acc` FOREIGN KEY (`usersaccount_id`) REFERENCES `users_account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

# admin 用户 admin:admin
INSERT INTO `users_account` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `real_name`, `mobile`, `email`, `position`, `department`, `login_position`)
VALUES
	(1, 'pbkdf2_sha256$100000$RLOjgpWAb2rK$h4fRtXRZ4Vs0OaUUYhV0RsR4iY4HNrLiWtySQCr8tPU=', '2019-05-10 14:16:15.775655', 1, 'admin', '', '', 1, 1, '2019-03-30 14:51:06.474228', 'admin', NULL, '972367265@qq.com', 'developer', '技术中心', NULL);


# 权限组
INSERT INTO `auth_group` (`id`, `name`)
VALUES
  (1, 'admin'),
  (2, 'guest');
# 权限
INSERT INTO `permissions_all` (`id`, `group_id`, `page_permission`)
VALUES
  (1, 1, '{\"home\":1,\"setting\":1,\"setting_user\":2,\"setting_permissionGroup\":2,\"setting_sendMessage\":2,\"audit\":1,\"audit_operationLog\":2,\"setting_commonSetting\":2,\"cmdb\":1,\"app\":1,\"cmdb_aliyun_resource\":2,\"cmdb_aliyun_monitor\":2,\"cmdb_native_resource\":2,\"cmdb_native_monitor\":2,\"cmdb_tag\":2,\"app_management\":2}'),
  (2, 2, '{\"home\":1,\"setting\":0,\"setting_user\":0,\"setting_permissionGroup\":0,\"setting_sendMessage\":0,\"audit\":0,\"audit_operationLog\":0,\"setting_commonSetting\":0,\"app\":1,\"app_management\":1,\"cmdb\":1,\"cmdb_aliyun_resource\":1,\"cmdb_aliyun_monitor\":1,\"cmdb_native_resource\":1,\"cmdb_native_monitor\":1,\"cmdb_tag\":0}');


# 组与user关系
INSERT INTO `users_account_groups` (`id`, `usersaccount_id`, `group_id`)
VALUES
  (1, 1, 1);

# 全局设置
INSERT INTO `common_setting_conf` (`id`, `owner`, `is_mail`, `is_inner`, `message_setting`, `cmdb_setting`, `app_setting`, `code_publish_setting`)
VALUES
  (1, 'global', 1, 1, '{\"mail\":{\"smtp_host\":\"smtp.ym.163.com\",\"smtp_port\":465,\"smtp_ssl\":true,\"mail_user\":\"ops@ishouru.com\",\"mail_password\":\"ayg99*OPS&\",\"mail_test\":\"972367265@qq.com\"}}', '{\"base\":{\"idc\":[],\"env\":[\"undefined\", \"external\"],\"ssh_proxy\":{\"aliyun\":\"AliyunEcs\",\"native\":\"NativeHost\"}}}', '{\"service\":[]}', '{"server_mode":["docker","jar","tc2docker","tomcat"],"jenkins_project":["ops-deposit","test-deposit","ayg-deposit"], "git_info": {"username": "", "password": ""}}');

