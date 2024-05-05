CREATE TABLE main.imd_band (
    id SERIAL PRIMARY KEY,
    imd_band VARCHAR(7) NOT NULL
);
INSERT INTO main.imd_band (imd_band)
SELECT DISTINCT imd_band
FROM staging."studentInfo"
WHERE imd_band IS NOT null
ORDER BY imd_band;
