data LineType = Horizontal | Vertical | Diagonal deriving (Show, Eq)

type Point = (Int, Int)

data Line = Line LineType (Point, Point) deriving (Show, Eq)

fromCoords :: (Point, Point) -> Line
fromCoords l@((x1, y1), (x2, y2))
  | x1 == x2 = Line Vertical l
  | y1 == y2 = Line Horizontal l
  | otherwise = Line Diagonal l

intersect :: Line -> Line -> [Point]
intersect (Line Vertical ((ax1, ay1), (ax2, ay2))) (Line Vertical ((bx1, by1), (bx2, by2))) = undefined
intersect (Line Horizontal ((ax1, ay1), (ax2, ay2))) (Line Vertical ((bx1, by1), (bx2, by2))) = undefined
intersect (Line Horizontal ((ax1, ay1), (ax2, ay2))) (Line Horizontal ((bx1, by1), (bx2, by2))) = undefined

main = undefined
