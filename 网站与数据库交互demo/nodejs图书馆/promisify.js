"use strict";
module.exports=promisify;
var OPTION={
	resultIndex:undefined,
	errorIndex:undefined,
	context:undefined
};
/** promisify async function
 * @param {function} fn the async function to promisify
 * @param {object} option {
 		resultIndex:Number=resolved with arguments[resultIndex] for the callback function,
 				or undefined(default)=wrap a Array of the arguments,
 		errorIndex:Number=reject if callback's arguments[errorIndex]
 		context:the 'this' for the async function (fn)
	}
 * @return {function} a function called with arguments just like fn
 		Use Function or promisify.CBPLACEHOLDER as the callback placeholder in the arguments.
 		The placeholder will automatically attached to the end of the arguments without placeholder.
 * @Example
 		1:	yield promisify(fs.read,{errorIndex:0,resultIndex:1})('c:/xxx.txt');
 			//auto attach callback placeholder to end and reject if error
 		2:	yield promisify(setTimeout)(Function,1000,'good');
 		3:	var readFile=promisify(fs.readFile);//auto attach callback placeholder
 			var x=yield readFile('c:/xxx.txt');
 			if(x[0])
 				console.error(x[0]);
 			else
 				console.log(x[1]);//data
 			y=yield readFile('c:/xxx.txt','utf-8');
 			......
 */
function promisify(fn,option)
{
	let opt=option || OPTION;
	return function()
	{
		let args=Array.prototype.slice.apply(arguments);
		let idx=args.indexOf(Function);
		if(idx<0) idx=args.length;
		return new Promise(function(resolve,reject)
		{
			args[idx]=function()
			{
				args[idx]=Function;
				if(null!=opt.errorIndex && arguments[opt.errorIndex])
					reject(arguments[opt.errorIndex]);
				else if(null != opt.resultIndex)
				{
					resolve(arguments[opt.resultIndex]);
				}
				else
					resolve(Array.prototype.slice.apply(arguments));
			};
			fn.apply((opt.context || this),args);
		});
	};
}

promisify.CBPLACEHOLDER=Function;