
-- 医院的基本信息数据
create table hos_model1 as 
select a.hos_name -- 医院名称
       ,diqu -- 地区
	   ,case when djlx='' then '无'
             when djlx like '%,%' then substring_index(djlx,',',1)
			 when djlx like '%级%' then djlx
		 else '无' end as yydj -- 医院等级
	   ,case when djlx='' then '无'
             when djlx like '%,%' then substring_index(djlx,',',-1)
			 when djlx like '%医院%' then djlx
		 else '无' end as yylx -- 医院等级
	   ,djlx -- 等级类型
	   ,jj -- 简介
	   ,dz -- 地址
	   ,dh -- 电话
	   ,lx -- 路线
	   ,ks_cnt -- 科室数
	   ,doc_cnt -- 科室数
  from 
	(
	select hos_name
		   ,diqu
	  from hdf_hos_link
	  )as a
	join (
	select hos_name
		   ,max(djlx) as djlx
		   ,max(jj) as jj 	
		   ,max(dz) as dz
		   ,max(dh) as dh
		   ,max(lx) as lx
	  from hdf_hos_msg
	  group by hos_name
	)as b on a.hos_name=b.hos_name
	join (
	select hos_name
		   ,count(distinct ks_name) as ks_cnt -- 科室数
	  from hdf_ks_link
	  group by hos_name
	)as c on a.hos_name=c.hos_name
	join (
	select hos_name
		   ,count(distinct doc_name) as doc_cnt -- 医师数
	  from hdf_doc_link
	  group by hos_name
	)as d on a.hos_name=d.hos_name


--------医院配置指数
with tmp as(
select hos_name
	   ,case when yydj like '%三级%' then 'a'
			 when yydj like '%二级%' then 'b'
			 when yydj like '%一级%' then 'c'
		  else 'd' end as dj_label
	   ,case when yydj='三级甲等' then 450
	         when yydj='三级' then 350
			 when yydj='二级甲等' then 300
			 when yydj='二级' then 200
			 when yydj='一级甲等' then 150
			 when yydj='一级' then 50
		  else 0 end as socre1
       ,ks_cnt
	   ,doc_cnt
  from hos_model1
  )


select hos_name
       ,cast(score1 as signed) as score1
  from(
	select hos_name
		   ,case when a.dj_label='d' then 1*ks_cnt+doc_cnt/10
			 else (socre1+1*(ks_cnt-min_ks_cnt)+1*(doc_cnt-min_doc_cnt)/10) end as score1
	  from tmp as a
	  join (
		select dj_label
			   ,min(ks_cnt) as min_ks_cnt
			   ,min(doc_cnt) as min_doc_cnt
		  from tmp
		  group by dj_label
	  ) as b on a.dj_label=b.dj_label
  )as a
  


--------疗效
with tmp as (
select hos_name
       ,doc_name
	   ,hz_name
	   ,hz_zglx
	   ,substring_index(substring_index(hz_zglx,'\n',1),'患者主观疗效：',-1) as lxpj -- 疗效评价
	   ,substring_index(substring_index(hz_zglx,'\n',-1),'态度：',-1) as tdpj -- 态度评价
  from 	hdf_hzpl_msg
  where hz_zglx!=''
  group by hos_name,doc_name,hz_name,hz_zglx
  )


select hos_name
	   ,sum(case when lxpj='满意' then 0.5
                 when lxpj='很满意' or lxpj='非常满意' then 1
				 when lxpj='不满意' then -10
			 else 0 end
				 ) as score4
  from tmp
  where lxpj not like '%态度%'
  group by hos_name



---------态度
with tmp as (
select hos_name
       ,doc_name
	   ,hz_name
	   ,hz_zglx
	   ,substring_index(substring_index(hz_zglx,'\n',1),'患者主观疗效：',-1) as lxpj -- 疗效评价
	   ,substring_index(substring_index(hz_zglx,'\n',-1),'态度：',-1) as tdpj -- 态度评价
  from 	hdf_hzpl_msg
  where hz_zglx!=''
  group by hos_name,doc_name,hz_name,hz_zglx
  )

select hos_name
	   ,sum(case when tdpj='满意' then 0.5
                 when tdpj='很满意' or tdpj='非常满意' then 1
				 when tdpj='不满意' then -10
			 else 0 end
				 ) as score4
  from tmp
  where tdpj not like '%服务%'
  group by hos_name



--------------- 数据表
CREATE TABLE `hos_model_5data` (
	`hos_name` VARCHAR(200) NOT NULL COMMENT '医院名称',
	`amt` float(2) NOT NULL COMMENT '总花费',
	`jj_amt` float(2) NOT NULL COMMENT '基金报销金额',
	`bili` float(6) NOT NULL COMMENT '报销比例',
	`user_cnt` int(11) NOT NULL COMMENT '用户数'
)
COMMENT='好大夫模型数据'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `hos_model_4` (
	`hos_name` VARCHAR(200) NOT NULL COMMENT '医院名称',
	`score` float(2) NOT NULL COMMENT '分数'
)
COMMENT='好大夫模型数据'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `hos_index` (
	`hos_name` VARCHAR(200) NOT NULL COMMENT '医院名称',
	`index` int(11) NOT NULL COMMENT '关联键'
)
COMMENT='医院关联键'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;





----------------  特色科室
with a as (
select hos_name
       ,ks_name
	   ,cast(substring_index(substring_index(substring_index(docker_cnt,',',1),'(',-1),'人',1) as signed) as doctor_cnt -- 医师数 
	   ,cast(substring_index(substring_index(substring_index(docker_cnt,',',-1),')',1),'票',1) as signed) as pl_cnt -- 评论数
	   ,docker_cnt as docker_cnt2
  from hdf_ks_link
  where ks_name not in ('内科','外科','妇产科','儿科','肿瘤科','神经科','眼科','口腔科','耳鼻喉科')
  group by hos_name,ks_name,docker_cnt
)


select hos_name
	   ,ks_name
	   ,num
  from( 
	select hos_name
		   ,ks_name
		   ,if(@hos_name=c.hos_name,@num:=@num+1,@num:=1) as num
		   ,(@hos_name:=c.hos_name) as hos_name_1
	  from
		(
		select hos_name
			   ,ks_name
			   ,sum(num) as num
		  from(
		  select * from (
			select hos_name
				   ,ks_name
				   ,doctor_cnt
				   ,pl_cnt
				   ,if(@hos_name=a.hos_name,@num:=@num+1,@num:=1) as num
				   ,(@hos_name:=a.hos_name) as hos_name_1
			  from a,(select @num:=0,@hos_name:='')b
			  order by hos_name,doctor_cnt  desc)as h1
			union all
		  select * from (
			select hos_name
				   ,ks_name
				   ,doctor_cnt
				   ,pl_cnt
				   ,if(@hos_name=a.hos_name,@num:=@num+1,@num:=1) as num
				   ,(@hos_name:=a.hos_name) as hos_name_1
			  from a,(select @num:=0,@hos_name:='')b
			  order by hos_name,pl_cnt desc)as h2
		  )as c
		  group by hos_name,ks_name
		  )as c,(select @num:=0,@hos_name:='')d
	  order by hos_name,num
  )as g
  where g.num<=3