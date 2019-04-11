 #! /usr/bin/env python3

import psycopg2
DB_NAME = 'news'


def db_get_results(sql):
   with psycopg2.connect('dbname={}'.format(DB_NAME)) as db:
       with db.cursor() as cur:
           cur.execute(sql)
           results = cur.fetchall()
   return results

def What_are_the_most_popular_three_articles_of_all_time ():
   results = db_get_results("select articles.title, count(*) from articles join log on log.path like CONCAT('%', articles.slug) group by title order by count desc limit 3;")

   for article, views in results:
       print(article, ':', views, 'views')

def Who_are_the_most_popular_article_authors_of_all_time ():
   results = db_get_results("select authors.name, count(*) from articles JOIN log on log.path like CONCAT('%', articles.slug)JOIN authors on authors.id=author group by name ORDER BY COUNT DESC limit 3;")

   for author, views in results:
       print(author, ':', views, 'views')

def On_which_days_did_more_than_1_percent_of_requests_lead_to_errors ():
   results = db_get_results("SELECT total.date, ROUND(((errors.error_requests*1.0) / total.requests), 3)*100 AS percent FROM (SELECT date(time), count(*) AS error_requests FROM log WHERE status <> '200 OK' GROUP BY date) AS errors JOIN (SELECT date(time), count(*) AS requests FROM log GROUP BY date) AS total ON total.date = errors.date WHERE (ROUND(((errors.error_requests*1.0) / total.requests), 3) > 0.01) ORDER BY percent DESC;")

   for author, views in results:
       print(author, ':', views, 'views')


if __name__ == '__main__':
   task_1()
