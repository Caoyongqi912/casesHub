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
VALUES (1, 'sWyPruqCGakgjwedMItN', 2022 - 07 - 31, 2022 - 07 - 31, 'QA', 'QA team', 1);
INSERT INTO department (id, uid, create_time, update_time, name, `desc`, `adminID`)
VALUES (2, 'mUAFYnxNHKolWUcMziui', 2022 - 07 - 31, 2022 - 07 - 31, 'DEV', 'DEV team', 1);



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
        'ADMIN@caseHub.com', null, TRUE, 'MALE', 1, 'ADMIN')


