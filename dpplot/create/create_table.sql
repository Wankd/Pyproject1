create table `job_info`(
`job_name` VARCHAR(200) NOT NULL COMMENT '任务名称',
`person` VARCHAR(50) NOT NULL COMMENT '负责人',
`job_mas` VARCHAR(200) NOT NULL COMMENT '任务描述',
`run_time` VARCHAR(200) NOT NULL COMMENT '执行时间',
`into_table` VARCHAR(200) NOT NULL COMMENT '目标表',
`from_table` VARCHAR(200) NOT NULL COMMENT '来源表',
`fu_name` VARCHAR(200) NOT NULL COMMENT '父任务名称',
`zi_id` VARCHAR(200) NOT NULL COMMENT '子任务名称'
)
COMMENT='任务配置信息表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;



create table `job_run_msg`(
`job_name` VARCHAR(200) NOT NULL COMMENT '任务名称',
`sql_run` text NOT NULL COMMENT '执行sql',
`status` VARCHAR(50) NOT NULL COMMENT '任务状态',
`error` text NOT NULL COMMENT '错误日志',
`start_time` VARCHAR(200) NOT NULL COMMENT '执行时间',
`end_time` VARCHAR(200) NOT NULL COMMENT '结束时间',
`time_len` VARCHAR(8) NOT NULL COMMENT '执行时长'
)
COMMENT='任务执行日志表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;	


create table `task_running`(
`job_name` VARCHAR(200) NOT NULL COMMENT '任务名称',
`start_time` VARCHAR(200) NOT NULL COMMENT '执行时间'
)
COMMENT='正在执行任务表'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


aae002	number
aab301	varchar2(256)
jblx	varchar2(256)
csum	number
jbname	varchar2(256)
jzlx	varchar2(256)
tot	number


create table test(
`aae002` int(11) COMMENT '',
`aab301` VARCHAR(200) COMMENT '',
`jblx` VARCHAR(200) COMMENT '',
`csum` int(11) COMMENT '',
`jbname` VARCHAR(200) COMMENT '',
`jzlx` VARCHAR(200) COMMENT '',
`tot` int(11) COMMENT '',
)