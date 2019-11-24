#!/usr/bin/python3
import psycopg2
import datetime

db = psycopg2.connect("dbname=news")
the_cursor = db.cursor()


def most_popular_articles():
    the_cursor.execute('''select articles.title, count(log.path) as views
    from articles, log where articles.slug = substring(log.path, 10)
    group by articles.title order by views desc limit 3;''')
    result = the_cursor.fetchall()
    print("Most popular three articles of all time:\n")
    for x in result:
        print(x[0]+" — "+str(x[1])+" views")
    print("__________________________________________________\n")


def most_popular_authors():
    the_cursor.execute('''select authors.name, count(log.path) as views
    from authors, articles, log
    where articles.slug = substring(log.path, 10)
    and articles.author = authors.id
    group by authors.name order by views desc;''')
    result = the_cursor.fetchall()
    print("Most popular authors of all time:\n")
    for x in result:
        print(x[0]+" — "+str(x[1])+" views")
    print("__________________________________________________\n")


def error_days():
    the_cursor.execute('''create view alldayviews as select date(time),
     count(date(time)) from log  group by date order by date desc;''')
    the_cursor.execute('''create view errordayviews as select date(time),
    count(date(time)) from log
    where status > '400' group by date order by date desc;''')
    the_cursor.execute('''select alldayviews.date,
    round(((errordayviews.count*100.0) / alldayviews.count), 3) as rate
    from alldayviews, errordayviews
    where alldayviews.date = errordayviews.date
    and ((alldayviews.count*0.01) <  errordayviews.count);''')
    result = the_cursor.fetchall()
    print("days where more than 1% of requests lead to errors:\n")
    for x in result:
        print(x[0], "—", x[1],"% errors")


most_popular_articles()
most_popular_authors()
error_days()

db.close()
