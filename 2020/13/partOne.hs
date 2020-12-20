import Data.List
import Data.List.Split
import Data.Ord

splitit :: [String] -> (Integer, [Integer])
splitit str = (n, xs) where
    n = read $ head str
    xs = map read $ filter (/= "x") $ splitOn "," (str !! 1)

dist :: Integer -> Integer -> (Integer, Integer)
dist n x = (d, x) where
    rest = n `mod` x
    d = (x - rest) `mod` x

solve :: (Integer, [Integer]) -> Integer
solve (n, xs') = uncurry (*) $ minimumBy (comparing fst) xs where
    xs = map (dist n) xs'

main = interact $ show . solve . splitit . words
