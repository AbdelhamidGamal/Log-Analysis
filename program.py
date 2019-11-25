#!/usr/bin/python3
import psycopg2
import datetime

try:
    db = psycopg2.connect("dbname=news")
except psycopg2.Error as e:
    print("Unable to connect to the database")
    print(e.pgerror)
    print(e.diag.message_detail)
    sys.exit(1)

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
    the_cursor.execute('''select alldayviews.date,
    round(((errordayviews.count*100.0) / alldayviews.count), 3) as rate
    from alldayviews, errordayviews
    where alldayviews.date = errordayviews.date
    and ((alldayviews.count*0.01) <  errordayviews.count);''')
    result = the_cursor.fetchall()
    print("days where more than 1% of requests lead to errors:\n")
    for x in result:
        print(x[0], "—", x[1], "% errors")


most_popular_articles()
most_popular_authors()
error_days()

db.close()
