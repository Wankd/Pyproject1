drop table tmp_hos_model_score1;
create table tmp_hos_model_score1 as 
select hos_name
       ,pm as pm1
		   ,case when pm-1<100 then 100-(pm-1)*0.5
			 else 100*(1-0.5)-(pm-100)*0.2 end score1
	  from(
		select hos_name
			   ,score1
			   ,case when @score=score1 then @num
					 when @score:=score1 then @num:=@num+1
				 end as pm
		  from tmp_hos_model_1 p,
		  (select @num:=0,@score:=NULL) t
		  order by score1 desc
	  )as a
;


drop table tmp_hos_model_score21;
create table tmp_hos_model_score21 as 
with tmp as (
select hos_name
			   ,score4
			   ,case when @score=score4 then @num
					 when @score:=score4 then @num:=@num+1
				 end as pm
		  from tmp_hos_model_2_1 p,
		  (select @num:=0,@score:=NULL) t
		  order by score4 desc
)

select hos_name
       ,pm as pm21
		   ,case when pm-1<100 then 200-(pm-1)*1
			 else 200*(1-0.5)-(pm-100)*0.4 end score21
	  from(
		select a.hos_name
		       ,a.score4
			   ,coalesce(a.pm,b.pm) as pm
		  from tmp a
		  join (
		  select score4
		         ,pm
			from tmp
			where pm is not null
			group by score4,pm
		  )b on a.score4=b.score4
	  )as a
;

drop table tmp_hos_model_score22;
create table tmp_hos_model_score22 as 
with tmp as (
select hos_name
			   ,score4
			   ,case when @score=score4 then @num
					 when @score:=score4 then @num:=@num+1
				 end as pm
		  from tmp_hos_model_2_2 p,
		  (select @num:=0,@score:=NULL) t
		  order by score4 desc
)

select hos_name
       ,pm as pm22
		   ,case when pm-1<100 then 100-(pm-1)*0.5
			 else 100*(1-0.5)-(pm-100)*0.2 end score22
	  from(
		select a.hos_name
		       ,a.score4
			   ,coalesce(a.pm,b.pm) as pm
		  from tmp a
		  join (
		  select score4
		         ,pm
			from tmp
			where pm is not null
			group by score4,pm
		  )b on a.score4=b.score4
	  )as a
;


;

drop table tmp_hos_model_score4;
create table tmp_hos_model_score4 as 
with tmp as (
select hos_name
			   ,score4
			   ,case when @score=score4 then @num
					 when @score:=score4 then @num:=@num+1
				 end as pm
		  from tmp_hos_model_4 p,
		  (select @num:=0,@score:=NULL) t
		  order by score4 desc
)

select hos_name
       ,pm as pm4
		   ,case when pm-1<100 then 200-(pm-1)*1
			 else 200*(1-0.5)-(pm-100)*0.4 end score4
	  from(
		select a.hos_name
		       ,a.score4
			   ,coalesce(a.pm,b.pm) as pm
		  from tmp a
		  join (
		  select score4
		         ,pm
			from tmp
			where pm is not null
			group by score4,pm
		  )b on a.score4=b.score4
	  )as a


;
-- drop table tmp_hos_model_score;
create table tmp_hos_model_score as 
select a.hos_name
       ,score
	   ,pm1
	   ,score1
	   ,pm21
	   ,score21
	   ,pm22
	   ,score22
	   ,pm4
	   ,score4
  from
(
select hos_name
       ,sum(score) as score
  from(
	-- ----------- 医院配置得分
	select hos_name,score1 as score from tmp_hos_model_score1
	union all
	-- ---------- 疗效评分
	select hos_name,score21 as score from tmp_hos_model_score21
	union all
	-- ---------- 态度评分
	select hos_name,score22 as score from tmp_hos_model_score22
	union all
	-- ---------- 科研评分
	select hos_name,score4 as score from tmp_hos_model_score4
  )as a
  group by hos_name
  )as a
  left join tmp_hos_model_score1 as b on a.hos_name=b.hos_name
  left join tmp_hos_model_score21 as c on a.hos_name=c.hos_name
  left join tmp_hos_model_score22 as d on a.hos_name=d.hos_name
  left join tmp_hos_model_score4 as e on a.hos_name=e.hos_name