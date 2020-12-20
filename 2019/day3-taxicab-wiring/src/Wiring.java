import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.LinkedList;
import java.util.List;

public class Wiring {
    private LinkedList<Line> wire1 = new LinkedList<>(), wire2 = new LinkedList<>();

    public Wiring(String left, String right) {
        String[] leftA = left.split(","), rightA = right.split(",");
        makeWire(leftA, wire1);
        makeWire(rightA, wire2);
    }


    private void makeWire(String[] input, List<Line> lines) {
        Coordinate start = new Coordinate(0, 0), end;
        for (String string : input) {
            char direction = string.charAt(0);
            int length = Integer.parseInt(string.substring(1));
            int x, y, startX = start.getX(), startY = start.getY();
            switch (direction) {
                case 'R':
                    x = start.getX() + length;
                    y = start.getY(); // horizontal
                    startX++; // preventing excess points in line
                    // TODO not even *that* seems to help, mkay
                    break;
                case 'L':
                    x = start.getX() - length;
                    y = start.getY(); // horizontal
                    startX--;
                    break;
                case 'D':
                    y = start.getY() - length;
                    x = start.getX(); // vertical
                    startY--;
                    break;
                case 'U':
                    y = start.getY() + length;
                    x = start.getX(); // vertical
                    startY++;
                    break;
                default:
                    throw new IllegalArgumentException("Illegal character in wire string");
            }
            start = new Coordinate(startX, startY);
            end = new Coordinate(x, y);
            lines.add(new Line(start, end));
            start = end;
        }
    }

    public List<Coordinate> findIntersections() {
        LinkedList<Coordinate> intersections = new LinkedList<>();
        for (Line line1 : wire1) {
            for (Line line2 : wire2) {
//                System.out.println(line1 + " ahd " + line2);
                if (line1.intersectsWith(line2)) {
                    intersections.add(line1.findIntersection(line2));
                    System.out.println("Intersection at " + intersections.getLast() + " at distance " + intersections.getLast().distanceFromOrigin());
                }
            }
        }
        return intersections;
    }

    public Coordinate findClosest(List<Coordinate> coordinates) {
        int min = Integer.MAX_VALUE;
        Coordinate res = null;
        for (Coordinate coord : coordinates) {
            if (coord.distanceFromOrigin() == 0) continue;
            if (coord.distanceFromOrigin() < min) {
                min = coord.distanceFromOrigin();
                res = coord;
            }
        }
        return res;
    }

    public static void main(String[] args) {
        String[] heh = null;
        try {
            heh = readFile("day3-taxicab-wiring/input", Charset.defaultCharset()).split("\n");
        } catch (IOException e) {
             e.printStackTrace();
        }
        Wiring wiring = new Wiring(heh[0], heh[1]);
//        Wiring wiring = new Wiring("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"); // 159 but I get 66
//        Wiring wiring = new Wiring("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"); // 135 but I get 91 but then I get correct when removing *that*...
//        Wiring wiring = new Wiring("R8,U5,L5,D3", "U7,R6,D4,L4"); // 6 as I get
        Coordinate place = wiring.findClosest(wiring.findIntersections());
        System.out.println("is at " + place + " distance " + place.distanceFromOrigin());
    }

    // from ze web I guess
    static String readFile(String path, Charset encoding) throws IOException {
        byte[] encoded = Files.readAllBytes(Paths.get(path));
        return new String(encoded, encoding);
    }
}

class Coordinate {
    private int x, y;

    public Coordinate(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public int distanceFromOrigin() {
        return Math.abs(x) + Math.abs(y);
    }

    @Override
    public String toString() {
        return "(" + x + ", " + y + ")";
    }
}

class Line {
    private final Coordinate start, end;
    private boolean horizontal;

    public Line(Coordinate start, Coordinate end) {
        this.start = start;
        this.end = end;
        this.horizontal = start.getY() == end.getY(); // y coords are same
    }

    public boolean intersectsWith(Line other) {
//        return (start.getX() + end.getX()) * (other.start.getX() + other.end.getX())
//                + (start.getY() + end.getY()) * (other.start.getY() + other.end.getY())
//                == 0; // dot product is 0 when two vectors intersect
        if (this.horizontal && other.horizontal || !this.horizontal && !other.horizontal) {
            // TODO check if overlap, you fool
            return false; // both horiz or both vert
        }

        if (this.horizontal) {
            // other is vertical at x = something
            return (this.start.getX() <= other.start.getX() && other.start.getX() <= this.end.getX())
                   || (this.start.getX() >= other.start.getX() && other.start.getX() >= this.end.getX());
//            return (this.start.getX() >= other.start.getX() && other.start.getX() >= this.end.getX());
        } else {
            // other is horizontal at y = something
            return (this.start.getY() <= other.start.getY() && other.start.getY() <= this.end.getY())
                    || (this.start.getY() >= other.start.getY() && other.start.getY() >= this.end.getY());
//            return (this.start.getY() >= other.start.getY() && other.start.getY() >= this.end.getY());
        }
    }

    public Coordinate findIntersection(Line other) {
        if (this.horizontal) { // then extract y from self and x from other
            return new Coordinate(other.start.getX(), this.start.getY());
        } else { // other has y
            return new Coordinate(this.start.getX(), other.start.getY());
        }
    }

    @Override
    public String toString() {
        return start.toString() + " -> " + end.toString();
    }
}
