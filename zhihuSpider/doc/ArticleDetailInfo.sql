/*
Navicat MySQL Data Transfer

Source Server         : Ubuntu_192.168.1.139
Source Server Version : 50720
Source Host           : 192.168.3.154:3306
Source Database       : testAPI

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2018-01-25 15:41:29
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for ArticleDetailInfo
-- ----------------------------
DROP TABLE IF EXISTS `ArticleDetailInfo`;
CREATE TABLE `ArticleDetailInfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `author` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `content` text COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
