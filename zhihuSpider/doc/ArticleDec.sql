/*
Navicat MySQL Data Transfer

Source Server         : Ubuntu_192.168.1.139
Source Server Version : 50720
Source Host           : 192.168.3.154:3306
Source Database       : testAPI

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2018-01-25 15:41:23
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for ArticleDec
-- ----------------------------
DROP TABLE IF EXISTS `ArticleDec`;
CREATE TABLE `ArticleDec` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topicCategory` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `ArticleName` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `ArticleLikenum` int(11) DEFAULT NULL,
  `ArticleCommentnum` int(11) DEFAULT NULL,
  `ArticleLink` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `Created` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=472 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
