increases :: [Int] -> Int
increases xs = length $ filter (== True) $ zipWith (>) next current
  where
    next = drop 1 xs
    current = take (length xs - 1) xs

slidingWindow :: [Int] -> [Int]
slidingWindow xs = zipWith3 (\x y z -> x + y + z) a b c
  where
    len = length xs - 2
    c = drop 2 xs
    b = take len $ drop 1 xs
    a = take len xs

solve = increases . slidingWindow

main = interact $ show . solve . map read . words
