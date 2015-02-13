
index pr_question_index
{
	source			= pr_question_src
	path			= /var/lib/sphinxsearch/data/pr_idx
	docinfo			= extern
	charset_type		= utf-8
	morphology = stem_enru
}


source pr_question_src
{
	type			= mysql

	sql_host		= localhost
	sql_user		= AdminUser
	sql_pass		= admin
	sql_db			= WEBProject
	sql_port		= 3306	# optional, default is 3306

	sql_query		= SELECT * FROM pr_question
	sql_query_pre = SET NAMES utf8

	sql_attr_uint		= id
	sql_attr_uint		= author_id
	sql_field_string = question_text
	sql_field_string = header
	sql_attr_bigint = rating
	sql_attr_timestamp	= pub_date

	#sql_query_info		= SELECT * FROM documents WHERE id=$id
}

indexer
{
	mem_limit		= 32M
}


searchd
{
	listen			= 9312
	listen			= 9306:mysql41
	log			= /var/log/sphinxsearch/searchd.log
	query_log		= /var/log/sphinxsearch/query.log
	read_timeout		= 5
	max_children		= 30
	pid_file		= /var/run/sphinxsearch/searchd.pid
	max_matches		= 1000
	seamless_rotate		= 1
	preopen_indexes		= 1
	unlink_old		= 1
	workers			= threads # for RT to work
	binlog_path		= /var/lib/sphinxsearch/data
}
