'use strict';
const book=require('./book');
const app=require('../WebApp');

app.route('/init','post',book.Init);
app.route('/createbook','post',book.CreateBook);
app.route('/addbookcnt','post',book.AddBookCnt);
app.route('/decreasebook','post',book.DecreaseBook);
app.route('/revisebook','post',book.ReviseBook);
app.route('/querybook','post',book.QueryBook);
app.route('/borrowbook','post',book.BorrowBook);
app.route('/returnbook','post',book.ReturnBook);

app.route('/createreader','post',book.CreateReader);
app.route('/deletereader','post',book.DeleteReader);
app.route('/revisereader','post',book.ReviseReader);
app.route('/queryreader','post',book.QueryReader);
app.route('/overtimelist','post',book.OvertimeList);
app.route('/unreturnlist','post',book.UnReturnList);

// app.route('/login','post',book.Login);
// app.route('/listuser','get',book.List);

