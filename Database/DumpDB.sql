CREATE DATABASE  IF NOT EXISTS `financial` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `financial`;
-- MySQL dump 10.17  Distrib 10.3.12-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: financial
-- ------------------------------------------------------
-- Server version	10.3.12-MariaDB-2

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
-- Table structure for table `fund_posi_stock`
--

DROP TABLE IF EXISTS `fund_posi_stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fund_posi_stock` (
  `sim_real` varchar(10) DEFAULT NULL COMMENT '仿真或实盘',
  `fund_name` varchar(45) DEFAULT NULL COMMENT '基金名',
  `strategy_name` varchar(45) DEFAULT NULL COMMENT '策略名',
  `code` varchar(10) NOT NULL COMMENT '股票代码，带后缀，如SH，SZ',
  `symbol` varchar(10) NOT NULL COMMENT '股票符号',
  `name` varchar(45) NOT NULL COMMENT '股票名称',
  `trade_type` varchar(10) DEFAULT NULL COMMENT '交易类型，买入，卖出，融资买入，融券卖出',
  `volume` int(11) DEFAULT NULL COMMENT '成交量',
  `cost_price` decimal(8,3) DEFAULT NULL COMMENT '成本价格',
  `current_price` decimal(8,2) DEFAULT NULL COMMENT '现价',
  `market_value` decimal(12,2) DEFAULT NULL COMMENT '市值',
  `profit` decimal(12,2) DEFAULT NULL COMMENT '盈亏',
  `target_price_lower` decimal(8,2) DEFAULT NULL COMMENT '目标价位下限',
  `target_price_upper` decimal(8,2) DEFAULT NULL COMMENT '目标价位上限',
  `stop_loss_price` decimal(8,2) DEFAULT NULL COMMENT '止损价',
  `industry` varchar(45) DEFAULT NULL COMMENT '行业',
  `board_type` varchar(10) DEFAULT NULL COMMENT '所属板块，主板，中小板，创业板，ST等',
  `exchange` varchar(10) DEFAULT NULL COMMENT '股票交易所',
  PRIMARY KEY (`code`,`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fund_posi_stock`
--

LOCK TABLES `fund_posi_stock` WRITE;
/*!40000 ALTER TABLE `fund_posi_stock` DISABLE KEYS */;
INSERT INTO `fund_posi_stock` VALUES ('实盘','ratel','orange','002644.SZ','002644','佛慈制药','买入',500,8.750,0.00,NULL,NULL,NULL,NULL,NULL,NULL,'中小版','深交所'),('仿真','ratel','apple','600030.SH','600030','中信证券','买入',500,25.756,0.00,0.00,NULL,NULL,NULL,NULL,'','主板','上交所'),('仿真','ratel','apple','600089.SH','600089','特变电工','买入',978,9.817,0.00,NULL,NULL,NULL,NULL,NULL,NULL,'主板','上交所'),('仿真','ratel','apple','600428.SH','600428','中远海特','买入',500,3.450,0.00,NULL,NULL,NULL,NULL,NULL,NULL,'主板','上交所');
/*!40000 ALTER TABLE `fund_posi_stock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fund_rcd_stock`
--

DROP TABLE IF EXISTS `fund_rcd_stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fund_rcd_stock` (
  `sim_real` varchar(10) DEFAULT NULL,
  `fund_name` varchar(45) DEFAULT NULL COMMENT '基金名',
  `strategy_name` varchar(45) DEFAULT NULL COMMENT '策略名',
  `code` varchar(10) NOT NULL COMMENT '股票代码',
  `symbol` varchar(10) NOT NULL COMMENT '股票符号',
  `name` varchar(45) DEFAULT NULL COMMENT '股票名称',
  `trade_type` varchar(10) DEFAULT NULL COMMENT '交易类型，买入，卖出，融资买入，融券卖出',
  `trade_price` decimal(8,2) DEFAULT NULL COMMENT '成交价格',
  `trade_volume` int(11) DEFAULT NULL COMMENT '成交量',
  `money` decimal(10,2) DEFAULT NULL COMMENT '实际金额，买入：股票+手续费；卖出：股票-收学费-税费。',
  `fee` decimal(8,2) DEFAULT NULL COMMENT '手续费',
  `tax` decimal(8,2) DEFAULT NULL,
  `trade_time` datetime DEFAULT NULL COMMENT '交易时间',
  `target_price_lower` decimal(8,2) DEFAULT NULL COMMENT '目标价位下限',
  `target_price_upper` decimal(8,2) DEFAULT NULL COMMENT '目标价位上限',
  `stop_loss_price` decimal(8,2) DEFAULT NULL COMMENT '止损价',
  PRIMARY KEY (`code`,`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fund_rcd_stock`
--

LOCK TABLES `fund_rcd_stock` WRITE;
/*!40000 ALTER TABLE `fund_rcd_stock` DISABLE KEYS */;
INSERT INTO `fund_rcd_stock` VALUES ('仿真','ratel','apple','002063.SZ','002063','远光软件','卖出',9.80,600,5880.00,5.00,20.00,'2019-03-08 13:36:25',NULL,NULL,NULL),('实盘','ratel','apple','300002.SZ','300002','神州泰岳','卖出',5.45,400,2180.00,5.00,20.00,'2019-03-08 13:21:39',NULL,NULL,NULL);
/*!40000 ALTER TABLE `fund_rcd_stock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `ratel_real_posi_stock_vi`
--

DROP TABLE IF EXISTS `ratel_real_posi_stock_vi`;
/*!50001 DROP VIEW IF EXISTS `ratel_real_posi_stock_vi`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `ratel_real_posi_stock_vi` (
  `code` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `trade_type` tinyint NOT NULL,
  `volume` tinyint NOT NULL,
  `cost_price` tinyint NOT NULL,
  `current_price` tinyint NOT NULL,
  `market_value` tinyint NOT NULL,
  `profit` tinyint NOT NULL,
  `target_price_lower` tinyint NOT NULL,
  `target_price_upper` tinyint NOT NULL,
  `stop_loss_price` tinyint NOT NULL,
  `industry` tinyint NOT NULL,
  `board_type` tinyint NOT NULL,
  `exchange` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `ratel_real_rcd_stock_vi`
--

DROP TABLE IF EXISTS `ratel_real_rcd_stock_vi`;
/*!50001 DROP VIEW IF EXISTS `ratel_real_rcd_stock_vi`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `ratel_real_rcd_stock_vi` (
  `code` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `trade_type` tinyint NOT NULL,
  `trade_price` tinyint NOT NULL,
  `trade_volume` tinyint NOT NULL,
  `money` tinyint NOT NULL,
  `fee` tinyint NOT NULL,
  `tax` tinyint NOT NULL,
  `trade_time` tinyint NOT NULL,
  `target_price_lower` tinyint NOT NULL,
  `target_price_upper` tinyint NOT NULL,
  `stop_loss_price` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `ratel_sim_posi_stock_vi`
--

DROP TABLE IF EXISTS `ratel_sim_posi_stock_vi`;
/*!50001 DROP VIEW IF EXISTS `ratel_sim_posi_stock_vi`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `ratel_sim_posi_stock_vi` (
  `code` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `trade_type` tinyint NOT NULL,
  `volume` tinyint NOT NULL,
  `cost_price` tinyint NOT NULL,
  `current_price` tinyint NOT NULL,
  `market_value` tinyint NOT NULL,
  `profit` tinyint NOT NULL,
  `target_price_lower` tinyint NOT NULL,
  `target_price_upper` tinyint NOT NULL,
  `stop_loss_price` tinyint NOT NULL,
  `industry` tinyint NOT NULL,
  `board_type` tinyint NOT NULL,
  `exchange` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `ratel_sim_rcd_stock_vi`
--

DROP TABLE IF EXISTS `ratel_sim_rcd_stock_vi`;
/*!50001 DROP VIEW IF EXISTS `ratel_sim_rcd_stock_vi`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `ratel_sim_rcd_stock_vi` (
  `code` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `trade_type` tinyint NOT NULL,
  `trade_price` tinyint NOT NULL,
  `trade_volume` tinyint NOT NULL,
  `money` tinyint NOT NULL,
  `fee` tinyint NOT NULL,
  `tax` tinyint NOT NULL,
  `trade_time` tinyint NOT NULL,
  `target_price_lower` tinyint NOT NULL,
  `target_price_upper` tinyint NOT NULL,
  `stop_loss_price` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `username` varchar(45) NOT NULL COMMENT '用户名',
  `password` varchar(45) NOT NULL COMMENT '用户密码',
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('zhangzheng','billchang106');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'financial'
--

--
-- Dumping routines for database 'financial'
--

--
-- Final view structure for view `ratel_real_posi_stock_vi`
--

/*!50001 DROP TABLE IF EXISTS `ratel_real_posi_stock_vi`*/;
/*!50001 DROP VIEW IF EXISTS `ratel_real_posi_stock_vi`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `ratel_real_posi_stock_vi` AS select `fund_posi_stock`.`code` AS `code`,`fund_posi_stock`.`name` AS `name`,`fund_posi_stock`.`trade_type` AS `trade_type`,`fund_posi_stock`.`volume` AS `volume`,`fund_posi_stock`.`cost_price` AS `cost_price`,`fund_posi_stock`.`current_price` AS `current_price`,`fund_posi_stock`.`market_value` AS `market_value`,`fund_posi_stock`.`profit` AS `profit`,`fund_posi_stock`.`target_price_lower` AS `target_price_lower`,`fund_posi_stock`.`target_price_upper` AS `target_price_upper`,`fund_posi_stock`.`stop_loss_price` AS `stop_loss_price`,`fund_posi_stock`.`industry` AS `industry`,`fund_posi_stock`.`board_type` AS `board_type`,`fund_posi_stock`.`exchange` AS `exchange` from `fund_posi_stock` where `fund_posi_stock`.`sim_real` = '实盘' and `fund_posi_stock`.`fund_name` = 'ratel' */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `ratel_real_rcd_stock_vi`
--

/*!50001 DROP TABLE IF EXISTS `ratel_real_rcd_stock_vi`*/;
/*!50001 DROP VIEW IF EXISTS `ratel_real_rcd_stock_vi`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `ratel_real_rcd_stock_vi` AS select `fund_rcd_stock`.`code` AS `code`,`fund_rcd_stock`.`name` AS `name`,`fund_rcd_stock`.`trade_type` AS `trade_type`,`fund_rcd_stock`.`trade_price` AS `trade_price`,`fund_rcd_stock`.`trade_volume` AS `trade_volume`,`fund_rcd_stock`.`money` AS `money`,`fund_rcd_stock`.`fee` AS `fee`,`fund_rcd_stock`.`tax` AS `tax`,`fund_rcd_stock`.`trade_time` AS `trade_time`,`fund_rcd_stock`.`target_price_lower` AS `target_price_lower`,`fund_rcd_stock`.`target_price_upper` AS `target_price_upper`,`fund_rcd_stock`.`stop_loss_price` AS `stop_loss_price` from `fund_rcd_stock` where `fund_rcd_stock`.`sim_real` = '实盘' and `fund_rcd_stock`.`fund_name` = 'ratel' */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `ratel_sim_posi_stock_vi`
--

/*!50001 DROP TABLE IF EXISTS `ratel_sim_posi_stock_vi`*/;
/*!50001 DROP VIEW IF EXISTS `ratel_sim_posi_stock_vi`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `ratel_sim_posi_stock_vi` AS select `fund_posi_stock`.`code` AS `code`,`fund_posi_stock`.`name` AS `name`,`fund_posi_stock`.`trade_type` AS `trade_type`,`fund_posi_stock`.`volume` AS `volume`,`fund_posi_stock`.`cost_price` AS `cost_price`,`fund_posi_stock`.`current_price` AS `current_price`,`fund_posi_stock`.`market_value` AS `market_value`,`fund_posi_stock`.`profit` AS `profit`,`fund_posi_stock`.`target_price_lower` AS `target_price_lower`,`fund_posi_stock`.`target_price_upper` AS `target_price_upper`,`fund_posi_stock`.`stop_loss_price` AS `stop_loss_price`,`fund_posi_stock`.`industry` AS `industry`,`fund_posi_stock`.`board_type` AS `board_type`,`fund_posi_stock`.`exchange` AS `exchange` from `fund_posi_stock` where `fund_posi_stock`.`sim_real` = '仿真' and `fund_posi_stock`.`fund_name` = 'ratel' */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `ratel_sim_rcd_stock_vi`
--

/*!50001 DROP TABLE IF EXISTS `ratel_sim_rcd_stock_vi`*/;
/*!50001 DROP VIEW IF EXISTS `ratel_sim_rcd_stock_vi`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `ratel_sim_rcd_stock_vi` AS select `fund_rcd_stock`.`code` AS `code`,`fund_rcd_stock`.`name` AS `name`,`fund_rcd_stock`.`trade_type` AS `trade_type`,`fund_rcd_stock`.`trade_price` AS `trade_price`,`fund_rcd_stock`.`trade_volume` AS `trade_volume`,`fund_rcd_stock`.`money` AS `money`,`fund_rcd_stock`.`fee` AS `fee`,`fund_rcd_stock`.`tax` AS `tax`,`fund_rcd_stock`.`trade_time` AS `trade_time`,`fund_rcd_stock`.`target_price_lower` AS `target_price_lower`,`fund_rcd_stock`.`target_price_upper` AS `target_price_upper`,`fund_rcd_stock`.`stop_loss_price` AS `stop_loss_price` from `fund_rcd_stock` where `fund_rcd_stock`.`sim_real` = '仿真' and `fund_rcd_stock`.`fund_name` = 'ratel' */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-12 20:45:15
