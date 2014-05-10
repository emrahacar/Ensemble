#!/usr/bin/tclsh
proc atAdi { mylist } { 
    global enc
    # atAdi tek kelime veya birden cok kelime olabilir
    # veya tcl'i bozan () karakterleri de olabilir
    # first encode
    set res [encoding convertto $enc [join $mylist " "]]
    # convert special char to () -> |
    regsub -all -- {\(} $res + res
    regsub -all -- {\)} $res + res
    return $res    
}
set enc utf-8
global enc
#
proc byp {a b} {
  global count
    if {$count($b)==$count($a)} {return 0}
    if {$count($b)>$count($a)} {return 1 }
    return -1
}
#
# number to search
set key [lindex $argv 0]
set files [lrange $argv 1 end]
set res ""
foreach f $files {
#    puts $f
    set ff [open $f r]
    set whole [split [read $ff] \n]
    close $ff
    foreach  w $whole {
	if {[regexp "=\ $key\ " $w]} {
	    lappend res $w
	}
    }
}
set count(0) 0
global count
foreach w $res {
    if {[regexp {== tahmin.+ ==\ ([[:alpha:]\ ]+) .+[0-9] ([[:alpha:]\ ]+) .+[0-9] ([[:alpha:]\ ]+) .+[0-9]} $w tmp a b c]} {
	# birinciye 1.5,ikinciye 1.2, ucuncuye 1
	#
	set birinci 1.75
	set ikinci  1.25
	set ucuncu  1.01
	set count(0) [expr $count(0)+1.75]
	if {[catch {set count($a) [expr $birinci+$count($a)]}]} {set count($a) $birinci}
	if {[catch {set count($b) [expr $ikinci+$count($b)]}]} {set count($b) $ikinci}
	if {[catch {set count($c) [expr $ucuncu+$count($c)]}]} {set count($c) $ucuncu}
    }
    if {[string is integer -strict [lindex $w 0]]} {
	# set db([lrange $w 7 end]) [lindex $w 0]
	set db([atAdi [lrange $w 7 end]]) [lindex $w 0]

    }
}
set count0 $count(0)
unset count(0)
set emptyLine "                  "
foreach k [lsort -command byp [array names count]] {
    set val [format "%4.1f" [expr 100.0*$count($k)/$count0]]
    puts "[format "%16s %5s" [string range ${k}${emptyLine} 0 15] $val]"
}
