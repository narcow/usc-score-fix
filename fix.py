#!/bin/python3
''' Python 3 script to recover scores after maps.db corruption in unnamed-sdvx-clone. '''

import sqlite3

good_db = sqlite3.connect( 'maps.db' )
bad_db = sqlite3.connect( 'corrupt.db' )

bc = bad_db.cursor()
bc2 = bad_db.cursor()
gc = good_db.cursor()

bc.execute( 'select count(*) from difficulties' )
count = bc.fetchone()[0]

bc.execute( 'select rowid, path from difficulties order by rowid' )
total_scores = 0

for _ in range(count):
    b_diffid, path = bc.fetchone()
    gc.execute( 'select rowid from difficulties where path=:path', {'path': path} )
    g_diffid = gc.fetchone()[0]
    #print( 'map old %i to %i' %(b_diffid, g_diffid) )
    bc2.execute( 'select count(*) from scores where diffid=:diffid', {'diffid': b_diffid} )
    score_count = bc2.fetchone()[0]
    bc2.execute( 'select * from scores where diffid=:diffid', {'diffid': b_diffid} )
    for __ in range(score_count):
        score, crit, near, miss, gauge, gameflags, diffid, hitstats, timestamp = bc2.fetchone()
        new_score_row = ( score, crit, near, miss, gauge, gameflags, g_diffid, hitstats, timestamp )
        gc.execute( 'insert into scores values ( ?, ?, ?, ?, ?, ?, ?, ?, ? )', new_score_row )
        total_scores += 1
        #print( 'found score %i from time %i' %(score, timestamp) )


good_db.commit()
print( 'migrated %i scores successfully' %total_scores )

bc.close()
bc2.close()
gc.close()
