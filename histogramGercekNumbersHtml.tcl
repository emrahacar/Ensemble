#!/usr/bin/tclsh
#
# this one combines the WPS triple and updates them, with weight 
# provided.
#
# updated- Jun 7 2013
set db(0) 0
set enc utf-8
global enc db

proc atAdi { mylist } { 
    global enc
    # multi - word veya  tcl'i bozan () karakterleri de olabilir
    set res [encoding convertto $enc [join $mylist " "]]
    regsub -all -- {\ +\([A-Z]+\).*} $res "" res
    return $res
}
proc setAtNo { no mylist } {
    # set db([encoding convertto $enc "[lrange $w 7 end] "]) [lindex $w 0]
    global db
    set at [atAdi $mylist]
    set db($at) $no
    return $no
}
proc atNo { k } {
    # count arrays have space in the end, we need to remove them
    global db enc
    set no 0
    set k [encoding convertto $enc $k]
    catch { set no $db($k) } msg
    return $no
}
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
#set enc unicode

foreach f $files {
#    puts $f
    set ff [open $f r]
    set whole [split [read $ff] \n]
    close $ff
    foreach  w $whole {
	if {[string is integer -strict [lindex $w 0]]} {
	    setAtNo [lindex $w 0] [lrange $w 7 end]
	}
	if {[regexp "=\ $key\ " $w]} {
	    lappend res $w
	}
    }
}
set count(0) 0
set count1(0) 0
set count2(0) 0
set count3(0) 0
global count
foreach w $res {
    if {![regexp {== weight ([0-9\.]+) ==} $w tmp myweight]} {
	set myweight 1.0
    }
    if {[regexp {== tahmin.+ ==\ ([[:alpha:]\ ]+) .+[0-9] ([[:alpha:]\ ]+) .+[0-9] ([[:alpha:]\ ]+) .+[0-9]} $w tmp a b c]} {
	# birinciye 1.5,ikinciye 1.2, ucuncuye 1
	#
	set birinci [expr 1.75*$myweight]
	set ikinci  [expr 1.25*$myweight]
	set ucuncu  [expr 1.01*$myweight]
	set count(0) [expr 1.0*$myweight+$count(0)]
	# at Adlarinda son char ' ' oldugundan siliyoruz.
	# correct atAdi, remove
	regsub -all -- {\ +$} $a "" a
	regsub -all -- {\ +$} $b "" b
	regsub -all -- {\ +$} $c "" c
	# increment tot
	if {[catch {set count($a) [expr $birinci+$count($a)]}]} {set count($a) $birinci}
	if {[catch {set count($b) [expr $ikinci+$count($b)]}]} {set count($b) $ikinci}
	if {[catch {set count($c) [expr $ucuncu+$count($c)]}]} {set count($c) $ucuncu}
	# increment 1, 2, 3 posizyon sayisi
	if {[catch {incr count1($a)}]} {set count1($a) 1}
	if {[catch {incr count2($b)}]} {set count2($b) 1}
	if {[catch {incr count3($c)}]} {set count3($c) 1}
    }
}
set count0 $count(0)
unset count(0)
set emptyLine "                  "
set tot 0.0
foreach k [lsort -command byp [array names count]] {
    set val $count($k)
    set tot [expr $tot+(1.0*$val)]
}
foreach k [lsort -command byp [array names count]] {
    set prob($k) [expr $count($k)/$tot]
}
foreach k [lsort -command byp [array names count]] {
#    set gny [format "%2.2f" [expr $count($k)/$iprobtot]]
    set val [format "%4.1f" [expr 100.0*$count($k)/$count0]]
    if {[info exists count1($k)]==0} {set count1($k) 0}
    if {[info exists count2($k)]==0} {set count2($k) 0}
    if {[info exists count3($k)]==0} {set count3($k) 0}
    set val2 [format "%3d/%3d/%3d" $count1($k) $count2($k) $count3($k)]
    set p [format "%2.1f" [expr 100.0*$prob($k)]]
    set no [atNo $k]
    # puts "[format "%16s %5s %11s | " [string range ${no}:${k}${emptyLine} 0 15] $val $val2 ]"
    puts stdout  "<td> [format "%16s" [string range ${no}:${k}${emptyLine} 0 15]] </td>" nonewline
    puts stdout  "<td> $val </td>" nonewline
    puts stdout  "<td> $count1($k) </td>" nonewline 
    puts stdout  "<td> $count2($k) </td>" nonewline
    puts stdout  "<td> $count3($k) </td>" 
}
