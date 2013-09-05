#!/usr/local/bin/python
# Simple program to parse mongostat output into a sensible CSV format for ingestion
# by Google Docs or Excel.
# 
# Mongostat does some things that make it difficult to ingest into Excel or a Google Spreadsheet,
# including:
#
#  Field labels that have spaces and special characters in them
#  Varying column widths
#  Columns within columns
#  No defined column seperator
#  Automatic insert of header fields ever 10 lines or so.
#
# Mongostat_sane.py can read from stdin (via a pipe) or a file and write to stdout or a file.
#
# By default it converts all input into CSV format.
#
# You can direct its output to a file with the --output <filename> argument.
#
# You can read from a file with with the --input <filenamne> argument.
#
# You can select a specific column to output by using the the --columns <column name> argument.
# The --columns argument can be repeated to select more than one column. The columns are output in the
# order of the arguments.
#
# You can list the canonical column names with --listcolumns
#
# You can add a rowcount column using the --rowcount argument. This allows the output to be normalised
# on a standard interval so different runs of the program can be graphed on the same timescale.
#
# joe.drumgoole@10gen.com 
#

import sys
import re
import argparse
import collections

column_order = [ 'insert', # 0
           'query',        # 1
           'update',       # 2
           'delete',       # 3
           'getmore',      # 4
           'command',      # 5
           'flushes',      # 6
           'mapped',       # 7
           'vsize',        # 8
           'res',          # 9
           'faults',       # 10
           'locked db',    # 11
           'idx miss %',   # 12
           'qr|qw',        # 13
           'ar|aw',        # 14
           'netIn',        # 15
           'netOut',       # 16
           'conn',         # 17
           'set',          # 18
           'repl',         # 19
           'time' ]        # 20

column_indexes = { 'insert'    : 0,
           'query'      : 1,
           'update'     : 2,
           'delete'     : 3,
           'getmore'    : 4,
           'command'    : 5,
           'flushes'    : 6,
           'mapped'     : 7,
           'vsize'      : 8,
           'res'        : 9,
           'faults'     : 10,
           'locked db'  : 11,
           'idx miss %' : 12,
           'qr|qw'      : 13,
           'ar|aw'      : 14,
           'netIn'      : 15,
           'netOut'     : 16,
           'conn'       : 17,
           'set'        : 28,
           'repl'       : 10,
           'time'       : 20 }  #also set and repl but not for this version


def parseHeader( canonical_columns, x ) :

    headers = collections.OrderedDict() 
    
    position = 0
    for i in canonical_columns:
        if re.search( i, x ) :
#            print "found %s in %s" % ( i, x )
            headers[ i ] = position 
            position += 1
 
    return headers

def parseLine( x ) :
    x =re.sub( '^[ ]+', "", x )
    x =re.sub( '[ ]+$', "", x ) 
    x= re.sub( '[ ]+', ',', x )
    x= re.sub( '\*', '', x )
    return x.split( ',' ) 

def processLine( x, actual_columns, selectors ) :
    return  processColumns( parseLine( x ), actual_columns, selectors )  

def processHeader( actual_columns, selectors ) :
    
    output_columns = []
    for i in selectors:
        if i in actual_columns :
            output_columns.append( i ) 

    return ",".join( output_columns ) 
        


def processColumns( column_data, actual_columns, selectors ) :
#
# Take a row of column data and a list of selected columns and filter out the columns
# that will be output based on the selectors. Data has been pre-cleaned so selectors is non-zero
# and valid.
#
    
    output_columns = []
#    print ( "selectors : %s" % selectors )  
    for i in selectors :
#            print "index : %s %d " % ( i, actual_columns[ i ] )
        output_columns.append( column_data[ actual_columns[ i ]]) 

    return ','.join( output_columns ) + "\n"
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser( description="Program to parse the output of mongostat into a CSV file" )

    parser.add_argument('--version', action='version', version='%(prog)s 0.2.1 beta')

    parser.add_argument( "--output", 
                         help="Define an output file to write to (default is stdout)",
                         default="stdout" )

    parser.add_argument( "--append", 
                         action="store_true",
                         help="Append output to the file specified by --output",
                         default=False )

    parser.add_argument( "--noheaders", 
                         action="store_true",
                         help="Don't output header columns (useful with --append)",
                         default=False )

    parser.add_argument( "--input",
                         help="Define an input file tor read from (default is stdin)",
                         default="stdin"  )

    parser.add_argument( "--columns",
                         action='append',
                         help="Only output named columns in the order they appear on the command line", 
                         default=[] )

    parser.add_argument( "--rowcount",
                         action='store_true',
                         help="add a column to the left that numbers each row of output", 
                         default=False )

    parser.add_argument( "--listallcolumns",
                         action="store_true",
                         help="list out canonical column headings and exit", 
                         default=False )
    
    parser.add_argument( "--listcolumns",
                         action="store_true",
                         help="list out columns in current output and exit", 
                         default=False )

    args = parser.parse_args()

    if args.input == "stdin" :
        input = sys.stdin 
    else :
        input = open( args.input, "r" ) ;

    writeStr = "wb"
    if args.output == "stdout" :
        output = sys.stdout 
    else :
        if args.append :
            writeStr = "ab" ;
            
        output = open( args.output, writeStr )

    if args.listallcolumns :
        output.write( ','.join( column_order )) 
        output.write( "\n" ) 
        output.close()
        sys.exit( 0 )

    x = input.readline()  #
 
    if x.startswith( "connected" ) :
#        print( x.rstrip( "\n" ))
        x = input.readline()  # strip of connected to

    if x.startswith( "insert" ) :
#        print( x.rstrip( "\n" ))
        actual_columns = parseHeader( column_order, x.rstrip( "\n" ))
        selected_columns = []

        #
        # if the user selects a column which is not in the output we ignore it.
        #
        

        if len( args.columns ) == 0 :
            # just use the list of columns we parsed if the user didn't select any
            selected_columns = actual_columns 
        else:
            for i in args.columns :
                if i in actual_columns  :
                    selected_columns.append( i ) 
                else :
                    sys.stderr.write( "Warning : you selected display of a column, '%s', which is not in the mongostat output\n" % i )

#        print( "actual columns : %s" % actual_columns )
#        print( "selected columns: %s" % selected_columns )

        if args.noheaders :
            pass
        else:
            if args.rowcount :
                output.write( "count," ) 
    
            output.write( processHeader( actual_columns, selected_columns )) # print headers once
            
            output.write( "\n" ) 

            if args.listcolumns :
                sys.exit( 0 ) # we are done.

        x = input.readline()  # 

    rowcounter = 1
    while x :
        if x.startswith( "insert" ) :
            x = input.readline()
            continue # strip out occasional header lines

        if args.rowcount :
            output.write( "%i," % rowcounter ) ;
            rowcounter += 1 

        output.write( processLine( x.rstrip( "\n" ), actual_columns, selected_columns )) # print headers once
        
        output.flush() 
#        print( x.rstrip( "\n" ))
        x = input.readline()

    input.close()
    output.close()
    
