#!/usr/bin/env python3

import psycopg2

DB_NAME = 'news'


def db_get_results(sql_query):
    with psycopg2.connect('dbname={}'.format(DB_NAME)) as db:
        with db.cursor() as cur:
            cur.execute(sql_query)
            results = cur.fetchall()
    return results


def what_are_the_most_popular_three_articles_of_all_time():
    query = """ select articles.title, count(*) from articles join
                log on log.path like CONCAT('%', articles.slug)
                group by title order by count desc limit 3;"""

    results = db_get_results(query)
    for article, views in results:
        print("\t", article, ':', views, 'views')


def who_are_the_most_popular_article_authors_of_all_time():
    query = """select authors.name, count(*) from articles JOIN
               log on log.path like CONCAT('%', articles.slug)
               JOIN authors on authors.id=author group by name
               ORDER BY COUNT DESC limit 3;"""

    results = db_get_results(query)
    for author, views in results:
        print("\t", author, ':', views, 'views')


def on_which_days_did_more_than_1_percent_of_requests_lead_to_errors():
    query = """SELECT total.date, ROUND(((errors.error_requests*1.0)
               / total.requests), 3)*100 AS percent FROM
               (SELECT date(time), count(*) AS error_requests FROM log
               WHERE status <> '200 OK' GROUP BY date) AS errors JOIN
               (SELECT date(time), count(*) AS requests FROM log GROUP BY date)
               AS total ON total.date = errors.date
               WHERE (ROUND(((errors.error_requests*3.0) / total.requests),
               3) > 0.01  ORDER BY percent DESC;"""

    results = db_get_results(query)
    for author, views in results:
        print("\t", author, ':', views, '%', 'of errors')


if __name__ == '__main__':
    print("1. What are the most popular three articles of all time?")
    what_are_the_most_popular_three_articles_of_all_time()
    print()

    print("2. Who are the most popular article authors of all time?")
    who_are_the_most_popular_article_authors_of_all_time()
    print()

    print("3. On which days did more than 1% of requests lead to errors?")
    on_which_days_did_more_than_1_percent_of_requests_lead_to_errors()
