```sql
-- SET NAMES utf8mb4; -- 设置字符集为utf8mb4，支持更广泛的字符集

-- SET FOREIGN_KEY_CHECKS = 0; -- 禁用外键检查，允许在插入数据时不满足外键约束

-- 创建 dispatcher 表
DROP TABLE IF EXISTS `dispatcher`;
CREATE TABLE `dispatcher` (
    `dispatcher_id` VARCHAR(50) NOT NULL,
    `dispatcher_name` VARCHAR(50) NOT NULL,
    `dispatcher_phone` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`dispatcher_id`),
    UNIQUE INDEX `dispatcher_id` (`dispatcher_id`),
    INDEX `dispatcher_name` (`dispatcher_name`),
    INDEX `dispatcher_phone` (`dispatcher_phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; -- 创建 dispatcher 表的结构，包括主键和索引

-- 向 dispatcher 表插入数据
-- INSERT INTO `dispatcher` VALUES
    

-- 创建 fastfood_shop 表（需要增加一个,店铺电话，好评,差评）
DROP TABLE IF EXISTS `fastfood_shop`;
CREATE TABLE `fastfood_shop` (
    `shop_name` VARCHAR(50) NOT NULL,
    `price` INT NOT NULL COMMENT '价格',
    `m_sale_v` INT NOT NULL COMMENT '销售量',
    `hp_num` int NOT NULL DEFAULT 0,
  	`cp_num` int NOT NULL DEFAULT 0,
    `shop_tel` INT NOT NULL COMMENT '店铺电话',
    PRIMARY KEY (`shop_name`),
    UNIQUE INDEX `shop_name` (`shop_name`),
    INDEX `price` (`price`),
    INDEX `m_sale_v` (`m_sale_v`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; -- 创建 fastfood_shop 表的结构

-- 向 fastfood_shop 表插入数据
-- INSERT INTO `fastfood_shop` VALUES
    

-- 创建 oorder 表
DROP TABLE IF EXISTS `oorder`;
CREATE TABLE `oorder` (
    `order_id` INT NOT NULL AUTO_INCREMENT,
    `shop_name` VARCHAR(50) NOT NULL,
    `order_money` INT NOT NULL,
    `order_way` VARCHAR(50) NOT NULL,
    `cons_phone` VARCHAR(50) NOT NULL,
    `cons_name` VARCHAR(50) NOT NULL,
    `cons_addre` VARCHAR(50) NOT NULL,
    `checked` INT DEFAULT 0,
    `create_time` VARCHAR(50),
    `rated` INT NULL DEFAULT 0,
    PRIMARY KEY (`order_id`),
    UNIQUE INDEX `order_id` (`order_id`),
    INDEX `shop_name` (`shop_name`),
    INDEX `order_money` (`order_money`),
    INDEX `order_way` (`order_way`),
    INDEX `cons_phone` (`cons_phone`),
    INDEX `cons_name` (`cons_name`),
    INDEX `cons_addre` (`cons_addre`),
    INDEX `checked` (`checked`),
    INDEX `create_time` (`create_time`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4; -- 创建 oorder 表的结构

-- 向 oorder 表插入数据
-- INSERT INTO `oorder` VALUES
    

-- 创建 orderway 表
DROP TABLE IF EXISTS `orderway`;
CREATE TABLE `orderway` (
    `orderway_name` VARCHAR(50) NOT NULL COMMENT '订餐方式',
    `count` INT NOT NULL COMMENT '该种方式的订餐数量',
    PRIMARY KEY (`orderway_name`),
    UNIQUE INDEX `orderway_name` (`orderway_name`),
    INDEX `count` (`count`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; -- 创建 orderway 表的结构

-- 向 orderway 表插入数据
-- INSERT INTO `orderway` VALUES
    -- ('网上订餐', 51),
    -- ('人工订餐', 108);

-- 创建 server 表（我们觉得可以删掉，并且在fastfood_shop 里面增加店主字段）
DROP TABLE IF EXISTS `server`;
CREATE TABLE `server` (
    `service_id` VARCHAR(50) NOT NULL COMMENT '服务员编号',
    `service_name` VARCHAR(50) NOT NULL,
    `fastfood_shop_name` VARCHAR(50) NOT NULL COMMENT '所在的店铺名字',
    PRIMARY KEY (`service_id`),
    UNIQUE INDEX `service_id` (`service_id`),
    INDEX `service_name` (`service_name`),
    INDEX `fastfood_shop_name` (`fastfood_shop_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; -- 创建 server 表的结构

-- 向 server 表插入数据
-- INSERT INTO `server` VALUES
    

-- 创建 user 表
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(20) NOT NULL,
    `password` VARCHAR(500) NOT NULL,-- 增长（因为hash处理之后，数据太长）
    `telephone` VARCHAR(20) NOT NULL,
    `role` INT NOT NULL,
    PRIMARY KEY

(`id`),
    UNIQUE INDEX `id` (`id`),
    INDEX `username` (`username`),
    INDEX `password` (`password`),
    INDEX `telephone` (`telephone`),
    INDEX `role` (`role`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4; -- 创建 user 表的结构

-- 向 user 表插入数据
-- INSERT INTO `user` VALUES
    

-- 创建 user_msg 表
DROP TABLE IF EXISTS `user_msg`;
CREATE TABLE `user_msg` (
    `id` INT UNSIGNED NULL DEFAULT NULL,
    `real_name` VARCHAR(50) NOT NULL,
    `sex` VARCHAR(50) NOT NULL,
    `age` INT NOT NULL,
    `mail` VARCHAR(50) NOT NULL,
    `phone` VARCHAR(50) NOT NULL,
    `user_name` VARCHAR(50) NOT NULL,
    INDEX `userid` (`id`),
    INDEX `real_name` (`real_name`),
    INDEX `sex` (`sex`),
    INDEX `age` (`age`),
    INDEX `mail` (`mail`),
    INDEX `phone` (`phone`),
    INDEX `user_name` (`user_name`),
    CONSTRAINT `userid` FOREIGN KEY (`id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; -- 创建 user_msg 表的结构


-- 创建 wuliu 表
DROP TABLE IF EXISTS `wuliu`;
CREATE TABLE `wuliu` (
    `order_id` INT NOT NULL COMMENT '订单的编号',
    `cons_phone` VARCHAR(50) NOT NULL,
    `disp_id` VARCHAR(50) NOT NULL,
    `deliver_time` VARCHAR(50) NOT NULL,
    `ended` INT NOT NULL DEFAULT 0 COMMENT '是否结束',
    PRIMARY KEY (`order_id`),
    UNIQUE INDEX `order_id` (`order_id`),
    INDEX `cons_phone` (`cons_phone`),
    INDEX `disp_id` (`disp_id`),
    INDEX `deliver_time` (`deliver_time`),
    INDEX `ended` (`ended`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; -- 创建 wuliu 表的结构

-- 向 wuliu 表插入数据
-- INSERT INTO `wuliu` VALUES
    

-- 创建 sended_order 视图
DROP VIEW IF EXISTS `sended_order`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `sended_order` AS 
    SELECT `oorder`.`order_id` AS `order_id`,
        `oorder`.`shop_name` AS `shop_name`,
        `oorder`.`order_money` AS `order_money`,
        `oorder`.`order_way` AS `order_way`,
        `oorder`.`cons_phone` AS `cons_phone`,
        `oorder`.`cons_name` AS `cons_name`,
        `oorder`.`cons_addre` AS `cons_addre`,
        `wuliu`.`disp_id` AS `disp_id`,
        `wuliu`.`deliver_time` AS `deliver_time`,
        `dispatcher`.`dispatcher_phone` AS `dispatcher_phone`
    FROM ((`oorder`
        JOIN `wuliu` ON ((`oorder`.`order_id` = `wuliu`.`order_id`)))
        JOIN `dispatcher` ON ((`wuliu`.`disp_id` = `dispatcher`.`dispatcher_id`)))
    WHERE (`oorder`.`checked` = 2); -- 创建 sended_order 视图

-- 创建 sending_order 视图
DROP VIEW IF EXISTS `sending_order`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `sending_order` AS 
    SELECT `oorder`.`order_id` AS `order_id`,
        `oorder`.`shop_name` AS `shop_name`,
        `oorder`.`order_money` AS `order_money`,
        `oorder`.`order_way` AS `order_way`,
        `oorder`.`cons_phone` AS `cons_phone`,
        `oorder`.`cons_name` AS `cons_name`,
        `oorder`.`cons_addre` AS `cons_addre`,
        `wuliu`.`disp_id` AS `disp_id`,
        `wuliu`.`deliver_time` AS `deliver_time`,
        `dispatcher`.`dispatcher_phone` AS `dispatcher_phone`
    FROM ((`oorder`
        JOIN `wuliu` ON ((`oorder`.`order_id` = `wuliu`.`order_id`)))
        JOIN `dispatcher` ON ((`wuliu`.`disp_id` = `dispatcher`.`dispatcher_id`)))
    WHERE (`oorder`.`checked` = 1); -- 创建 sending_order 视图

-- 创建 oorder 表的触发器
DROP TRIGGER IF EXISTS `order_insert`;
delimiter ;;
CREATE TRIGGER `order_insert` AFTER INSERT ON `oorder` FOR EACH ROW
BEGIN
    UPDATE orderway 
    SET count = count + 1 
    WHERE orderway_name = new.order_way;
END;;
delimiter ;

DROP TRIGGER IF EXISTS `order_insert_sale`;
delimiter ;;
CREATE TRIGGER `order_insert_sale` AFTER INSERT ON `oorder` FOR EACH ROW
BEGIN
    UPDATE fastfood_shop 
    SET m_sale_v = m_sale_v + 1 
    WHERE shop_name = new.shop_name;
END;;
delimiter ;

DROP TRIGGER IF EXISTS `order_update`;
delimiter ;;
CREATE TRIGGER `order_update` AFTER UPDATE ON `oorder` FOR EACH ROW
BEGIN
    IF (new.order_way != old.order_way) THEN
        UPDATE orderway 
        SET count = count - 1 
        WHERE orderway_name = old.order_way;
        UPDATE orderway 
        SET count = count + 1 
        WHERE orderway_name = new.order_way;
    END IF;
END;;
delimiter ;

DROP TRIGGER IF EXISTS `order_delete`;
delimiter ;;
CREATE TRIGGER `order_delete` AFTER DELETE ON `oorder` FOR EACH ROW
BEGIN
    UPDATE orderway 
    SET count = count - 1 
    WHERE orderway_name = old.order_way;
END;;
delimiter ;

DROP TRIGGER IF EXISTS `order_delete_sale`;
delimiter ;;
CREATE TRIGGER `order_delete_sale` AFTER DELETE ON `oorder` FOR EACH ROW
BEGIN
    UPDATE fastfood_shop 
    SET m_sale_v = m_sale_v - 1 
    WHERE shop_name = old.shop_name;
END;;
delimiter ;

-- 创建 wuliu 表的触发器
DROP TRIGGER IF EXISTS `wuliu_insert`;
delimiter ;;
CREATE TRIGGER `wuliu_insert` AFTER INSERT ON `wuliu` FOR EACH ROW
BEGIN
	UPDATE oorder 
    SET checked = 1 
    WHERE order_id = new.order_id;
END;;
delimiter ;

-- 创建好评的触发器
DELIMITER $$

CREATE TRIGGER update_hp_num AFTER UPDATE ON oorder
FOR EACH ROW
BEGIN
    IF NEW.rated = 1 AND OLD.rated != 1 THEN
        UPDATE fastfood_shop
        SET hp_num = hp_num + 1
        WHERE shop_name = NEW.shop_name;
    END IF;
END$$

DELIMITER ;


-- 创建差评的触发器
DELIMITER $$

CREATE TRIGGER update_cp_num AFTER UPDATE ON oorder
FOR EACH ROW
BEGIN
    IF NEW.rated = 2 AND OLD.rated != 2 THEN
        UPDATE fastfood_shop
        SET cp_num = cp_num + 1
        WHERE shop_name = NEW.shop_name;
    END IF;
END$$

DELIMITER ;



-- 恢复外键约束检查
-- SET FOREIGN_KEY_CHECKS = 1;
