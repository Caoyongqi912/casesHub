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
    `projectID` INTEGER NOT NULL COMMENT '所属项目',
    PRIMARY KEY (id),
    UNIQUE (name),
    FOREIGN KEY (`projectID`) REFERENCES project (id)
);
INSERT INTO product (id, uid, create_time, update_time, name, `desc`, projectID)
VALUES (1, 'ZsWBjEgGrRQijRZKzpZA', '2022-08-01', '2022-08-01', 'pro1', 'pro1 desc', 2);
INSERT INTO product (id, uid, create_time, update_time, name, `desc`, projectID)
VALUES (2, 'yyuiZSdSmHvwjUslsOHv', '2022-08-01', '2022-08-01', 'pro2', 'pro2 for project 1', 2);
INSERT INTO product (id, uid, create_time, update_time, name, `desc`, projectID)
VALUES (3, 'YXSVrSgQxowjjtlnPfFI', '2022-08-01', '2022-08-01', 'pro3', 'pro3 desc', 2);
INSERT INTO product (id, uid, create_time, update_time, name, `desc`, projectID)
VALUES (4, 'bfvMFjEpLdxbQuoMxvLL', '2022-08-01', '2022-08-01', 'pro4', 'pro4 desc', 3);
INSERT INTO product (id, uid, create_time, update_time, name, `desc`, projectID)
VALUES (5, 'eJpUgXNBrCfAYiKWJyxL', '2022-08-01', '2022-08-01', 'pro5', 'pro5 desc', 3);

CREATE TABLE product_user
(
    `productID` INTEGER,
    `userID`    INTEGER,
    FOREIGN KEY (`productID`) REFERENCES product (id),
    FOREIGN KEY (`userID`) REFERENCES user (id)
);

CREATE TABLE version
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATE COMMENT '创建时间',
    update_time DATE COMMENT '修改时间',
    name        VARCHAR(20) COMMENT '版本名称',
    `desc`      VARCHAR(100) COMMENT '版本描述',
    `productID` INTEGER COMMENT '所属产品',
    PRIMARY KEY (id),
    FOREIGN KEY (`productID`) REFERENCES product (id) ON DELETE CASCADE
);
INSERT INTO version (id, uid, create_time, update_time, name, `desc`, productID)
VALUES (1, 'eErlYCZXtbolWXSFlWtD', '2022-08-01', '2022-08-01', '1.0', null, 4);
INSERT INTO version (id, uid, create_time, update_time, name, `desc`, productID)
VALUES (2, 'vmGwQrCzDxSLrTDivkTl', '2022-08-01', '2022-08-01', '1.0', null, 5);
INSERT INTO version (id, uid, create_time, update_time, name, `desc`, productID)
VALUES (3, 'qQbpCRnmROuxhutwLFGS', '2022-08-01', '2022-08-01', '1.1', null, 5);

CREATE TABLE platform
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATE COMMENT '创建时间',
    update_time DATE COMMENT '修改时间',
    name        ENUM ('IOS','ANDROID','WEB','PC') COMMENT '平台名称',
    PRIMARY KEY (id)
);
INSERT INTO platform (id, uid, create_time, update_time, name)
VALUES (1, 'XwrnNjNsHrKSrXWsoTqj', '2022-08-02', '2022-08-02', 'IOS');
INSERT INTO platform (id, uid, create_time, update_time, name)
VALUES (2, 'wkDKNwEcZxHAODJPbSHJ', '2022-08-02', '2022-08-02', 'ANDROID');
INSERT INTO platform (id, uid, create_time, update_time, name)
VALUES (3, 'ThlPwvBcfWOdioeNQPgO', '2022-08-02', '2022-08-02', 'PC');
INSERT INTO platform (id, uid, create_time, update_time, name)
VALUES (4, 'EQhfXBJxtxVDAXLZXcYH', '2022-08-02', '2022-08-02', 'WEB');

CREATE TABLE case_part
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATE COMMENT '创建时间',
    update_time DATE COMMENT '修改时间',
    `partName`  VARCHAR(20) COMMENT '用例模块',
    `productID` INTEGER COMMENT '所属产品',
    PRIMARY KEY (id),
    FOREIGN KEY (`productID`) REFERENCES product (id)
);

CREATE TABLE cases
(
    id           INTEGER      NOT NULL AUTO_INCREMENT,
    uid          VARCHAR(50) COMMENT '唯一标识',
    create_time  DATE COMMENT '创建时间',
    update_time  DATE COMMENT '修改时间',
    title        VARCHAR(20)  NOT NULL COMMENT '用例名称',
    tag          ENUM ('常规','冒烟') COMMENT '用例标签'                                              DEFAULT '常规',
    `desc`       VARCHAR(100) NOT NULL COMMENT '用例描述',
    case_level   ENUM ('P1','P2','P3','P4') COMMENT '用例等级',
    case_type    ENUM ('功能','接口','性能') COMMENT '用例类型'                                         DEFAULT '功能',
    status       ENUM ('QUEUE','TESTING','BLOCK','SKIP','PASS','FAIL','CLOSE') COMMENT '用例状态' DEFAULT 'QUEUE',
    setup        VARCHAR(40) COMMENT '用例前置',
    info         JSON         NOT NULL COMMENT '用例步骤与预期结果',
    mark         VARCHAR(100) COMMENT '用例备注',
    `partID`     INTEGER COMMENT '模块',
    `productID`  INTEGER COMMENT '所属产品',
    `platformID` INTEGER COMMENT '所属平台',
    creator      INTEGER      NOT NULL COMMENT '创建人',
    updater      INTEGER COMMENT '修改人',
    PRIMARY KEY (id),
    FOREIGN KEY (`partID`) REFERENCES case_part (id) ON DELETE SET NULL,
    FOREIGN KEY (`productID`) REFERENCES product (id) ON DELETE SET NULL,
    FOREIGN KEY (`platformID`) REFERENCES platform (id) ON DELETE SET NUll
);

CREATE TABLE bug
(
    id           INTEGER     NOT NULL AUTO_INCREMENT,
    uid          VARCHAR(50) COMMENT '唯一标识',
    create_time  DATE COMMENT '创建时间',
    update_time  DATE COMMENT '修改时间',
    title        VARCHAR(20) COMMENT 'bug名称',
    `desc`       VARCHAR(100) COMMENT 'bug描述',
    tag          VARCHAR(30) COMMENT 'bug标签',
    tester       VARCHAR(20) NOT NULL COMMENT '测试人',
    developer    VARCHAR(20) COMMENT '开发',
    pr           VARCHAR(20) COMMENT '产品',
    bug_type     ENUM ('线上问题','优化','缺陷') COMMENT 'bug类型',
    level        ENUM ('P1','P2','P3','P4') COMMENT 'BUG等级',
    status       ENUM ('OPEN','CLOSE','BLOCK') COMMENT 'BUG状态' DEFAULT 'OPEN',
    file         VARCHAR(50) COMMENT '附件地址',
    mark         VARCHAR(100) COMMENT 'BUG备注',
    `platformID` INTEGER COMMENT '所属平台',
    `versionID`  INTEGER COMMENT '所属版本',
    `caseID`     INTEGER COMMENT '所属用例',
    PRIMARY KEY (id),
    FOREIGN KEY (`platformID`) REFERENCES platform (id) ON DELETE SET NUll,
    FOREIGN KEY (`versionID`) REFERENCES version (id) ON DELETE SET NULL,
    FOREIGN KEY (`caseID`) REFERENCES cases (id) ON DELETE SET NULL
);
