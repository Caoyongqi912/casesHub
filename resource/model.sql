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
VALUES (1, 'qygKojXzJkOFElKendjU', '2022-08-08', '2022-08-08', 'DEV', 'DEV team', 1);
INSERT INTO department (id, uid, create_time, update_time, name, `desc`, `adminID`)
VALUES (2, 'ZjIcsbULvhGxhWEbyToL', '2022-08-08', '2022-08-08', 'QA', 'QA team', 1);



CREATE TABLE project
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATE COMMENT '创建时间',
    update_time DATE COMMENT '修改时间',
    name        VARCHAR(20) COMMENT '项目名称',
    `desc`      VARCHAR(100) COMMENT '项目描述',
    `adminID`   INTEGER COMMENT '项目负责人ID',
    `adminNAme` VARCHAR(50) COMMENT '项目负责人姓名',
    PRIMARY KEY (id),
    UNIQUE (name)
);
insert into project (id, uid, create_time, update_time, name, `desc`, adminID)
values (1, 'SFqIOVNUIxWUGHjyZVAT', '2022-08-09', '2022-08-09', 'p1', 'xxxxxxxxxxxxxxxxxxxxxxx', 1);
insert into project (id, uid, create_time, update_time, name, `desc`, adminID)
values (2, 'lTdDWeAvmBMFsHXmqlcC', '2022-08-09', '2022-08-09', 'p2', 'xxxxxxxxxxxxxxxxxxxxxxx', 2);


CREATE TABLE platform
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATE COMMENT '创建时间',
    update_time DATE COMMENT '修改时间',
    name        ENUM ('IOS','ANDROID','WEB','PC') COMMENT '平台名称',
    PRIMARY KEY (id)
);
INSERT INTO platform(id, uid, create_time, update_time, name)
VALUES (1, 'yGlrWVBxHBYFiHLOkntk', '2022-08-09', '2022-08-09', 'IOS');
INSERT INTO platform(id, uid, create_time, update_time, name)
VALUES (2, 'SgKpUtQZrfcAoeAZGwSk', '2022-08-09', '2022-08-09', 'ANDROID');

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
    gender         INTEGER COMMENT '性别',
    tag            INTEGER COMMENT '标签',
    avatar         VARCHAR(400) COMMENT '头像',
    `isAdmin`      BOOL COMMENT '管理',
    `departmentID` INTEGER COMMENT '所属部门',
    PRIMARY KEY (id),
    UNIQUE (phone),
    UNIQUE (email),
    FOREIGN KEY (`departmentID`) REFERENCES department (id)
);
INSERT INTO user (id, uid, create_time, update_time, username, phone, password, email, gender, tag, avatar, `isAdmin`,
                  `departmentID`)
VALUES (1, 'OAzksgGicHcwpqgRgXZU', '2022-08-08', '2022-08-08', 'ADMIN', '17612395915',
        'pbkdf2:sha256:260000$jSVPQ77vpnkERsSE$6187321158c003e28cdfe32383b19423e7fa64f2c68cde7c55b830a720e07a3e',
        'ADMIN@caseHub.com', 1, 0, null, 1, null);
INSERT INTO user (id, uid, create_time, update_time, username, phone, password, email, gender, tag, avatar, `isAdmin`,
                  `departmentID`)
values (2, 'cxpKyEisuRZoepPFQGaO', '2022-08-08', '2022-08-08', 'dawa', '17612395913',
        'pbkdf2:sha256:260000$jIOla04MKwhl61L2$78e44f053a2bc19734538e36bd16e349ceb1d643356756cd5a5257da9ec9509f',
        'dawa@caseHub.com', 1, 1, null, 0, 1);

CREATE TABLE case_part
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATE COMMENT '创建时间',
    update_time DATE COMMENT '修改时间',
    `partName`  VARCHAR(20) UNIQUE COMMENT '用例模块',
    `projectID` INTEGER COMMENT '所属产品',
    PRIMARY KEY (id),
    FOREIGN KEY (`projectID`) REFERENCES project (id)
);
insert into case_part(id, uid, create_time, update_time, partName, projectID)
VALUES (1, 'awpTEztUPovjrtbwoJGt', '2022-08-09', '2022-08-09', 'part1', 1);



CREATE TABLE version
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATE COMMENT '创建时间',
    update_time DATE COMMENT '修改时间',
    name        VARCHAR(20) COMMENT '版本名称',
    `desc`      VARCHAR(100) COMMENT '版本描述',
    `projectID` INTEGER COMMENT '所属产品',
    PRIMARY KEY (id),
    FOREIGN KEY (`projectID`) REFERENCES project (id) ON DELETE CASCADE
);

insert into version(id, uid, create_time, update_time, name, `desc`, projectID)
values (1, 'gYPeeSKTZAnJrDPveQgJ', '2022-08-09', '2022-08-09', 'version 1.0', 'v1 banben', 1);
insert into version(id, uid, create_time, update_time, name, `desc`, projectID)
values (1, 'xlpogVbnHvKLyMfhPYDL', '2022-08-09', '2022-08-09', 'version 1.0', 'v1 banben', 2);



CREATE TABLE project_user
(
    project_id INTEGER NOT NULL,
    user_id    INTEGER NOT NULL,
    PRIMARY KEY (project_id, user_id),
    FOREIGN KEY (project_id) REFERENCES project (id),
    FOREIGN KEY (user_id) REFERENCES user (id)
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
    type         INTEGER COMMENT 'bug类型',
    level        INTEGER COMMENT 'BUG等级',
    status       INTEGER COMMENT 'BUG状态',
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

CREATE TABLE cases
(
    id           INTEGER      NOT NULL AUTO_INCREMENT,
    uid          VARCHAR(50) COMMENT '唯一标识',
    create_time  DATE COMMENT '创建时间',
    update_time  DATE COMMENT '修改时间',
    title        VARCHAR(20)  NOT NULL COMMENT '用例名称',
    `desc`       VARCHAR(100) NOT NULL COMMENT '用例描述',
    tag          INTEGER COMMENT '用例标签',
    case_level   INTEGER COMMENT '用例等级',
    case_type    INTEGER COMMENT '用例类型',
    status       INTEGER COMMENT '用例状态',
    setup        VARCHAR(40) COMMENT '用例前置',
    info         JSON         NOT NULL COMMENT '用例步骤与预期结果',
    mark         VARCHAR(100) COMMENT '用例备注',
    `partID`     INTEGER COMMENT '模块',
    `projectID`  INTEGER COMMENT '所属产品',
    `platformID` INTEGER COMMENT '所属平台',
    `versionID`  INTEGER COMMENT '所属版本',
    creator      INTEGER      NOT NULL COMMENT '创建人',
    updater      INTEGER COMMENT '修改人',
    PRIMARY KEY (id),
    FOREIGN KEY (`partID`) REFERENCES case_part (id) ON DELETE SET NULL,
    FOREIGN KEY (`projectID`) REFERENCES project (id) ON DELETE SET NULL,
    FOREIGN KEY (`platformID`) REFERENCES platform (id) ON DELETE SET NUll,
    FOREIGN KEY (`versionID`) REFERENCES version (id) ON DELETE SET NUll
);
insert into cases(id, uid, create_time, update_time, title, `desc`, tag, case_level, case_type, status, setup, info,
                  mark, partID, projectID, platformID, versionID, creator, updater)
VALUES (1, 'vCesTlgzDczVubtBjABF', '2022-08-09', '2022-08-09', 'case1', 'case1 desc', 1, 4, 1, 1, null, '[
  {
    "do": "sdfdsfdsfdsfsdf",
    "exp": "dasasas",
    "step": 1
  },
  {
    "do": "fdsfsdfsdfsddsfsdf",
    "exp": "dasdasdasnnf",
    "step": 2
  }
]', null, 1, 1, 1, 1, 1, null);

insert into cases(id, uid, create_time, update_time, title, `desc`, tag, case_level, case_type, status, setup, info,
                  mark, partID, projectID, platformID, versionID, creator, updater)
values (3, 'tSDptJEdrGPgLNvqdEkx', '2022-08-09', '2022-08-09', 'case2', 'case2 desc', 1, 4, 1, 1, null, '[
  {
    "do": "xxx",
    "exp": "xxx",
    "step": 1
  },
  {
    "do": "xxx",
    "exp": "xxxx",
    "step": 2
  }
]', null, 1, 1, 1, 1, 1, null);

CREATE TABLE case_excel
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATE COMMENT '创建时间',
    update_time DATE COMMENT '修改时间',
    `fileName`  VARCHAR(50) COMMENT '附件名',
    `filePath`  VARCHAR(200) COMMENT '附件路径',
    PRIMARY KEY (id),
    UNIQUE (`fileName`)
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
    type         INTEGER COMMENT 'bug类型',
    level        INTEGER COMMENT 'BUG等级',
    status       INTEGER COMMENT 'BUG状态',
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



CREATE TABLE interface
(
    id                INTEGER NOT NULL AUTO_INCREMENT,
    uid               VARCHAR(50) COMMENT '唯一标识',
    create_time       DATETIME COMMENT '创建时间',
    update_time       DATETIME COMMENT '修改时间',
    title             VARCHAR(40) COMMENT '标题',
    `desc`            VARCHAR(200) COMMENT '描述',
    mark              VARCHAR(200) COMMENT '备注',
    creator           INTEGER COMMENT '创建人',
    updater           INTEGER COMMENT '修改人',
    `connectTimeout`  INTEGER COMMENT '连接超时',
    `responseTimeout` INTEGER COMMENT '请求超时',
    `caseID`          INTEGER COMMENT '关联的用例',
    `partID`          INTEGER COMMENT '所属模块',
    `projectID`       INTEGER COMMENT '所属产品',
    `versionID`       INTEGER COMMENT '所属版本',
    steps             JSON COMMENT '接口步骤',
    PRIMARY KEY (id),
    FOREIGN KEY (`partID`) REFERENCES case_part (id) ON DELETE SET NULL,
    FOREIGN KEY (`projectID`) REFERENCES project (id) ON DELETE SET NULL,
    FOREIGN KEY (`versionID`) REFERENCES version (id) ON DELETE SET NUll
);


CREATE TABLE api_host
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATETIME COMMENT '创建时间',
    update_time DATETIME COMMENT '修改时间',
    name        VARCHAR(20) COMMENT 'host 名称',
    host        VARCHAR(50) COMMENT 'host 值',
    `projectID` INTEGER COMMENT '所属版本',
    PRIMARY KEY (id),
    FOREIGN KEY (`projectID`) REFERENCES project (id) ON DELETE SET NUll
);
CREATE TABLE interface_result
(
    id            INTEGER                 NOT NULL AUTO_INCREMENT,
    uid           VARCHAR(50) COMMENT '唯一标识',
    create_time   DATETIME COMMENT '创建时间',
    update_time   DATETIME COMMENT '修改时间',
    `interfaceID` INTEGER COMMENT '所属用例',
    `resultInfo`  JSON COMMENT '响应结果',
    `starterID`   INTEGER COMMENT '运行人ID',
    `starterName` VARCHAR(20) COMMENT '运行人姓名',
    `useTime`     VARCHAR(20) COMMENT '用时',
    status        ENUM ('SUCCESS','FAIL') NOT NULL COMMENT '运行状态',
    PRIMARY KEY (id),
    FOREIGN KEY (`interfaceID`) REFERENCES interface (id) ON DELETE CASCADE
)