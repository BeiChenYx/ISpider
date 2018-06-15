/*
Navicat MySQL Data Transfer

Source Server         : Ubuntu_192.168.1.139
Source Server Version : 50720
Source Host           : 192.168.3.154:3306
Source Database       : testAPI

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2018-01-25 15:41:15
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for AnswerInfo
-- ----------------------------
DROP TABLE IF EXISTS `AnswerInfo`;
CREATE TABLE `AnswerInfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `questionName` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `questionInfo` text COLLATE utf8mb4_bin NOT NULL,
  `answer` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `answerContentInfo` text COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1919 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
