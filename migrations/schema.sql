-- tfluxv3.job_feed_config definition

CREATE TABLE `job_feed_config` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `query` json NOT NULL,
  `token` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `job_feed_config_unique` (`token`)
);