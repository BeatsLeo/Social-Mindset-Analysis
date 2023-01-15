'use strict';
exports.html={
	begin:"<html><body><br><div id='result' style='display:none'>",
	end:'<br></body></html>'
};

exports.StrTime=function(D,fmt)
{//Date转换为字串表达(D=Date或Date的字串,fmt=格式，目前只支持"yyyy,mm,dd,hh,nn,ss"几个符号)
	if(String==D.constructor || Number==D.constructor)
		D=new Date(D);
	var d=(100000000+10000*D.getFullYear()+100*(D.getMonth()+1)+D.getDate()).toString();
	var t=(1000000+10000*D.getHours()+100*D.getMinutes()+D.getSeconds()).toString();
	return fmt.replace("yyyy",d.substr(1,4)).replace("mm",d.substr(5,2)).replace("dd",d.substr(7,2)).replace(
		"hh",t.substr(1,2)).replace("nn",t.substr(3,2)).replace("ss",t.substr(5,2)).replace("yy",d.substr(3,2));
};

//+---------------------------------------------------  
//| 求两个时间的天数差 日期格式为 YYYY-MM-dd   
//+---------------------------------------------------  
exports.BetweenTime=function(DateOne,DateTwo)  
{   
   var OneMonth = DateOne.substring(5,DateOne.lastIndexOf ('-'));  
   var OneDay = DateOne.substring(DateOne.length,DateOne.lastIndexOf ('-')+1);  
   var OneYear = DateOne.substring(0,DateOne.indexOf ('-'));  
 
   var TwoMonth = DateTwo.substring(5,DateTwo.lastIndexOf ('-'));  
   var TwoDay = DateTwo.substring(DateTwo.length,DateTwo.lastIndexOf ('-')+1);  
   var TwoYear = DateTwo.substring(0,DateTwo.indexOf ('-'));  
 
   var cha=((Date.parse(OneMonth+'/'+OneDay+'/'+OneYear)- Date.parse(TwoMonth+'/'+TwoDay+'/'+TwoYear))/86400000);   
   return Math.abs(cha);  
}  

//日期加上天数得到新的日期
//dateTemp 需要参加计算的日期，days要添加的天数，返回新的日期，日期格式：YYYY-MM-DD
exports.AddDate=function(dateTemp, days) {
    var dateTemp = dateTemp.split("-");
    var nDate = new Date(dateTemp[1] + '-' + dateTemp[2] + '-' + dateTemp[0]); //转换为MM-DD-YYYY格式  
    var millSeconds = Math.abs(nDate) + (days * 24 * 60 * 60 * 1000);
    var rDate = new Date(millSeconds);
    var year = rDate.getFullYear();
    var month = rDate.getMonth() + 1;
    if (month < 10) month = "0" + month;
    var date = rDate.getDate();
    if (date < 10) date = "0" + date;
    return (year + "-" + month + "-" + date);
}
