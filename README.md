Mongostat to CSV Conversion Script
==================================

    usage: mstat_to_csv.py [-h] [--version] [--output OUTPUT] [--append]
                           [--noheaders] [--input INPUT] [--columns COLUMNS]
                           [--rowcount] [--listallcolumns] [--listcolumns]

Program to parse the output of mongostat into a CSV file

optional arguments:
  -h, --help         show this help message and exit
  --version          show program's version number and exit
  --output OUTPUT    Define an output file to write to (default is stdout)
  --append           Append output to the file specified by --output
  --noheaders        Don't output header columns (useful with --append)
  --input INPUT      Define an input file tor read from (default is stdin)
  --columns COLUMNS  Only output named columns in the order they appear on the
                     command line
  --rowcount         add a column to the left that numbers each row of output
  --listallcolumns   list out canonical column headings and exit
  --listcolumns      list out columns in current output and exit

Example usage:

The default case:

    JD10Gen:mstat_to_csv jdrumgoole$ mongostat | python mstat_to_csv.py 
    insert,query,update,delete,getmore,command,flushes,mapped,vsize,res,faults,locked db,idx miss %,qr|qw,ar|aw,netIn,netOut,conn,time
    0,0,0,0,0,1|0,0,80m,2.66g,143m,0,local:0.0%,0,0|0,0|0,62b,2k,1,14:24:12
    0,0,0,0,0,1|0,0,80m,2.66g,143m,0,local:0.0%,0,0|0,0|0,62b,2k,1,14:24:13
    0,0,0,0,0,1|0,0,80m,2.66g,143m,0,local:0.0%,0,0|0,0|0,62b,2k,1,14:24:14
    0,0,0,0,0,1|0,0,80m,2.66g,143m,0,local:0.0%,0,0|0,0|0,62b,2k,1,14:24:15
    0,0,0,0,0,1|0,0,80m,2.66g,143m,0,local:0.0%,0,0|0,0|0,62b,2k,1,14:24:16

Just get the query column:

    JD10Gen:mstat_to_csv jdrumgoole$ mongostat | python mstat_to_csv.py --columns query
    query
    0
    0
    0
    0

Get the queries and vsize columns:

    JD10Gen:mstat_to_csv jdrumgoole$ mongostat | python mstat_to_csv.py --columns query --columns vsize
    query,vsize
    0,2.66g
    0,2.66g
    0,2.66g
    1,2.66g
    0,2.66g

Get the output and add a rowcount:

    JD10Gen:mstat_to_csv jdrumgoole$ mongostat | python mstat_to_csv.py --rowcount
    count,insert,query,update,delete,getmore,command,flushes,mapped,vsize,res,faults,locked db,idx miss %,qr|qw,ar|aw,netIn,netOut,conn,time
    1,0,0,0,0,0,1|0,0,80m,2.66g,143m,0,local:0.0%,0,0|0,0|0,62b,2k,1,14:27:21
    2,0,0,0,0,0,1|0,0,80m,2.66g,143m,0,local:0.0%,0,0|0,0|0,62b,2k,1,14:27:22
    3,0,0,0,0,0,1|0,0,80m,2.66g,143m,0,local:0.0%,0,0|0,0|0,62b,2k,1,14:27:23
    4,0,0,0,0,0,1|0,0,80m,2.66g,143m,0,.:0.0%,0,0|0,0|0,62b,2k,1,14:27:24
    5,0,0,0,0,0,1|0,0,80m,2.66g,143m,0,local:0.0%,0,0|0,0|0,62b,2k,1,14:27:25
    6,0,0,0,0,0,1|0,0,80m,2.66g,143m,0,local:0.0%,0,0|0,0|0,62b,2k,1,14:27:26
    7,0,0,0,0,0,1|0,0,80m,2.66g,143m,0,local:0.0%,0,0|0,0|0,62b,2k,1,14:27:27

Get the output and write to a file:

    JD10Gen:mstat_to_csv jdrumgoole$ mongostat | python mstat_to_csv.py --rowcount --output mstat.out
