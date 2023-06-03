import pymysql


class MysqlConnector:
    def __init__(self, db_name):
        self.session = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='mysql', db=db_name,
                                       charset='utf8')
        self.cur = self.session.cursor()

    def multi_insert(self, sql, staffs):
        try:
            self.cur.executemany(sql, staffs)
            self.session.commit()
        except Exception as e:
            print("Error:", e)
            self.session.rollback()
