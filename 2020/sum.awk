BEGIN {
    secs=0
    msecs=0
}
{
    if ($2 == "s")
        secs += $1*1000
    else
        msecs += $1
}
END {
    print "Just secs: "secs", total: "(secs+msecs)
}
