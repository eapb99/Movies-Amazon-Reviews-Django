GLOBAL_QUERY = '''SELECT "reviews"."productid", "reviews"."userid", "reviews"."profilename",
 "reviews"."helpfulness", "reviews"."score", "reviews"."summary", "reviews"."timed", "reviews"."text" FROM "reviews" '''

WHERE_CLAUSE = " WHERE "
USER_FIELD = ' userid '
PRODUCT_FIELD = ' productid '

ORDER_ASC = ' order by score asc limit 10 '
ORDER_DESC = ' order by score desc limit 10 '

METRIC_QUERY = '''select  count(*)as Cantidad,max(score) as MaxValue,
avg(score) as AvgValue, min(score) as MinValue from reviews '''


def queryProduct(tipo):
    if tipo == 'a':
        query = GLOBAL_QUERY + WHERE_CLAUSE + PRODUCT_FIELD + """ = %s """ + ORDER_ASC
    elif tipo == 'd':
        query = GLOBAL_QUERY + WHERE_CLAUSE + PRODUCT_FIELD + """ = %s """ + ORDER_DESC
    return query


def queryUser(tipo):
    if tipo == 'a':
        query = GLOBAL_QUERY + WHERE_CLAUSE + USER_FIELD + """ = %s """ + ORDER_ASC
    elif tipo == 'd':
        query = GLOBAL_QUERY + WHERE_CLAUSE + USER_FIELD + """ = %s """ + ORDER_DESC
    return query
