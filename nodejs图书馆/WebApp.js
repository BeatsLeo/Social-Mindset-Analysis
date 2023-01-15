"use strict";
const assert=require('assert');
if(!require('http').ServerResponse.send)
{
	require('http').ServerResponse.prototype.send=function(data)
	{
		if(!data) data='';
		let ct=null;
		if(String==data.constructor)
			ct='text/plain;charset=utf-8';
		else if(Buffer!=data.constructor)
		{
			data=JSON.stringify(data);
			ct='text/json;charset=utf-8';
		}
		if(ct && !this.getHeader('Content-Type'))
			this.setHeader('Content-Type',ct);
		this.end(data);
		this._sent=true;//this.finished is not available immediately after end(), so ... :(
	};
	Date.prototype.stamp=function()
	{
		let d=(this.getFullYear()*10000+(this.getMonth()*100+100)+this.getDate()).toString();
		let t=(10000+this.getHours()*100+this.getMinutes()).toString();
		let s=this.getSeconds()+this.getMilliseconds()/1000;
		return d.substr(0,4)+'-'+d.substr(4,2)+'-'+d.substr(6,2)+' '+t.substr(1,2)+':'+t.substr(3,2)+':'+s.toFixed(3);
	}
}
var co=require('co');
var url=require('url');
var QUE=[];//middle ware queue
var ROUTE={};//router map
var LOG=console;
/** init WebApp's logger
 * @param {*} logger to replace console
 * @returns {app}
 */
function app(logger)
{
	if(logger && console==LOG)
		LOG=logger;
	return app;
}
/** proc unhandler error
 * @param {request} req
 * @param {response} res
 * @param {Error|{}|int|String} err
 * 		Error | JSON to send(statusCode=500) | statusCode(statusMessage=txt) | statusMessage(statusCode=500)
 * @param {String} txt
 * @private
 */
function OnError(req,res,err,txt)
{
	let code=err;
	if(String==err.constructor)
	{
		code=500;
		txt=err;
	}
	else if(Number!=err.constructor)
	{
		txt=JSON.stringify(err);
		if(!txt || '{}'==txt) txt='';
		else txt='\tError:'+txt;
		txt=err.toString()+txt;
		code=500;
	}
	if(200!=code)
	{
		LOG.error(req._path+'\n\t'+txt);
		if(err.stack)
			LOG.error(err.stack);
	}
	if(!res.finished && !res._sent)
	{
		res.statusCode=code;
		res.statusMessage=txt;
		res.end(txt);
		res._sent=true;
	}
}
/**
 * @param {String} path
 * @param {int} step
 * @returns {undefined|Function|GeneratorFunction}
 * @private
 */
function MatchNext(path,step)
{
	for(let i=step;i<QUE.length;i++)
	{
		let mw=QUE[i];
		if(!mw.path || (String==mw.path.constructor && mw.path==path) || (RegExp==mw.path.constructor && mw.path.test(path)))
			return {fn:mw.fn,step:i};
	}
}
app.OnRequest=function(req,res)
{
	var step=0;
	var path=url.parse(req.url).pathname;
	req._path=path;
	var next=function(err)
	{
		let match=MatchNext(path,step);
		if(!match)
		{//no handler error
			if(err) OnError(req,res,err);
			else OnError(req,res,404,'Not found');
			return;
		}
		step=match.step+1;
		if(Function==match.fn.constructor)
		{
			if(err)
				match.fn(err,req,res,next);
			else
				match.fn(req,res,next);
		}
		else if(err)
			co(match.fn(err,req,res,next));
		else
			co(match.fn(req,res,next));
	};
	next();
};
/**
 * @param {String|RegExp|Function|GeneratorFunction} path
 * @param {Function|GeneratorFunction} fn
 */
app.use=function(path,fn)
{
	if(null!=path && (Function==path.constructor || 'GeneratorFunction'===path.constructor.name))
		QUE.push({fn:path});
	else
	{
		assert(null!=path && (String==path.constructor || RegExp==path.constructor),'WebApp.use: @param path must be String or RegExp');
		assert(null!=fn && (Function==fn.constructor || 'GeneratorFunction'===fn.constructor.name),'WebApp.use: @param must be Function or GeneratorFunction');
		QUE.push({path:path,fn:fn});
	}
};
/**
 * @param {String|Array} path
 * @param {String|Array} method '*'|'POST'|'GET'|'HEAD'|'PUT'|'DELETE'|['POST','GET',...]
 * @param {Function|GeneratorFunction} fn
 */
app.route=function(path,method,fn)
{
	assert(fn && (Function==fn.constructor || 'GeneratorFunction'==fn.constructor.name),'WebApp.route: @param fn must be Function or GeneratorFunction');
	if(null!=path && String==path.constructor)
		path=[path];
	if(null!=method && String==method.constructor)
		method=[method.toUpperCase()];
	assert(Array==path.constructor,'WebApp.route: @param path must be String or Array of String (not empty)');
	assert(Array==method.constructor && method.length>0,'WebApp.route: @param method must be String or Array of String (not empty)');
	for(let i=0;i<path.length;i++)
	{
		let p=path[i];
		assert(p && String==p.constructor,'WebApp.route: @param path must be String or Array of String (not empty)');
		let rte=ROUTE[p];
		if(!rte)
		{
			rte={};
			ROUTE[p]=rte;
		}
		for(let j=0;j<method.length;j++)
		{
			let m=method[j];
			assert(m && String==m.constructor,'WebApp.route: @param method must be String or Array of String (not empty)');
			let f=rte['*'];
			if(!f) f=rte[m];
			if(f==fn)
			{
				LOG.warn('Duplicate set route('+m+':'+p+') to same function');
				continue;
			}
			assert(!f,'Duplicate set route('+m+':'+p+') to different function');
			if('*'==m)
			{
				for(let k in rte)
				{
					if('*'==k) continue;
					assert(rte[k]==fn,'route(*:'+p+') overset route('+k+':'+p+') to different function');
					LOG.warn('route(*:'+p+') overset route('+k+':'+p+') to same function');
				}
			}
			rte[m]=fn;
		}
	}
};
/**
 * @param {request} req
 * @param {response} res
 * @param {Function} next
 */
app.router=function(req,res,next)
{
	if(arguments.length>=4)//some error
		return arguments[3](req);//next(err)
	var rte=ROUTE[req._path];
	if(!rte)
		return next();
	var fn=rte['*'];
	if(!fn) fn=rte[req.method];
	if(!fn)
		return next();
	if(Function==fn.constructor)
	{
		try{fn(req,res);}
		catch(e)
		{
			next(e);
		}
	}
	else co(fn(req,res)).then(function(val)
	{
		if(!res.finished && !res._sent)
		{
			if(null!=val)
				res.send(val);
			else
				LOG.error(req._path+' : is pendding...');
		}
	},function(err)
	{
		next(err);
	});
};
module.exports=app;
