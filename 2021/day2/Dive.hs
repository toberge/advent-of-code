data Direction = Forward Int | Down Int | Up Int deriving Show

type Point    = (Int, Int)
type AimPoint = (Int, Int, Int)

parse :: String -> Direction
parse = innerParse . words
  where
    innerParse ["forward", x] = Forward (read x)
    innerParse ["down",    x] = Down (read x)
    innerParse ["up",      x] = Up (read x)
    innerParse _              = Forward 0


travel1 :: Point -> Direction -> Point
travel1 (pos, depth) (Forward x) = (pos + x, depth)
travel1 (pos, depth) (Down x)    = (pos, depth + x)
travel1 (pos, depth) (Up x)      = (pos, depth - x)

travel2 :: AimPoint -> Direction -> AimPoint
travel2 (pos, depth, aim) (Forward x) = (pos + x, depth + aim * x, aim)
travel2 (pos, depth, aim) (Down x)    = (pos, depth, aim + x)
travel2 (pos, depth, aim) (Up x)      = (pos, depth, aim - x)

solve1 :: [Direction] -> Int
solve1 = (\(p, d) -> p * d) . foldl travel1 (0, 0)

solve2 :: [Direction] -> Int
solve2 = (\(p, d, _) -> p * d) . foldl travel2 (0, 0, 0)

-- TODO two things in main I suppose
main = interact $ show . solve2 . map parse . lines
