CREATE TABLE tfluxv3.job_feed_config (
	id BIGINT auto_increment NOT NULL,
	query json NOT NULL,
	CONSTRAINT job_feed_config_pk PRIMARY KEY (id)
);
