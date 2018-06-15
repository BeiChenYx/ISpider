/*
Navicat MySQL Data Transfer

Source Server         : Ubuntu_192.168.1.139
Source Server Version : 50720
Source Host           : 192.168.3.154:3306
Source Database       : testAPI

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2018-01-25 15:41:42
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for topic_info
-- ----------------------------
DROP TABLE IF EXISTS `topic_info`;
CREATE TABLE `topic_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `topicCategory` varchar(255) NOT NULL,
  `topicLink` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=546 DEFAULT CHARSET=utf8;
