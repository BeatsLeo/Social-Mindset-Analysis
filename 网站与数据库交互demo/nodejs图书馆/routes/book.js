'use strict';
const HTM=require('../lib').html;
const db=require("../coSqlite3");
const StrTime=require('../lib').StrTime;
const BetweenTime=require('../lib').BetweenTime;
const AddDate=require('../lib').AddDate;

//数据库初始化
exports.Init=function*(req,res)
{
	try {
		yield db.execSQL("CREATE TABLE b (bID VARCHAR(30) PRIMARY KEY, bName VARCHAR(30), bPub VARCHAR(30), bDate DATE,bAuthor VARCHAR(20), bMem VARCHAR(30), bCnt INTEGER)");
		yield db.execSQL("CREATE TABLE r (rID VARCHAR(8) PRIMARY KEY, rName VARCHAR(10), rSex VARCHAR(1), rDept VARCHAR(10), rGrade INTEGER)");
		yield db.execSQL("CREATE TABLE bb (rID VARCHAR(8), bID VARCHAR(30), bbDate DATE)");
	    return HTM.begin+'0'+'</div>'+'<br>'+'成功'+HTM.end;
	} catch (error) {
		return HTM.begin+'1'+'</div>'+'<br>'+error.message+HTM.end;
	}
};

//添加新书
exports.CreateBook=function*(req,res)
{
	let body=req.body;
	if(!body.bID)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：书号没有填写'+HTM.end;
	if(body.bID.length>30)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：填写的内容不符合格式要求，书号长度不能超过30字'+HTM.end;
	if(!body.bName)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：书名没有填写'+HTM.end;
	if(body.bName.length>30)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：填写的内容不符合格式要求，书名长度不能超过30字'+HTM.end;
	if(body.bPub.length>30)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：填写的内容不符合格式要求，出版社长度不能超过30字'+HTM.end;
    var testime = body.bDate.match(/^(\d{4})-(\d{2})-(\d{2})$/);
	if (testime == null&&body.bDate) {
			return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：填写的内容不符合格式要求，出版日期格式不正确'+HTM.end;
	}
	if(body.bAuthor.length>20)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：填写的内容不符合格式要求，作者长度不能超过20字'+HTM.end;
	if(body.bMem.length>30)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：填写的内容不符合格式要求，内容摘要长度不能超过30字'+HTM.end;
	if(!body.bCnt)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：填写的内容不符合格式要求，书籍数量不能为空'+HTM.end;
	if(body.bCnt<=0)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：填写的内容不符合格式要求，新书数量应大于0'+HTM.end;
	if(!(/(^[1-9]\d*$)/.test(body.bCnt)))
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：填写的内容不符合格式要求，数量不是填写的整数'+HTM.end;

	try {
		let flag=yield db.execSQL("SELECT 1 FROM b WHERE bID='"+body.bID+"' LIMIT 1")
		//console.log(flag.length)
	    if (flag.length!=0)
		    return HTM.begin+'1'+'</div>'+'<br>'+'该书已经存在'+HTM.end;
		yield db.execSQL("INSERT INTO b(bID, bName, bPub, bDate, bAuthor, bMem, bCnt) VALUES(?,?,?,?,?,?,?)",[body.bID,body.bName,body.bPub,body.bDate,body.bAuthor,body.bMem,body.bCnt]);
	    return HTM.begin+'0'+'</div>'+'<br>'+'成功'+HTM.end;
	} catch (error) {	
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误:'+error.message+HTM.end;
	}
};

//增加书籍数量
exports.AddBookCnt=function*(req,res)
{
	let body=req.body;
	if(!body.bID)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：书号没有填写'+HTM.end;
	if(body.bID.length>30)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：书号长度过长'+HTM.end;
	if(!body.bCnt)
	    return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：书增加的数量不能为空'+HTM.end;
	if(body.bCnt<=0)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：书增加的数量应大于0'+HTM.end;
	if(!(/(^[1-9]\d*$)/.test(body.bCnt)))
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：数量不是填写的整数'+HTM.end;

	let flag=yield db.execSQL("SELECT 1 FROM b WHERE bID='"+body.bID+"' LIMIT 1")
	//console.log(flag.length)
	if (flag.length==0)
		return HTM.begin+'1'+'</div>'+'<br>'+'该书不存在'+HTM.end;

	yield db.execSQL("UPDATE b SET bCnt=bCnt+'"+body.bCnt+"' WHERE bID='"+body.bID+"'");
	return HTM.begin+'0'+'</div>'+'<br>'+'成功'+HTM.end;
};

//删除或减少书籍
exports.DecreaseBook=function*(req,res)
{
	let body=req.body;
	if(!body.bID)
		return HTM.begin+'3'+'</div>'+'<br>'+'提交的参数有误：书号没有填写'+HTM.end;
	if(body.bID.length>30)
		return HTM.begin+'3'+'</div>'+'<br>'+'提交的参数有误：书号长度不能超过30字'+HTM.end;
	if(!body.bCnt)
	    return HTM.begin+'3'+'</div>'+'<br>'+'提交的参数有误：数量不能为空'+HTM.end;
	if(body.bCnt<=0)
		return HTM.begin+'3'+'</div>'+'<br>'+'提交的参数有误：数量应大于0'+HTM.end;
	if(!(/(^[1-9]\d*$)/.test(body.bCnt)))
		return HTM.begin+'3'+'</div>'+'<br>'+'提交的参数有误：数量不是填写的整数'+HTM.end;

	let flag=yield db.execSQL("SELECT 1 FROM b WHERE bID='"+body.bID+"' LIMIT 1")
	if (flag.length==0)
	   return HTM.begin+'1'+'</div>'+'<br>'+'该书不存在'+HTM.end;
	
	
	

	let cnt=yield db.execSQL("SELECT bCnt FROM b WHERE bID='"+body.bID+"'");
	let count=yield db.execSQL("SELECT COUNT(*) FROM bb WHERE bID='"+body.bID+"'")
	let rows=yield db.execSQL("SELECT * FROM bb INNER JOIN b ON bb.bID = b.bID")
	for(let row of rows){
			if(body.bCnt>(row.bCnt-count[0]["COUNT(*)"])&&body.bID==row.bID)
				return HTM.begin+'2'+'</div>'+'<br>'+'减少的数量大于该书目前在库数量'+HTM.end;
			if(cnt[0].bCnt<body.bCnt)
                return HTM.begin+'2'+'</div>'+'<br>'+'减少的数量大于该书目前在库数量'+HTM.end;
			if(cnt[0].bCnt==body.bCnt&&count[0]["COUNT(*)"]==0){
		        yield db.execSQL("DELETE FROM b WHERE bID='"+body.bID+"'");
	            return HTM.begin+'0'+'</div>'+'<br>'+'成功'+HTM.end; 		
	}
	
	}
	  
	yield db.execSQL("UPDATE b SET bCnt=bCnt-'"+body.bCnt+"' WHERE bID='"+body.bID+"'");
	return HTM.begin+'0'+'</div>'+'<br>'+'成功'+HTM.end;
};

//修改书籍信息
exports.ReviseBook=function*(req,res)
{
	let body=req.body;
	if(!body.bID)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：书号没有填写'+HTM.end;
	if(body.bID.length>30)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：书号长度不能超过30字'+HTM.end;
	
	if(!body.bName)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：书名没有填写'+HTM.end;
	if(body.bName.length>30)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：书名长度不能超过30字'+HTM.end;
	if(body.bPub.length>30)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：出版社长度不能超过30字'+HTM.end;
    var testime = body.bDate.match(/^(\d{4})-(\d{2})-(\d{2})$/);
	if (testime == null&&body.bDate) {
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：出版日期格式不正确'+HTM.end;
	}
	if(body.bAuthor.length>20)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：作者长度不能超过20字'+HTM.end;
	if(body.bMem.length>30)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：内容摘要长度不能超过30字'+HTM.end;

	let flag=yield db.execSQL("SELECT 1 FROM b WHERE bID='"+body.bID+"' LIMIT 1")
	//console.log(flag.length)
	if (flag.length==0)
		return HTM.begin+'1'+'</div>'+'<br>'+'该书不存在'+HTM.end;

	let rows=yield db.execSQL("SELECT * FROM b WHERE bID='"+body.bID+"'")
	if (!body.bPub)
		body.bPub=rows[0].bPub;
	if (!body.bDate)
		body.bDate=rows[0].bDate;
	if (!body.bAuthor)
		body.bAuthor=rows[0].bAuthor;
	if (!body.bMem)
	    body.bMem=rows[0].bMem;

	try {
		yield db.execSQL("UPDATE b SET bName='"+body.bName+"',bPub='"+body.bPub+"',bDate='"+body.bDate+"',bAuthor='"+body.bAuthor+"',bMem='"+body.bMem+"'  WHERE bID='"+body.bID+"'");
	    return HTM.begin+'0'+'</div>'+'<br>'+'成功'+HTM.end;
	} catch (error) {
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误:'+error.message+HTM.end;
	}
};

//查询书籍
exports.QueryBook=function*(req,res)
{
	let body=req.body;
	let cnd='',sql="SELECT bID,bName,bPub,bDate,bAuthor,bMem,bCnt FROM b";
	let flag=0
	if(body.bID){
		if(flag==0){
			flag=1;
		    cnd+=" WHERE";
		}
		cnd+=" bID like '%"+body.bID.replace(/\x27/g,"''")+"%'";
	}
	if(flag==1&&body.bName)
		cnd+=" AND";
	if(body.bName){
		if(flag==0){
			flag=1;
		    cnd+=" WHERE";
		}
		cnd+=" bName like '%"+body.bName.replace(/\x27/g,"''")+"%'";
	}
	if(flag==1&&body.bPub)
		cnd+=" AND";
	if(body.bPub){
		if(flag==0){
			flag=1;
		    cnd+=" WHERE";
		}
		cnd+=" bPub like '%"+body.bPub.replace(/\x27/g,"''")+"%'";
	}
	var testime = body.bDate0.match(/^(\d{4})-(\d{2})-(\d{2})$/);
	if(testime==null&&body.bDate0){
		return '<html><head><META HTTP-EQUIV="Content-Type" Content="text-html;charset=utf-8"></head><br><body><br><table border=1 id="result"></table><br></body><br></html>'
	}
	if(flag==1&&body.bDate0)
		cnd+=" AND";
	if (body.bDate0){
		if(flag==0){
			flag=1;
		    cnd+=" WHERE";
		}
		cnd+=" bDate>='"+body.bDate0+"'";
	}
	var testime = body.bDate1.match(/^(\d{4})-(\d{2})-(\d{2})$/);
	if(testime==null&&body.bDate1){
		return '<html><head><META HTTP-EQUIV="Content-Type" Content="text-html;charset=utf-8"></head><br><body><br><table border=1 id="result"></table><br></body><br></html>'
	}
	if(flag==1&&body.bDate1)
		cnd+=" AND";
	if (body.bDate1){
		if(flag==0){
			flag=1;
		    cnd+=" WHERE";
		}
		cnd+=" bDate<='"+body.bDate1+"'";
	}
	if(flag==1&&body.bAuthor)
		cnd+=" AND";
	if(body.bAuthor){
		if(flag==0){
			flag=1;
		    cnd+=" WHERE";
		}
		cnd+=" bAuthor like '%"+body.bAuthor.replace(/\x27/g,"''")+"%'";
	}
	if(flag==1&&body.bMem)
		cnd+=" AND";
	if(body.bMem){
		if(flag==0){
			flag=1;
		    cnd+=" WHERE";
		}
		cnd+=" bMem like '%"+body.bMem.replace(/\x27/g,"''")+"%'";
	}
		
	sql+=cnd;

	let htm='<html><head><META HTTP-EQUIV="Content-Type" Content="text-html;charset=utf-8"></head><br><body><br><table border=1 id="result">';
	let rows=yield db.execSQL(sql);
	for(let row of rows){
		htm+='<tr><td>'+row.bID+'</td>'
			+'<td>'+row.bName+'</td>'
			+'<td>'+row.bCnt+'</td>';
		let count=yield db.execSQL("SELECT COUNT(*) FROM bb WHERE bID='"+row.bID+"'")
		console.log(count[0]["COUNT(*)"])
		let nowcnt=row.bCnt-count[0]["COUNT(*)"]
		htm+='<td>'+nowcnt+'</td>';
		htm+='<td>'+row.bPub+'</td>'
			+'<td>'+row.bDate+'</td>'
			+'<td>'+row.bAuthor+'</td>'
			+'<td>'+row.bMem+'</td></tr>';
	}
		
	htm+='</table><br></body><br></html>';
	return htm;
};

//添加读者
exports.CreateReader=function*(req,res)
{
	let body=req.body;
	if(!body.rID)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：证号不能为空'+HTM.end;
	if(body.rID.length>8)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：证号长度不能超过8字'+HTM.end;
	if(body.rName.length>10)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：姓名长度不能超过10字'+HTM.end;
	if(!(body.rSex=="男"||body.rSex=="女"||!body.rSex))
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：性别应为“男”或“女”'+HTM.end;
	if(body.rDept.length>10)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：系名长度不能超过10字'+HTM.end;
	if(!(/(^[1-9]\d*$)/.test(body.rGrade)||!body.rGrade))
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：年级应为正整数'+HTM.end;

	try {
		let flag=yield db.execSQL("SELECT 1 FROM r WHERE rID='"+body.rID+"' LIMIT 1")
		console.log(flag.length)
	    if (flag.length!=0)
		    return HTM.begin+'1'+'</div>'+'<br>'+'该证号已经存在'+HTM.end;
		yield db.execSQL("INSERT INTO r(rID, rName, rSex, rDept, rGrade) VALUES(?,?,?,?,?)",[body.rID,body.rName,body.rSex,body.rDept,body.rGrade]);
	    return HTM.begin+'0'+'</div>'+'<br>'+'成功'+HTM.end;
	} catch (error) {	
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误:'+error.message+HTM.end;
	}
};

//删除读者
exports.DeleteReader=function*(req,res)
{
	let body=req.body;
	if(!body.rID)
		return HTM.begin+'1'+'</div>'+'<br>'+'该证号不存在'+HTM.end;

	let flag=yield db.execSQL("SELECT 1 FROM r WHERE rID='"+body.rID+"' LIMIT 1")
	if (flag.length==0)
	   return HTM.begin+'1'+'</div>'+'<br>'+'该证号不存在'+HTM.end;
	
	flag=yield db.execSQL("SELECT 1 FROM bb WHERE rID='"+body.rID+"' LIMIT 1")
	if (flag.length!=0)
		return HTM.begin+'2'+'</div>'+'<br>'+'该读者尚有书籍未归还'+HTM.end;
	
	yield db.execSQL("DELETE FROM r WHERE rID='"+body.rID+"'");
	return HTM.begin+'0'+'</div>'+'<br>'+'成功'+HTM.end;
};

//修改读者信息
exports.ReviseReader=function*(req,res)
{
	let body=req.body;
	if(!body.rID)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：证号没有填写'+HTM.end;
	if(body.rID.length>8)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：证号长度不能超过8字'+HTM.end;
	if(body.rName.length>10)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：姓名长度不能超过10字'+HTM.end;
	if(!(body.rSex=="男"||body.rSex=="女"||!body.rSex))
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：性别应为“男”或“女”'+HTM.end;
	if(body.rDept.length>10)
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：系名长度不能超过10字'+HTM.end;
	if(!(/(^[1-9]\d*$)/.test(body.rGrade)||!body.rGrade))
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误：年级应为正整数'+HTM.end;

	let flag=yield db.execSQL("SELECT 1 FROM r WHERE rID='"+body.rID+"' LIMIT 1")
	//console.log(flag.length)
	if (flag.length==0)
		return HTM.begin+'1'+'</div>'+'<br>'+'该证号不存在'+HTM.end;

	let rows=yield db.execSQL("SELECT * FROM r WHERE rID='"+body.rID+"'")
	if (!body.rName)
		body.rName=rows[0].rName;
	if (!body.rSex)
		body.rSex=rows[0].rSex;
	if (!body.rDept)
		body.rDept=rows[0].rDept;
	if (!body.rGrade)
	    body.rGrade=rows[0].rGrade;

	try {
		yield db.execSQL("UPDATE r SET rName='"+body.rName+"',rSex='"+body.rSex+"',rDept='"+body.rDept+"',rGrade='"+body.rGrade+"' WHERE rID='"+body.rID+"'");
	    return HTM.begin+'0'+'</div>'+'<br>'+'成功'+HTM.end;
	} catch (error) {
		return HTM.begin+'2'+'</div>'+'<br>'+'提交的参数有误:'+error.message+HTM.end;
	}
};

//查询读者
exports.QueryReader=function*(req,res)
{
	let body=req.body;
	let cnd='',sql="SELECT rID, rName, rSex, rDept, rGrade FROM r";
	let flag=0
	if(body.rID.length>8)
	    return '<html><head><META HTTP-EQUIV="Content-Type" Content="text-html;charset=utf-8"></head><br><body><br><table border=1 id="result"></table><br></body><br></html>'
	if(body.rName.length>10)
	    return '<html><head><META HTTP-EQUIV="Content-Type" Content="text-html;charset=utf-8"></head><br><body><br><table border=1 id="result"></table><br></body><br></html>'
	if(!(body.rSex=="男"||body.rSex=="女"||!body.rSex))
	    return '<html><head><META HTTP-EQUIV="Content-Type" Content="text-html;charset=utf-8"></head><br><body><br><table border=1 id="result"></table><br></body><br></html>'
	if(body.rDept.length>10)
	    return '<html><head><META HTTP-EQUIV="Content-Type" Content="text-html;charset=utf-8"></head><br><body><br><table border=1 id="result"></table><br></body><br></html>'
	if(!(/(^[1-9]\d*$)/.test(body.rGrade0)||!body.rGrade0))
		return '<html><head><META HTTP-EQUIV="Content-Type" Content="text-html;charset=utf-8"></head><br><body><br><table border=1 id="result"></table><br></body><br></html>'
	if(!(/(^[1-9]\d*$)/.test(body.rGrade1)||!body.rGrade1))
	    return '<html><head><META HTTP-EQUIV="Content-Type" Content="text-html;charset=utf-8"></head><br><body><br><table border=1 id="result"></table><br></body><br></html>'
	if(body.rID){
		if(flag==0){
			flag=1;
		    cnd+=" WHERE";
		}
		cnd+=" rID like '%"+body.rID.replace(/\x27/g,"''")+"%'";
	}
	if(body.rName){
		if(flag==1)
			cnd+=" AND";
		if(flag==0){
			flag=1;
		    cnd+=" WHERE";
		}
		cnd+=" rName like '%"+body.rName.replace(/\x27/g,"''")+"%'";
	}
	if(body.rSex=='男'&&body.rSex){
		if(flag==1)
			cnd+=" AND";
		if(flag==0){
			flag=1;
		    cnd+=" WHERE";
		}	
		cnd+=" rSex=='男'";
	}
	if(body.rSex=='女'&&body.rSex){		
		if(flag==1)
			cnd+=" AND";
		if(flag==0){
			flag=1;
		    cnd+=" WHERE";
		}
		cnd+=" rSex=='女'";
	}
	if(body.rDept){		
		if(flag==1)
			cnd+=" AND";
		if(flag==0){
			flag=1;
		    cnd+=" WHERE";
		}
		cnd+=" rDept like '%"+body.rDept.replace(/\x27/g,"''")+"%'";
	}
	if(body.rGrade0){
		if(flag==1)
			cnd+=" AND";
		if(flag==0){
			flag=1;
		    cnd+=" WHERE";
		}
		cnd+=" rGrade>='"+body.rGrade0+"'";
	}
	if(body.rGrade1){
		if(flag==1)
			cnd+=" AND";
		if(flag==0){
			flag=1;
		    cnd+=" WHERE";
		}
		cnd+=" rGrade<='"+body.rGrade1+"'";
	}
	sql+=cnd;
	console.log(sql)

	let htm='<html><head><META HTTP-EQUIV="Content-Type" Content="text-html;charset=utf-8"></head><br><body><br><table border=1 id="result">';
	let rows=yield db.execSQL(sql);
	for(let row of rows)
		htm+='<tr><td>'+row.rID+'</td>'
			+'<td>'+row.rName+'</td>'
			+'<td>'+row.rSex+'</td>'
			+'<td>'+row.rDept+'</td>'
			+'<td>'+row.rGrade+'</td></tr>';
	htm+='</table><br></body><br></html>';
	return htm;
};

//查看某个读者还未还书籍信息
exports.UnReturnList=function*(req,res)
{
	let body=req.body;
	if(!body.rID)
		return HTM.begin+'1'+'</div>'+'<br>'+'该证号不存在'+HTM.end;
	let flag=yield db.execSQL("SELECT 1 FROM r WHERE rID='"+body.rID+"' LIMIT 1")
	if (flag.length==0)
		return HTM.begin+'1'+'</div>'+'<br>'+'该证号不存在'+HTM.end;
	
	var myDate = new Date();
	var mytime=myDate.toLocaleDateString();     //获取当前时间
	mytime=StrTime(mytime,'yyyy-mm-dd')

	let htm='<html><head><META HTTP-EQUIV="Content-Type" Content="text-html;charset=utf-8"></head><br><body><br><table border=1 id="result">';
	let rows=yield db.execSQL("SELECT * FROM bb INNER JOIN b ON bb.bID = b.bID WHERE rID='"+body.rID+"'")
	for(let row of rows){
		var days=BetweenTime(mytime,row.bbDate);
		console.log(row.bCnt)
		htm+='<tr><td>'+row.bID+'</td>'
			+'<td>'+row.bName+'</td>'
			+'<td>'+row.bbDate+'</td>';
		let newday=AddDate(row.bbDate,30);
		htm+='<td>'+newday+'</td>';
		if(days>30)
			htm+='<td>'+'是'+'</td></tr>';
		else
		    htm+='<td>'+'否'+'</td></tr>';
	}
		
	htm+='</table><br></body><br></html>';
	return htm;
};

//借书
exports.BorrowBook=function*(req,res)
{
	let body=req.body;
	if(!body.rID)
		return HTM.begin+'1'+'</div>'+'<br>'+'该证号不存在'+HTM.end;
	let flag=yield db.execSQL("SELECT 1 FROM r WHERE rID='"+body.rID+"' LIMIT 1")
	if (flag.length==0)
		return HTM.begin+'1'+'</div>'+'<br>'+'该证号不存在'+HTM.end;

	if(!body.bID)
		return HTM.begin+'2'+'</div>'+'<br>'+'该书号不存在'+HTM.end;
	flag=yield db.execSQL("SELECT 1 FROM b WHERE bID='"+body.bID+"' LIMIT 1")
		if (flag.length==0)
			return HTM.begin+'2'+'</div>'+'<br>'+'该书号不存在'+HTM.end;
	
	var myDate = new Date();
	var mytime=myDate.toLocaleDateString();     //获取当前时间
	mytime=StrTime(mytime,'yyyy-mm-dd')

	let count=yield db.execSQL("SELECT COUNT(*) FROM bb WHERE bID='"+body.bID+"'")
	let rows=yield db.execSQL("SELECT * FROM bb INNER JOIN b ON bb.bID = b.bID")
	for(let row of rows){
			var days=BetweenTime(mytime,row.bbDate);
			if(row.rID==body.rID){
				if(days>30)
			        return HTM.begin+'3'+'</div>'+'<br>'+'该读者有超期书未还'+HTM.end;
		        if(row.bID==body.bID)
				    return HTM.begin+'4'+'</div>'+'<br>'+'该读者已经借阅该书，且未归还'+HTM.end;
			}
			if(count[0]["COUNT(*)"]>=row.bCnt&&body.bID==row.bID)
		        return HTM.begin+'5'+'</div>'+'<br>'+'该书已经全部借出'+HTM.end; 		
	}
	try {
			yield db.execSQL("INSERT INTO bb(rID, bID, bbDate) VALUES(?,?,?)",[body.rID,body.bID,mytime]);
	        return HTM.begin+'0'+'</div>'+'<br>'+'成功'+HTM.end;
		} catch (error) {
			return HTM.begin+'6'+'</div>'+'<br>'+error.message+HTM.end;	
		}
};

//还书
exports.ReturnBook=function*(req,res)
{
	let body=req.body;
	if(!body.rID)
		return HTM.begin+'1'+'</div>'+'<br>'+'该证号不存在'+HTM.end;
	let flag=yield db.execSQL("SELECT 1 FROM r WHERE rID='"+body.rID+"' LIMIT 1")
	if (flag.length==0)
		return HTM.begin+'1'+'</div>'+'<br>'+'该证号不存在'+HTM.end;

	if(!body.bID)
		return HTM.begin+'2'+'</div>'+'<br>'+'该书号不存在'+HTM.end;
	flag=yield db.execSQL("SELECT 1 FROM b WHERE bID='"+body.bID+"' LIMIT 1")
	if (flag.length==0)
		return HTM.begin+'2'+'</div>'+'<br>'+'该书号不存在'+HTM.end;
	
	let rows=yield db.execSQL("SELECT * FROM bb INNER JOIN b ON bb.bID = b.bID WHERE rID='"+body.rID+"'")

	for(let row of rows){
			if(row.bID==body.bID){
				yield db.execSQL("DELETE FROM bb WHERE rID='"+body.rID+"' AND bID='"+body.bID+"'"  );
	            return HTM.begin+'0'+'</div>'+'<br>'+'成功'+HTM.end;
			}	
	}			
	return HTM.begin+'3'+'</div>'+'<br>'+'该读者并未借阅该书'+HTM.end;
};

//超期读者列表
exports.OvertimeList=function*(req,res)
{
	var myDate = new Date();
	var mytime=myDate.toLocaleDateString();     //获取当前时间
	mytime=StrTime(mytime,'yyyy-mm-dd')

	let htm='<html><head><META HTTP-EQUIV="Content-Type" Content="text-html;charset=utf-8"></head><br><body><br><table border=1 id="result">';
	let rows=yield db.execSQL("SELECT * FROM r INNER JOIN bb ON bb.rID = r.rID");
	for(let row of rows){
		var days=BetweenTime(mytime,row.bbDate);
	    console.log(row)
		console.log(days)
		if(days>30)
			htm+='<tr><td>'+row.rID+'</td>'
			+'<td>'+row.rName+'</td>'
			+'<td>'+row.rSex+'</td>'
			+'<td>'+row.rDept+'</td>'
			+'<td>'+row.rGrade+'</td></tr>';
	}	
	htm+='</table><br></body><br></html>';
	return htm;
};