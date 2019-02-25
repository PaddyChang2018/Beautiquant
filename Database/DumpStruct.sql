-- MySQL dump 10.13  Distrib 8.0.13, for Linux (x86_64)
--
-- Host: localhost    Database: financial
-- ------------------------------------------------------
-- Server version	5.5.5-10.3.12-MariaDB-2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `position`
--

DROP TABLE IF EXISTS `position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `position` (
  `posi_type` varchar(10) NOT NULL COMMENT '持仓类型，股票，封闭式基金，期货等',
  `code` varchar(10) NOT NULL COMMENT '股票代码，带后缀，如SH，SZ',
  `symbol` varchar(10) NOT NULL COMMENT '股票符号',
  `name` varchar(45) NOT NULL COMMENT '股票名称',
  `exchange` varchar(10) DEFAULT NULL,
  `board_type` varchar(10) DEFAULT NULL COMMENT '所属板块，主板，中小板，创业板，ST等',
  `industry` varchar(45) DEFAULT NULL COMMENT '行业',
  `trade_type` varchar(10) DEFAULT NULL COMMENT '交易类型，买入，卖出，融资买入，融券卖出',
  `volume` int(11) DEFAULT NULL COMMENT '成交量',
  `cost_price` decimal(8,3) DEFAULT NULL COMMENT '成本价格',
  `current_price` decimal(8,2) DEFAULT NULL COMMENT '现价',
  `market_value` decimal(12,2) DEFAULT NULL COMMENT '市值',
  `profit` decimal(12,2) DEFAULT NULL COMMENT '盈亏',
  PRIMARY KEY (`code`,`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trade_records`
--

DROP TABLE IF EXISTS `trade_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `trade_records` (
  `code` varchar(10) NOT NULL COMMENT '标的代码，股票代码，期货代码',
  `symbol` varchar(10) NOT NULL COMMENT '标的符号，股票编号',
  `trade_type` varchar(10) DEFAULT NULL COMMENT '交易类型，买入，卖出，融资买入，融券卖出',
  `openclose` varchar(45) DEFAULT NULL COMMENT '开平仓类型',
  `trade_price` decimal(8,2) DEFAULT NULL COMMENT '成交价格',
  `trade_volume` int(11) DEFAULT NULL COMMENT '成交量',
  `fee` decimal(8,2) DEFAULT NULL COMMENT '手续费',
  `trade_time` varchar(10) DEFAULT NULL COMMENT '交易时间',
  PRIMARY KEY (`code`,`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user` (
  `username` varchar(45) NOT NULL COMMENT '用户名',
  `password` varchar(45) NOT NULL COMMENT '用户密码',
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed
