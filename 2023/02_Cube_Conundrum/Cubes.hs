-- TODO replace with custom function or sth, this is embarrassing
--      (would've used splitOn but my haskell installation is borked)
wordsWhen     :: (Char -> Bool) -> String -> [String]
wordsWhen p s =  case dropWhile p s of
                      "" -> []
                      s' -> w : wordsWhen p s''
                            where (w, s'') = break p s'

type Sample = (Int, Int, Int)

type Game = (Int, [Sample])

parse :: String -> Game
parse = parseGame . wordsWhen (==':')
  where
    parseGame [id, rest] = (read $ last $ words id, map parseSample $ wordsWhen (==';') $ rest)

-- TODO this could be prettier
parseSample :: String -> Sample
parseSample = foldl parseInner (0, 0, 0) . map words . wordsWhen (==',')
  where
    parseInner (r, g, b) [n, "red"]   = (r+(read n), g,   b)
    parseInner (r, g, b) [n, "green"] = (r,   g+(read n), b)
    parseInner (r, g, b) [n, "blue"]  = (r,   g,   b+(read n))

solve game = sum . map game

game1 :: Game -> Int
game1 (i, samples) = case all check samples of
             True -> i
             False -> 0

check (r,g,b) = r <= 12 && g <= 13 && b <= 14

game2 :: Game -> Int
game2 (i, samples) = power $ foldl1 minSample samples

-- this could've been much prettier
minSample :: Sample -> Sample -> Sample
minSample (r1, g1, b1) (r2, g2, b2) = (max r1 r2, max g1 g2, max b1 b2)

power :: Sample -> Int
power (r, g, b) = r * g * b

part1 = show . solve game1 . map parse . lines
part2 = show . solve game2 . map parse . lines

main = do
  stuff <- getContents
  putStr "Part 1: "
  putStrLn $ part1 $ stuff
  putStr "Part 2: "
  putStrLn $ part2 $ stuff
