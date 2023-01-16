CREATE TABLE department
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATETIME COMMENT '创建时间',
    update_time DATETIME COMMENT '修改时间',
    name        VARCHAR(20) COMMENT '用户名',
    `desc`      VARCHAR(40) COMMENT '部门描述',
    `adminID`   INTEGER COMMENT '部门负责人',
    PRIMARY KEY (id),
    UNIQUE (name)
);
CREATE TABLE user
(
    id               INTEGER NOT NULL AUTO_INCREMENT,
    uid              VARCHAR(50) COMMENT '唯一标识',
    create_time      DATETIME COMMENT '创建时间',
    update_time      DATETIME COMMENT '修改时间',
    username         VARCHAR(20) COMMENT '用户名',
    phone            VARCHAR(12) COMMENT '手机',
    password         VARCHAR(200) COMMENT '密码',
    email            VARCHAR(40) COMMENT '邮箱',
    gender           INTEGER COMMENT '性别',
    avatar           VARCHAR(400) COMMENT '头像',
    `isAdmin`        BOOL COMMENT '管理',
    `departmentID`   INTEGER COMMENT '所属部门',
    `departmentName` VARCHAR(20) COMMENT '所属部门名称',
    `tagName`        VARCHAR(20) COMMENT '对应标签名称',
    PRIMARY KEY (id),
    UNIQUE (phone),
    UNIQUE (email),
    FOREIGN KEY (`departmentID`) REFERENCES department (id) ON DELETE set null
);
CREATE TABLE `userTag`
(
    id             INTEGER NOT NULL AUTO_INCREMENT,
    uid            VARCHAR(50) COMMENT '唯一标识',
    create_time    DATETIME COMMENT '创建时间',
    update_time    DATETIME COMMENT '修改时间',
    name           VARCHAR(20) COMMENT '标签名称',
    `departmentID` INTEGER COMMENT '所属部门',
    PRIMARY KEY (id),
    UNIQUE (name),
    FOREIGN KEY (`departmentID`) REFERENCES department (id) ON DELETE set null
);
CREATE TABLE project
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATETIME COMMENT '创建时间',
    update_time DATETIME COMMENT '修改时间',
    name        VARCHAR(20) COMMENT '项目名称',
    `desc`      VARCHAR(100) COMMENT '项目描述',
    `adminID`   INTEGER COMMENT '项目负责人ID',
    `adminName` VARCHAR(20) COMMENT '项目负责人姓名',
    PRIMARY KEY (id),
    UNIQUE (name),
    UNIQUE (`adminName`)
);
CREATE TABLE platform
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATETIME COMMENT '创建时间',
    update_time DATETIME COMMENT '修改时间',
    name        VARCHAR(30) COMMENT '平台名称',
    PRIMARY KEY (id),
    UNIQUE (name)
);
CREATE TABLE file
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATETIME COMMENT '创建时间',
    update_time DATETIME COMMENT '修改时间',
    `fileName`  VARCHAR(50) COMMENT '附件名称',
    `fileType`  VARCHAR(100) COMMENT '附件格式',
    `filePath`  VARCHAR(100) COMMENT '路径',
    PRIMARY KEY (id)
);
CREATE TABLE report
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATETIME COMMENT '创建时间',
    update_time DATETIME COMMENT '修改时间',
    title       VARCHAR(20) COMMENT '名称',
    `desc`      VARCHAR(100) COMMENT '描述',
    version     VARCHAR(40) COMMENT '版本',
    status      ENUM ('RELEASE','UNRELEASE') COMMENT '发布状态' DEFAULT 'UNRELEASE',
    online      VARCHAR(20) COMMENT '上线时间',
    players     JSON COMMENT '参与人',
    bugs        JSON COMMENT 'bug',
    demands     JSON COMMENT '需求链接',
    PRIMARY KEY (id),
    UNIQUE (title)
);
CREATE TABLE version
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATETIME COMMENT '创建时间',
    update_time DATETIME COMMENT '修改时间',
    name        VARCHAR(20) COMMENT '版本名称',
    `desc`      VARCHAR(100) COMMENT '版本描述',
    `projectID` INTEGER COMMENT '所属产品',
    PRIMARY KEY (id),
    FOREIGN KEY (`projectID`) REFERENCES project (id) ON DELETE CASCADE
);
CREATE TABLE case_part
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATETIME COMMENT '创建时间',
    update_time DATETIME COMMENT '修改时间',
    `partName`  VARCHAR(20) COMMENT '用例模块',
    `projectID` INTEGER COMMENT '所属产品',
    PRIMARY KEY (id),
    FOREIGN KEY (`projectID`) REFERENCES project (id)
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
CREATE TABLE variable
(
    id          INTEGER NOT NULL AUTO_INCREMENT,
    uid         VARCHAR(50) COMMENT '唯一标识',
    create_time DATETIME COMMENT '创建时间',
    update_time DATETIME COMMENT '修改时间',
    `key`       VARCHAR(20) COMMENT '变量名称',
    val         VARCHAR(500) COMMENT '变量值',
    `desc`      VARCHAR(500) COMMENT '描述',
    creator     VARCHAR(20) COMMENT '创建人',
    updater     VARCHAR(20) COMMENT '修改人',
    `projectID` INTEGER COMMENT '所属项目',
    PRIMARY KEY (id),
    FOREIGN KEY (`projectID`) REFERENCES project (id) ON DELETE SET NUll
);
CREATE TABLE cases
(
    id           INTEGER      NOT NULL AUTO_INCREMENT,
    uid          VARCHAR(50) COMMENT '唯一标识',
    create_time  DATETIME COMMENT '创建时间',
    update_time  DATETIME COMMENT '修改时间',
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
CREATE TABLE project_user
(
    project_id INTEGER NOT NULL,
    user_id    INTEGER NOT NULL,
    PRIMARY KEY (project_id, user_id),
    FOREIGN KEY (project_id) REFERENCES project (id),
    FOREIGN KEY (user_id) REFERENCES user (id)
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
CREATE TABLE bug
(
    id            INTEGER     NOT NULL AUTO_INCREMENT,
    uid           VARCHAR(50) COMMENT '唯一标识',
    create_time   DATETIME COMMENT '创建时间',
    update_time   DATETIME COMMENT '修改时间',
    title         VARCHAR(20) COMMENT 'bug名称',
    `desc`        TEXT COMMENT 'bug描述',
    bug_tag       VARCHAR(30) COMMENT 'bug标签',
    `creatorID`   INTEGER     NOT NULL COMMENT '创建人id',
    `creatorName` VARCHAR(20) NOT NULL COMMENT '创建人',
    `updaterID`   INTEGER COMMENT '更新人ID',
    `updaterName` VARCHAR(20) COMMENT '更新人',
    `agentID`     INTEGER COMMENT '经办人ID',
    `agentName`   VARCHAR(20) NOT NULL COMMENT '经办人',
    bug_type      INTEGER COMMENT 'bug类型',
    bug_level     INTEGER COMMENT 'BUG等级',
    bug_status    INTEGER COMMENT 'BUG状态',
    files         JSON COMMENT '附件uid列',
    mark          VARCHAR(100) COMMENT 'BUG备注',
    `platformID`  INTEGER COMMENT '所属平台',
    `versionID`   INTEGER COMMENT '所属版本',
    `caseID`      INTEGER COMMENT '所属用例',
    PRIMARY KEY (id),
    FOREIGN KEY (`platformID`) REFERENCES platform (id) ON DELETE SET NUll,
    FOREIGN KEY (`versionID`) REFERENCES version (id) ON DELETE SET NULL,
    FOREIGN KEY (`caseID`) REFERENCES cases (id) ON DELETE SET NULL
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
);