
-- 1. Total number of telemetry records
SELECT COUNT(*) AS total_records
FROM telemetry;


-- 2. Total energy generation and consumption
SELECT
    ROUND(SUM(solar_energy_wh), 2) AS solar_energy_wh,
    ROUND(SUM(load_energy_wh), 2) AS load_energy_wh
FROM telemetry;


-- 3. Battery performance
SELECT
    ROUND(AVG(battery_soc), 2) AS average_soc,
    ROUND(MIN(battery_soc), 2) AS minimum_soc,
    ROUND(MAX(battery_soc), 2) AS maximum_soc
FROM telemetry;


-- 4. Temperature statistics
SELECT
    ROUND(AVG(temperature), 2) AS average_temperature,
    ROUND(MAX(temperature), 2) AS maximum_temperature
FROM telemetry;


-- 5. Telemetry records by solar power level
SELECT
    solar_power,
    COUNT(*) AS measurement_count
FROM telemetry
GROUP BY solar_power
ORDER BY solar_power;
