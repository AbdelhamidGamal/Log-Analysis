# Log Analysis

This program analyzes the log of a news Magazine.

## Getting Started

Copy the source code on your machine and run it against the database.


### Prerequisites

* Linux machine.
* python.
* PostgreSQL.


## Running the tests

You just need to run the program.py file. nothing else.

## Code explanation

This program contains three main functions:

1.most_popular_articles()

this function prints out the most popular 3 article of all time through this code:
```
select articles.title, count(log.path) as views from articles, log where articles.slug =log.path group by articles.title order by views desc limit 3;
```
which prints out the articles title and how many views each one got through joining articles table and log table .

2.most_popular_authors()

this function prints out the most popular 3 authors of all time through this code:
```
select authors.name, count(log.path) as views from authors, articles, log where articles.slug = log.path and articles.author = authors.id group by authors.name order by views desc limit 3;
```
which prints out the author name and how many views each one got through joining authors , articles and log tables together


3.error_days()

this code prints out on which days more than 1% of requests lead to errors through this code:
```
create view alldayviews as select date(time), count(date(time)) from log  group by date order by date desc;
```
which creates a view named (alldayviews) which prints out the total views count of each day.
and this code:
```
create view errordayviews as select date(time), count(date(time)) from log where status > '400' group by date order by date desc;
```
which create a view named (errordayviews) which prints out the total count of errors in each day.
and this code:
```
select * from alldayviews, errordayviews where alldayviews.date = errordayviews.date and ((alldayviews.count*0.01) <  errordayviews.count);
```
which prints the days that have more than 1% errors of total requests .


## Authors

* **Abdelhamid Ismail**
