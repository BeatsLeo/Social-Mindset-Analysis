/** ver 20220510
 * Created by chenpeng on 10/22/16.
 */
"use strict";
const sqlite3=require("sqlite3");
let db=null;
let LOG=console;
/**
 * @param {{file:String|undefined,mode:int|undefined}} opt :
 * 	file:字串，数据库文件名,也支持":memory:",缺省值":memory:"
 * 	mode:模式，coSqlite3.OPEN_READONLY或coSqlite3.OPEN_READWRITE和coSqlite3.OPEN_CREATE的组合（默认）
 * @param {*} logger to replace console
 * @returns {coSqlite3}
 */
function coSqlite3(opt,logger)
{
	if(!db)
	{
		if(logger)
			LOG=logger;
		if(!opt)
			opt={};
		db=new sqlite3.Database((opt.file || ":memory:"),(opt.mode || (sqlite3.OPEN_READWRITE | sqlite3.OPEN_CREATE)),function(err)
		{
			if(err)
				LOG.error('open database error:'+err.toString());
			else{
				db.exec("PRAGMA foreign_keys=ON;");
				LOG.info('coSqlite3 is ready');
			}
		});
	}
	return coSqlite3;
}
coSqlite3.OPEN_READONLY=sqlite3.OPEN_READONLY;
coSqlite3.OPEN_READWRITE=sqlite3.OPEN_READWRITE;
coSqlite3.OPEN_CREATE=sqlite3.OPEN_CREATE;


/**
 * execute single SQL
 * @param {String|{sql:'...',args:[...]}} sql
 * @param {boolean} silent
 * @return {Promise} resolve(result)
 */
coSqlite3.SingleSQL=function(sql,silent)
{
	if(String==sql.constructor)
		sql={sql:sql,args:[]};
	return new Promise(function(resolve,reject)
	{
		db.all(sql.sql,sql.args,function(err,rows)
		{
			if(err)
			{
				if(!silent)
					LOG.error('SQL Error:'+err.toString()+'\n\t'+sql.sql+'\n\t['+sql.args+']');
				reject(err);
			}
			else resolve(rows);
		});
	});
};


/** excute SQLs (sqls[,args][,autoTrans][,Error])
 * @param {String|[{sql:"...",args:[...]},...]} sqls
 * @param {*,...} other
 * 		[,args:Array=args for one sql][,autoTrans:Boolean=use transaction]
 * @return {Promise} resolve (the last sql result)
 */
coSqlite3.execSQL=function * (sqls,other)
{
	//:smart parse arguments
	var args=[],autoTrans,conn,retError;
	for(let x of arguments)
	{
		if(x===sqls || null==x)
			continue;
		switch(x.constructor)
		{
		case Array:
			args=x;
			break;
		case Boolean:
		case Number:
			autoTrans=x;
			break;
		default:
			if(Error===x) retError=true;
		}
	}
	if(String==sqls.constructor)
		sqls=[{sql:sqls,args:args}];
	//:execute sql
	if(autoTrans)
		yield coSqlite3.SingleSQL('begin;');
	var rows;
	try
	{
		for(let sql of sqls)
			rows=yield coSqlite3.SingleSQL(sql,retError);
	}
	catch(e)
	{
		if(autoTrans)
			yield coSqlite3.SingleSQL('rollback;');
		if(retError) return e;
		throw e;
	}
	if(autoTrans)
		yield coSqlite3.SingleSQL('commit;');
	return rows;
};

/**
 * wrap query row to JSON
 * @param row
 * @return {{}} JSON object
 */
coSqlite3.wrapRowData=function(row)
{
	let obj={};
	for(let k in row)
		obj[k]=row[k];
	return obj;
};

/**
 * wrap UPDATE set clause string and args
 * @param {JSON} body: post data or get data
 * @param {{key:field,...}} map: key is property in body and field is table's field, such as {"ID":"sid","NAME":"xName","TIME":"stamp"}
 * @param {Array} arg: receive args
 * @param {Boolean} withSet: return SQL with ' set ....'
 * @return {String} such as " sid=?,xName=?,stamp=?" or " set sid=?,xName=?,stamp=?"
 */
coSqlite3.wrapSet=function(body,map,arg,withSet)
{
	let s='';
	for(let k in map)
	{
		if(undefined===body[k]) continue;
		s+=','+map[k]+'=?';
		arg.push(body[k]);
	}
	if(s)
		s=(withSet?' set ':' ')+s.substr(1);
	return s;
};

/**
 * wrap SQL where clause string and args
 * @param {JSON} body: post data or get data
 * @param {{key:[field,op],...}} map: such as {"ID":["id","="],"NAME":["xName","like"],"TIME":["stamp","in"],"AGE":["age",">"]}
 * 		op:{=|<>|>|<|>=|<=|like|in|not in}
 * @param {Array} arg: receive where args
 * @param {Boolean} withWhere: return SQL with ' where '
 * @return {String}
 */
coSqlite3.wrapWhere=function(body,map,arg,withWhere)
{
	let s='',op;
	for(let k in map)
	{
		let v=body[k];
		if(undefined===v || (String==v.constructor && !v)) continue;
		let m=map[k];
		op=m[1].toLowerCase();
		s+=' and '+m[0];
		switch(op)
		{
		case 'like':
			arg.push('%'+v+'%');
			s+=' like ?';
			break;
		case 'in':
		case 'not in':
			s+=' '+op+'('+v+')';
			break;
		default:
			arg.push(v);
			s+=' '+op+' ?';
		}
	}
	if(s)
		return (withWhere?' where ':'')+s.substr(5);
	else
		return s;
};

module.exports=coSqlite3;