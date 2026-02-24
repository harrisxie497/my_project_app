-- 为tasks表添加header_params字段
ALTER TABLE tasks ADD COLUMN header_params VARCHAR(1000) NULL COMMENT '表头参数JSON字符串';
