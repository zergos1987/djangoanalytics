--task_history
--view_log
CREATE OR REPLACE FUNCTION clear_table_by_limit_view_log() RETURNS TRIGGER AS $clear_table_by_limit_view_log$
DECLARE 
	cnt integer;
BEGIN
	cnt := COUNT(*) FROM metabase.public.view_log;
	IF cnt > 50000
		THEN DELETE FROM metabase.public.view_log;
	END IF;
	RETURN null;
END;
$clear_table_by_limit_view_log$ LANGUAGE plpgsql;

CREATE TRIGGER clear_table_by_limit_view_log BEFORE INSERT
ON metabase.public.view_log FOR EACH STATEMENT
EXECUTE PROCEDURE clear_table_by_limit_view_log();
