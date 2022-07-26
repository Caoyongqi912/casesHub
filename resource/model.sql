
CREATE TABLE cases (
	id INTEGER NOT NULL AUTO_INCREMENT,
	create_time DATE COMMENT '创建时间',
	update_time DATE COMMENT '修改时间',
	part VARCHAR(20) COMMENT '模块',
	title VARCHAR(20) NOT NULL COMMENT '用例名称',
	`desc` VARCHAR(100) NOT NULL COMMENT '用例描述',
	creator INTEGER NOT NULL COMMENT '创建人',
	steps JSON NOT NULL COMMENT '用例步骤',
	status ENUM('QUEUE','TESTING','BLOCK','SKIP','PASS','FAIL','CLOSE') COMMENT '状态' DEFAULT 'QUEUE',
	platform ENUM('IOS','ANDROID','WEB','PC','APP') COMMENT '所属平台' DEFAULT 'IOS',
	case_level ENUM('P1','P2','P3','P4') COMMENT '用例等级' DEFAULT 'P1',
	case_type ENUM('功能','接口','性能') COMMENT '用例类型' DEFAULT '功能',
	prd VARCHAR(200) NOT NULL COMMENT '需求链接',
	updater INTEGER COMMENT '修改人',
	mark VARCHAR(100) COMMENT '用例备注',
	`versionID` INTEGER COMMENT '所属版本',
	`productID` INTEGER COMMENT '所属产品',
	PRIMARY KEY (id),
	UNIQUE (title),
	FOREIGN KEY(`versionID`) REFERENCES version (id),
	FOREIGN KEY(`productID`) REFERENCES product (id)
)



CREATE TABLE bug (
	id INTEGER NOT NULL AUTO_INCREMENT,
	create_time DATE COMMENT '创建时间',
	update_time DATE COMMENT '修改时间',
	title VARCHAR(20) COMMENT 'bug名称',
	`desc` VARCHAR(100) COMMENT 'bug描述',
	tester VARCHAR(20) NOT NULL COMMENT '测试',
	developer VARCHAR(20) NOT NULL COMMENT '测试',
	pr VARCHAR(20) NOT NULL COMMENT '产品',
	level ENUM('P1','P2','P3','P4') COMMENT 'BUG等级' DEFAULT 'P1',
	status ENUM('OPEN','CLOSE','BLOCK') COMMENT 'BUG状态' DEFAULT 'OPEN',
	file VARCHAR(50) COMMENT '附件地址',
	mark VARCHAR(100) COMMENT 'BUG备注',
	`caseID` INTEGER COMMENT '所属用例',
	PRIMARY KEY (id),
	UNIQUE (title),
	FOREIGN KEY(`caseID`) REFERENCES cases (id)
)