@test "Example" {
    run ./partTwo < example.dat
    echo "$output"
    [ "$output" = "1068781" ]
}

@test "Other examples 1" {
    run sh -c "echo blahblah 17,x,13,19 | ./partTwo"
    echo "$output"
    [ "$output" = "3417" ]
}

@test "Other examples 2" {
    run sh -c "echo blahblah 67,7,59,61 | ./partTwo"
    echo "$output"
    [ "$output" = "754018" ]
}

@test "Other examples 3" {
    run sh -c "echo blahblah 67,x,7,59,61  | ./partTwo"
    echo "$output"
    [ "$output" = "779210" ]
}

@test "Other examples 4" {
    run sh -c "echo blahblah 67,7,x,59,61  | ./partTwo"
    echo "$output"
    [ "$output" = "1261476" ]
}

@test "Other examples 5" {
    run sh -c "echo blahblah 1789,37,47,1889  | ./partTwo"
    echo "$output"
    [ "$output" = "1202161486" ]
}
