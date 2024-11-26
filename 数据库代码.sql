/*
 Navicat Premium Data Transfer

 Source Server         : t1
 Source Server Type    : MySQL
 Source Server Version : 80400 (8.4.0)
 Source Host           : localhost:3306
 Source Schema         : example

 Target Server Type    : MySQL
 Target Server Version : 80400 (8.4.0)
 File Encoding         : 65001

 Date: 12/06/2024 21:44:07
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for dispatcher
-- ----------------------------
DROP TABLE IF EXISTS `dispatcher`;
CREATE TABLE `dispatcher`  (
  `dispatcher_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `dispatcher_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `dispatcher_phone` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`dispatcher_id`) USING BTREE,
  UNIQUE INDEX `dispatcher_id`(`dispatcher_id` ASC) USING BTREE,
  INDEX `dispatcher_name`(`dispatcher_name` ASC) USING BTREE,
  INDEX `dispatcher_phone`(`dispatcher_phone` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for fastfood_shop
-- ----------------------------
DROP TABLE IF EXISTS `fastfood_shop`;
CREATE TABLE `fastfood_shop`  (
  `shop_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `price` int NOT NULL COMMENT '价格',
  `m_sale_v` int NOT NULL COMMENT '月销售量',
  `hp_num` int NOT NULL DEFAULT 0,
  `cp_num` int NOT NULL DEFAULT 0,
  `shop_tel` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`shop_name`) USING BTREE,
  UNIQUE INDEX `shop_name`(`shop_name` ASC) USING BTREE,
  INDEX `price`(`price` ASC) USING BTREE,
  INDEX `m_sale_v`(`m_sale_v` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for oorder
-- ----------------------------
DROP TABLE IF EXISTS `oorder`;
CREATE TABLE `oorder`  (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `shop_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `order_money` int NOT NULL,
  `order_way` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `cons_phone` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `cons_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `cons_addre` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `checked` int NULL DEFAULT 0,
  `create_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `rated` int NULL DEFAULT 0,
  PRIMARY KEY (`order_id`) USING BTREE,
  UNIQUE INDEX `order_id`(`order_id` ASC) USING BTREE,
  INDEX `shop_name`(`shop_name` ASC) USING BTREE,
  INDEX `order_money`(`order_money` ASC) USING BTREE,
  INDEX `order_way`(`order_way` ASC) USING BTREE,
  INDEX `cons_phone`(`cons_phone` ASC) USING BTREE,
  INDEX `cons_name`(`cons_name` ASC) USING BTREE,
  INDEX `cons_addre`(`cons_addre` ASC) USING BTREE,
  INDEX `checked`(`checked` ASC) USING BTREE,
  INDEX `create_time`(`create_time` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for orderway
-- ----------------------------
DROP TABLE IF EXISTS `orderway`;
CREATE TABLE `orderway`  (
  `orderway_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '???ͷ?ʽ',
  `count` int NOT NULL COMMENT '???ַ?ʽ?Ķ????',
  PRIMARY KEY (`orderway_name`) USING BTREE,
  UNIQUE INDEX `orderway_name`(`orderway_name` ASC) USING BTREE,
  INDEX `count`(`count` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for server
-- ----------------------------
DROP TABLE IF EXISTS `server`;
CREATE TABLE `server`  (
  `service_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '????Ա???',
  `service_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `fastfood_shop_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '???ڵĵ????',
  PRIMARY KEY (`service_id`) USING BTREE,
  UNIQUE INDEX `service_id`(`service_id` ASC) USING BTREE,
  INDEX `service_name`(`service_name` ASC) USING BTREE,
  INDEX `fastfood_shop_name`(`fastfood_shop_name` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `password` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `telephone` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `role` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `id`(`id` ASC) USING BTREE COMMENT '??????????ѡUNIQUE',
  INDEX `username`(`username` ASC) USING BTREE,
  INDEX `password`(`password` ASC) USING BTREE,
  INDEX `telephone`(`telephone` ASC) USING BTREE,
  INDEX `role`(`role` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user_msg
-- ----------------------------
DROP TABLE IF EXISTS `user_msg`;
CREATE TABLE `user_msg`  (
  `id` int UNSIGNED NULL DEFAULT NULL,
  `real_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `sex` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `age` int NOT NULL,
  `mail` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `phone` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `user_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  INDEX `userid`(`id` ASC) USING BTREE,
  INDEX `real_name`(`real_name` ASC) USING BTREE,
  INDEX `sex`(`sex` ASC) USING BTREE,
  INDEX `age`(`age` ASC) USING BTREE,
  INDEX `mail`(`mail` ASC) USING BTREE,
  INDEX `phone`(`phone` ASC) USING BTREE,
  INDEX `user_name`(`user_name` ASC) USING BTREE,
  CONSTRAINT `userid` FOREIGN KEY (`id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for wuliu
-- ----------------------------
DROP TABLE IF EXISTS `wuliu`;
CREATE TABLE `wuliu`  (
  `order_id` int NOT NULL COMMENT '?????ı??',
  `cons_phone` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `disp_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `deliver_time` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `ended` int NOT NULL DEFAULT 0 COMMENT '?Ƿ????',
  PRIMARY KEY (`order_id`) USING BTREE,
  UNIQUE INDEX `order_id`(`order_id` ASC) USING BTREE,
  INDEX `cons_phone`(`cons_phone` ASC) USING BTREE,
  INDEX `disp_id`(`disp_id` ASC) USING BTREE,
  INDEX `deliver_time`(`deliver_time` ASC) USING BTREE,
  INDEX `ended`(`ended` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- View structure for sended_order
-- ----------------------------
DROP VIEW IF EXISTS `sended_order`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `sended_order` AS select `oorder`.`order_id` AS `order_id`,`oorder`.`shop_name` AS `shop_name`,`oorder`.`order_money` AS `order_money`,`oorder`.`order_way` AS `order_way`,`oorder`.`cons_phone` AS `cons_phone`,`oorder`.`cons_name` AS `cons_name`,`oorder`.`cons_addre` AS `cons_addre`,`wuliu`.`disp_id` AS `disp_id`,`wuliu`.`deliver_time` AS `deliver_time`,`dispatcher`.`dispatcher_phone` AS `dispatcher_phone` from ((`oorder` join `wuliu` on((`oorder`.`order_id` = `wuliu`.`order_id`))) join `dispatcher` on((`wuliu`.`disp_id` = `dispatcher`.`dispatcher_id`))) where (`oorder`.`checked` = 2);

-- ----------------------------
-- View structure for sending_order
-- ----------------------------
DROP VIEW IF EXISTS `sending_order`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `sending_order` AS select `oorder`.`order_id` AS `order_id`,`oorder`.`shop_name` AS `shop_name`,`oorder`.`order_money` AS `order_money`,`oorder`.`order_way` AS `order_way`,`oorder`.`cons_phone` AS `cons_phone`,`oorder`.`cons_name` AS `cons_name`,`oorder`.`cons_addre` AS `cons_addre`,`wuliu`.`disp_id` AS `disp_id`,`wuliu`.`deliver_time` AS `deliver_time`,`dispatcher`.`dispatcher_phone` AS `dispatcher_phone` from ((`oorder` join `wuliu` on((`oorder`.`order_id` = `wuliu`.`order_id`))) join `dispatcher` on((`wuliu`.`disp_id` = `dispatcher`.`dispatcher_id`))) where (`oorder`.`checked` = 1);

-- ----------------------------
-- Triggers structure for table oorder
-- ----------------------------
DROP TRIGGER IF EXISTS `order_insert`;
delimiter ;;
CREATE TRIGGER `order_insert` AFTER INSERT ON `oorder` FOR EACH ROW BEGIN
    UPDATE orderway 
    SET count = count + 1 
    WHERE orderway_name = new.order_way;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table oorder
-- ----------------------------
DROP TRIGGER IF EXISTS `order_insert_sale`;
delimiter ;;
CREATE TRIGGER `order_insert_sale` AFTER INSERT ON `oorder` FOR EACH ROW BEGIN
    UPDATE fastfood_shop 
    SET m_sale_v = m_sale_v + 1 
    WHERE shop_name = new.shop_name;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table oorder
-- ----------------------------
DROP TRIGGER IF EXISTS `order_update`;
delimiter ;;
CREATE TRIGGER `order_update` AFTER UPDATE ON `oorder` FOR EACH ROW BEGIN
    IF (new.order_way != old.order_way) THEN
        UPDATE orderway 
        SET count = count - 1 
        WHERE orderway_name = old.order_way;
        UPDATE orderway 
        SET count = count + 1 
        WHERE orderway_name = new.order_way;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table oorder
-- ----------------------------
DROP TRIGGER IF EXISTS `update_cp_num`;
delimiter ;;
CREATE TRIGGER `update_cp_num` AFTER UPDATE ON `oorder` FOR EACH ROW BEGIN
    IF NEW.rated = 2 AND OLD.rated != 2 THEN
        UPDATE fastfood_shop
        SET cp_num = cp_num + 1
        WHERE shop_name = NEW.shop_name;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table oorder
-- ----------------------------
DROP TRIGGER IF EXISTS `update_hp_num`;
delimiter ;;
CREATE TRIGGER `update_hp_num` AFTER UPDATE ON `oorder` FOR EACH ROW BEGIN
    IF NEW.rated = 1 AND OLD.rated != 1 THEN
        UPDATE fastfood_shop
        SET hp_num = hp_num + 1
        WHERE shop_name = NEW.shop_name;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table oorder
-- ----------------------------
DROP TRIGGER IF EXISTS `order_delete`;
delimiter ;;
CREATE TRIGGER `order_delete` AFTER DELETE ON `oorder` FOR EACH ROW BEGIN
    UPDATE orderway 
    SET count = count - 1 
    WHERE orderway_name = old.order_way;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table oorder
-- ----------------------------
DROP TRIGGER IF EXISTS `order_delete_sale`;
delimiter ;;
CREATE TRIGGER `order_delete_sale` AFTER DELETE ON `oorder` FOR EACH ROW BEGIN
    UPDATE fastfood_shop 
    SET m_sale_v = m_sale_v - 1 
    WHERE shop_name = old.shop_name;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table wuliu
-- ----------------------------
DROP TRIGGER IF EXISTS `wuliu_insert`;
delimiter ;;
CREATE TRIGGER `wuliu_insert` AFTER INSERT ON `wuliu` FOR EACH ROW BEGIN
	UPDATE oorder 
    SET checked = 1 
    WHERE order_id = new.order_id;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
