import sqlite3 as sql
import datetime


def connect():                              # connect with sqlite database
    connection = sql.connect("store.db")
    return connection


def open(db):                               # create database tables if not present
    db.execute("""create table if not exists EXPEND(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\
                , ITEM_NAME TEXT, COMPANY TEXT, QUANTITY REAL NOT NULL, AMOUNT REAL NOT NULL\
                , CASH_FLOW TEXT NOT NULL, TRANSACTION_TYPE TEXT NOT NULL, ITEM_TYPE TEXT NOT NULL\
                , TIME TEXT NOT NULL);""")


def insert(db, details):                    # insert records in database
    currentime = str(datetime.datetime.now())
    db.execute(f"""insert into EXPEND(ITEM_NAME,COMPANY,QUANTITY,UNIT\
                    ,AMOUNT,CURRENCY,AFFILIATE,CASH_FLOW,TRANSACTION_TYPE,ITEM_TYPE,TIME)\
                    VALUES('{details['item']}',"{details['comp']}",{details['quant']}\
                    , '{details['unit']}',{details['amt']},'{details['currency']}'\
                    , '{details['aff']}','{details['flow']}','{details['stat']}'\
                    , '{details['itemtype']}','{currentime}');""")
    db.commit()


def delete(db, idtag):                      # delete records from database
    db.execute(f"delete from EXPEND where ID={idtag}")
    db.commit()


def search(db, vals):                       # search for records in database
    keys = ["ITEM_NAME", "COMPANY", "QUANTITY", "UNIT", "AMOUNT", "CURRENCY", "AFFILIATE", "CASH_FLOW", "TRANSACTION_TYPE", "ITEM_TYPE"]
    var = []
    for i, j in enumerate(vals):
        if j != "":
            if keys[i] not in "QUANTITYAMOUNT":
                var.append(f"{keys[i]} LIKE '%{j}%'")
            else:
                var.append(f"{keys[i]} = {j}")
    var = ' and '.join(var)
    query = f"select * from EXPEND{' where ' + var if var != '' else ''};"
    return db.execute(query).fetchall()


def edit(db, vals, idtag):                  # edit values in database
    keys = ["ITEM_NAME", "COMPANY", "QUANTITY", "UNIT", "AMOUNT", "CURRENCY", "AFFILIATE", "CASH_FLOW", "TRANSACTION_TYPE", "ITEM_TYPE"]
    var = []
    flag = 0
    for i, j in enumerate(vals):
        if keys[i] not in "COMPANYAFFILIATE" and j == "":
            flag = 1
            break
        if keys[i] not in "QUANTITYAMOUNT":
            var.append(f"{keys[i]} = '{j}'")
        else:
            var.append(f"{keys[i]} = {j}")
    if not flag:
        var = ','.join(var)
        query = f"update EXPEND set {var} where ID={idtag};"
        db.execute(query)
        db.commit()
        return True
    return False

