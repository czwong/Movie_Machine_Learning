USE 2019_movies;

DELETE `a`
FROM
    `movie_data` AS `a`,
    `movie_data` AS `b`
WHERE
    -- IMPORTANT: Ensures one version remains
    -- Change "ID" to your unique column's name
    `a`.`movieID` < `b`.`movieID`

    -- Any duplicates you want to check for
    AND `a`.`name` <=> `b`.`name`;
    
USE 2019_movies;

DELETE `a`
FROM
    `images` AS `a`,
    `images` AS `b`
WHERE
    -- IMPORTANT: Ensures one version remains
    -- Change "ID" to your unique column's name
    `a`.`movieID` < `b`.`movieID`

    -- Any duplicates you want to check for
    AND `a`.`name` <=> `b`.`name`;
    
SELECT * FROM images;

