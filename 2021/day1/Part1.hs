solve :: [Int] -> Int
solve xs = length $ filter (== True) $ zipWith (>) next current
  where
    next = drop 1 xs
    current = take (length xs - 1) xs

main = interact $ show . solve . map read . words
