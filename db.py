import sqlite3
import traceback



#copy from https://github.com/binux/libMA/blob/master/basedb.py
class BaseDB:
    '''
    BaseDB

    dbcur should be overwirte
    '''
    @property
    def dbcur(self):
        raise Exception("NOT IMPLEMENTED")

    def _execute(self, sql_query, values=[]):
        try:
            print sql_query, values
            return self.dbcur.execute(sql_query, values)
        except:
            print repr(sql_query)
            for i in values:
                print repr(i),
            print
            print traceback.format_exc()
    
    def _select2list(self, tablename, what="*", where="", offset=0, limit=None):
        sql_query = "SELECT %s FROM %s" % (what, tablename)
        if where: sql_query += " WHERE %s" % where
        if limit: sql_query += " LIMIT %d, %d" % (offset, limit)

        return self._execute(sql_query).fetchall()

    def _select(self, tablename, what="*", where="", offset=0, limit=None):
        sql_query = "SELECT %s FROM %s" % (what, tablename)
        if where: sql_query += " WHERE %s" % where
        if limit: sql_query += " LIMIT %d, %d" % (offset, limit)

        dbcur = self._execute(sql_query)
        fields = [f[0] for f in dbcur.description]
        if limit:
            return [dict(zip(fields, row)) for row in dbcur.fetchall()]
        else:
            return (dict(zip(fields, row)) for row in dbcur.fetchall())
 
    def _replace(self, tablename, **values):
        if values:
            _keys = ", ".join(("`%s`" % k for k in values.iterkeys()))
            _values = ", ".join(["?", ] * len(values))
            sql_query = "REPLACE INTO `%s` (%s) VALUES (%s)" % (tablename, _keys, _values)
        else:
            sql_query = "REPLACE INTO %s DEFAULT VALUES" % tablename
        
        if values:
            dbcur = self._execute(sql_query, values.values())
        else:
            dbcur = self._execute(sql_query)
        return dbcur.lastrowid
 
    def _insert(self, tablename, **values):
        if values:
            _keys = ", ".join(("`%s`" % k for k in values.iterkeys()))
            _values = ", ".join(["?", ] * len(values))
            sql_query = "INSERT INTO `%s` (%s) VALUES (%s)" % (tablename, _keys, _values)
        else:
            sql_query = "INSERT INTO %s DEFAULT VALUES" % tablename
        
        if values:
            dbcur = self._execute(sql_query, values.values())
        else:
            dbcur = self._execute(sql_query)
        return dbcur.lastrowid

    def _update(self, tablename, where, **values):
        _key_values = ", ".join(["`%s` = ?" % k for k in values.iterkeys()]) 
        sql_query = "UPDATE %s SET %s WHERE %s" % (tablename, _key_values, where)

        return self._execute(sql_query, values.values())
    
    def _delete(self, tablename, where):
        sql_query = "DELETE FROM %s" % tablename
        if where: sql_query += " WHERE %s" % where
        logger.debug("<sql: %s>" % sql_query)

        return self._execute(sql_query)


class XiamiDB(BaseDB):

    def __init__(self, path="xiami.db"):
        self.conn = sqlite3.connect(path)
        cursor = self.conn.cursor()
        cursor.execute("""create table if not exists users(
            email varchar(32),password varchar(32),
            uid integer PRIMARY KEY,cookie text default '',
            last default 0,days default 0,errcount default 0,
            nexttime default 0,notify default 0,status text)""")
        self.conn.commit()

    @property
    def dbcur(self):
        self.conn.commit()
        return self.conn.cursor()

    def scan(self, where=None):
        return self._select("users",where=where)

    def add(self, uid, email, password):
        self._replace("users",uid=uid,email=email,password=password)

    def delete(self, email,password):
        pass

    def get(self,uid):
        for i in self._select("users",where="uid=%s"%uid,limit=1):
            return i

    def update(self,uid,**argv):
        self._update("users",where="uid=%s"%uid,**argv)

xiamidb = XiamiDB()
