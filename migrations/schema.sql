CREATE SCHEMA `jobfeed` ;

CREATE TABLE `jobfeed`.`config` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `client_id` bigint NOT NULL,
  `query` json NOT NULL,
  `token` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `job_feed_config_unique` (`token`)
);