CREATE TABLE department
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATE COMMENT '创建时间',
    update_time DATE COMMENT '修改时间',
    name        VARCHAR(20) COMMENT '用户名',
    `desc`      VARCHAR(40) COMMENT '部门描述',
    `adminID`   INTEGER COMMENT '部门负责人',
    PRIMARY KEY (id),
    UNIQUE (name)
);
INSERT INTO department (id, uid, create_time, update_time, name, `desc`, `adminID`)
VALUES (1, 'sWyPruqCGakgjwedMItN', '2022-07-31', '2022-07-31', 'QA', 'QA team', 1);
INSERT INTO department (id, uid, create_time, update_time, name, `desc`, `adminID`)
VALUES (2, 'mUAFYnxNHKolWUcMziui', '2022-07-31', '2022-07-31', 'DEV', 'DEV team', 1);



CREATE TABLE user
(
    id             INTEGER NOT NULL AUTO_INCREMENT,
    uid            VARCHAR(50) COMMENT '唯一标识',
    create_time    DATE COMMENT '创建时间',
    update_time    DATE COMMENT '修改时间',
    username       VARCHAR(20) COMMENT '用户名',
    phone          VARCHAR(12) COMMENT '手机',
    password       VARCHAR(200) COMMENT '密码',
    email          VARCHAR(40) COMMENT '邮箱',
    gender         ENUM ('MALE','FEMALE') COMMENT '性别' DEFAULT 'MALE',
    avatar         VARCHAR(400) COMMENT '头像',
    isAdmin        BOOL COMMENT '管理',
    tag            ENUM ('QA','PR','DEV','ADMIN') COMMENT '标签',
    `departmentID` INTEGER COMMENT '所属部门',
    PRIMARY KEY (id),
    UNIQUE (username),
    UNIQUE (phone),
    UNIQUE (email),
    FOREIGN KEY (`departmentID`) REFERENCES department (id)
);

#添加管理员
INSERT INTO user (uid, create_time, update_time, username, phone, password, email, gender, avatar, `isAdmin`, tag,
                  `departmentID`)
VALUES ('4e111a28-e68c-429c-95f6-2f7370a4fbdd', '2022-07-31', '2022-07-31', 'ADMIN', '17612395915',
        'pbkdf2:sha256:260000$7dfUoYrnI6Ko3mDu$0c86e80f77259c2b6589c36e6f63ce323ecc28a96f05f72814406b4d5e1bb4e4',
        'ADMIN@caseHub.com', 'MALE', null, TRUE, 1, null);



CREATE TABLE project
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATE COMMENT '创建时间',
    update_time DATE COMMENT '修改时间',
    name        VARCHAR(20) COMMENT '项目名称',
    `desc`      VARCHAR(100) COMMENT '项目描述',
    `adminID`   INTEGER COMMENT '项目负责人',
    PRIMARY KEY (id),
    UNIQUE (name)
);
INSERT INTO project (id, uid, create_time, update_time, name, `desc`, `adminID`)
VALUES (1, 'MuLaJydzZlrSPPGSENEa', '2022-07-31', '2022-07-31', 'P1', 'xxxxxxxxxxxxxxxxxxxxxxx', 1);


CREATE TABLE product
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATE COMMENT '创建时间',
    update_time DATE COMMENT '修改时间',
    name        VARCHAR(20) COMMENT '产品名称',
    `desc`      VARCHAR(100) COMMENT '产品描述',
    `adminID`   INTEGER COMMENT '产品负责人',
    `projectID` INTEGER NOT NULL COMMENT '所属项目',
    PRIMARY KEY (id),
    UNIQUE (name),
    FOREIGN KEY (`projectID`) REFERENCES project (id)
);

CREATE TABLE product_user
(
    `productID` INTEGER,
    `userID`    INTEGER,
    FOREIGN KEY (`productID`) REFERENCES product (id),
    FOREIGN KEY (`userID`) REFERENCES user (id)
);

CREATE TABLE version (
	id INTEGER NOT NULL AUTO_INCREMENT,
	uid VARCHAR(50) COMMENT '唯一标识',
	create_time DATE COMMENT '创建时间',
	update_time DATE COMMENT '修改时间',
	name VARCHAR(20) COMMENT '版本名称',
	`desc` VARCHAR(100) COMMENT '版本描述',
	`productID` INTEGER COMMENT '所属产品',
	PRIMARY KEY (id),
	FOREIGN KEY(`productID`) REFERENCES product (id) ON DELETE CASCADE
)