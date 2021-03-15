CREATE TABLE `hdf_hos_msg` (
	`hos_name` VARCHAR(200) NOT NULL COMMENT '医院名称',
	`djlx` VARCHAR(100) NOT NULL COMMENT '医院等级类型',
	`jj` text NOT NULL COMMENT '医院简介',
	`dz` VARCHAR(255) NOT NULL COMMENT '医院地址',
	`dh` VARCHAR(255) NOT NULL COMMENT '医院电话',
	`lx` VARCHAR(255) NOT NULL COMMENT '医院电话'
)
COMMENT='好大夫医院信息数据'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `hdf_ks_link` (
	`hos_name` VARCHAR(200) NOT NULL COMMENT '医院名称',
	`ks_name` VARCHAR(100) NOT NULL COMMENT '科室名称',
	`ks_url` VARCHAR(255) NOT NULL COMMENT '科室链接',
	`docker_cnt` VARCHAR(100) NOT NULL COMMENT '科室人数',
	`zt` VARCHAR(100) NOT NULL COMMENT '状态'
)
COMMENT='好大夫医院信息数据'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `hdf_ks_jj` (
	`hos_name` VARCHAR(200) NOT NULL COMMENT '医院名称',
	`ks_name` VARCHAR(100) NOT NULL COMMENT '科室名称',
	`ks_jj` text NOT NULL COMMENT '科室简介'
)
COMMENT='好大夫科室简介'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `hdf_doc_link` (
	`hos_name` VARCHAR(200) NOT NULL COMMENT '医院名称',
	`ks_name` VARCHAR(100) NOT NULL COMMENT '科室名称',
	`doc_name` VARCHAR(100) NOT NULL COMMENT '医师名称',
	`doc_url` VARCHAR(255) NOT NULL COMMENT '医师链接',
	`doc_zc` VARCHAR(255) NOT NULL COMMENT '医师职称',
	`doc_jzdz` VARCHAR(255) NOT NULL COMMENT '就诊地址',
	`zt` VARCHAR(100) NOT NULL COMMENT '状态'
)
COMMENT='好大夫医师链接数据'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `hdf_doc_msg` (
	`hos_name` VARCHAR(200) NOT NULL COMMENT '医院名称',
	`ks_name` VARCHAR(100) NOT NULL COMMENT '科室名称',
	`doc_name` VARCHAR(100) NOT NULL COMMENT '医师姓名',
	`doc_ks` VARCHAR(100) NOT NULL COMMENT '医师科室',
	`doc_zc` VARCHAR(100) NOT NULL COMMENT '医师职称',
	`doc_sc` VARCHAR(255) NOT NULL COMMENT '医师擅长',
	`doc_zjjl` text NOT NULL COMMENT '医师执业经历',
	`doc_zpj` VARCHAR(100) NOT NULL COMMENT '医生总评价',
	`doc_tp` VARCHAR(255) NOT NULL COMMENT '患者投票',
	`gxx` VARCHAR(100) NOT NULL COMMENT '感谢信',
	`lw` VARCHAR(100) NOT NULL COMMENT '礼物'
)
COMMENT='好大夫医师信息数据'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `hdf_hzpl_msg` (
	`hos_name` VARCHAR(200) NOT NULL COMMENT '医院名称',
	`ks_name` VARCHAR(100) NOT NULL COMMENT '科室名称',
	`doc_name` VARCHAR(100) NOT NULL COMMENT '医师姓名',
	`hz_name` VARCHAR(100) NOT NULL COMMENT '患者名字',
	`hz_shjb` VARCHAR(100) NOT NULL COMMENT '所患疾病',
	`hz_kbmd` VARCHAR(100) NOT NULL COMMENT '看病目的',
	`hz_zlfs` VARCHAR(100) NOT NULL COMMENT '治疗方式',
	`hz_zglx` VARCHAR(100) NOT NULL COMMENT '患者主观疗效',
	`hz_pl` text NOT NULL COMMENT '患者评论'
)
COMMENT='好大夫患者评论数据'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


update hdf_doc_link r
join(
select hos_name
       ,ks_name
       ,doc_name
       ,max(doc_ks) as doc_ks
       ,max(doc_zc) as doc_zc
from hdf_doc_msg
group by hos_name,ks_name,doc_name) p
on r.hos_name=p.hos_name and r.ks_name=p.ks_name and r.doc_name=p.doc_name
set r.zt=''
where p.doc_ks='' and p.doc_zc=''
;