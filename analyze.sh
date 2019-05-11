#!/bin/bash
set -e
#set -x

# https://extendsclass.com/sqlite-browser.html

db_file=~/openwpm_results/crawl-data.sqlite
if [ ! -f $db_file ]; then
	db_file=$(find ~ -maxdepth 1 | grep openwpm_results | sort -r | head -n 1)/crawl-data.sqlite
fi
echo using database $db_file

python << EOF
import sqlite3
from six.moves.urllib.parse import urlparse

conn = sqlite3.connect('${db_file}')
select_cursor = conn.cursor()
insert_cursor = conn.cursor()

# Create an empty table
insert_cursor.execute('DROP TABLE IF EXISTS third_party_analyze')
insert_cursor.execute('CREATE TABLE IF NOT EXISTS third_party_analyze ( url TEXT, top_level_url TEXT, is_third_party INTEGER )')
#conn.commit()

# all_rows = cursor.fetchall()
for row in select_cursor.execute('SELECT url , top_level_url FROM http_requests;'):
	#print row
	#print(urlparse(row[0]).netloc,"\t",urlparse(row[1]).netloc)
	is_third_party = ( urlparse(row[0]).hostname != urlparse(row[1]).hostname ) and ( urlparse(row[1]).hostname != None )
	#print(is_third_party)
	# Insert a row of data
	insert_cursor.executemany('INSERT INTO third_party_analyze VALUES (?,?,?)', [( row[0], row[1], 1 if is_third_party else 0)])
	#conn.commit()

# Save (commit) the changes
conn.commit()

conn.close()
EOF

# export instrumented data to a html file (an ugly way...)
html_file=$(dirname $db_file)/export.html
echo exporting to $html_file
echo "<html><body>" >$html_file
for table in $(echo ".tables" | sqlite3 $db_file); do
	#break
	echo -e "\n<hr>" >>$html_file
	echo "<h1>${table}</h1>" >>$html_file
	echo "<table border=1>" >>$html_file
	echo -e ".headers ON\n.mode html\nSELECT * FROM $table;" | sqlite3 $db_file >>$html_file
	echo "</table>" >>$html_file
done
echo "</body></html>" >>$html_file

#echo -e ".headers ON\nSELECT top_level_url, COUNT(*) FROM third_party_analyze WHERE is_third_party=0 GROUP BY top_level_url;" | sqlite3 $db_file
echo
echo -e ".headers ON\n.mode column\n.width 50 -14 -11 -22\n\
		SELECT \
			top_level_url, \
			COUNT(*) AS 'total requests', \
			COUNT(case when is_third_party = 1 then 1 else null end) AS 'third party', \
			printf( '%6.2f%', COUNT(case when is_third_party = 1 then 1 else null end) * 100.0 / COUNT(*) ) AS 'third party requests %' \
		FROM third_party_analyze \
		WHERE top_level_url != 'about:blank' AND top_level_url != 'undefined' \
		GROUP BY top_level_url \
		ORDER BY COUNT(case when is_third_party = 1 then 1 else null end) DESC;" | sqlite3 $db_file

if [ -d ~/openwpm_results ]; then
	mv ~/openwpm_results ~/.openwpm_results_$(date +"%Y%m%d%H%M%S%N")
fi

echo
