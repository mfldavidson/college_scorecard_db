# Questions
The questions I posed for myself to answer were:

1. Which city has the most institutions, and how many does it have? If there is a tie, I only need to see one.
1. What are the average earnings for each control?
1. What is the average cost and average family income for each level?
1. Which region has the highest average share of first generation students attending its institutions? Which has the lowest? Please include the share of first generation students as well with each.
1. Which institution has the largest share of first generation students? Please give me the share as well as the institution’s name, city, state (abbreviated), region, control, level, mean earnings, mean family income, and mean cost. If there is a tie, I only need to see one.
1. Which institutional control has the highest mean family income, and what is that income? How much higher is it than the next closest?
1. Which region has the largest share of private for-profit institutions (compared to other types of controls)?
1. Please give me the name, city, and state (full name, not abbreviated) of the top 5 institutions by mean earnings which also meet the following criteria:
    - Over 50% first generation students
    - Mean cost is less than $10,000
1. Please give me the name and level of the 5 institutions with the highest mean cost.
1. Which region has the highest mean earnings? Which state?

### 1. Which city has the most institutions, and how many does it have?

```buildoutcfg
SELECT city, abbr_state, COUNT(city) FROM institutions
LEFT JOIN states ON states.state_id = institutions.state_id
GROUP BY institutions.state_id, city 
ORDER BY COUNT(city) DESC LIMIT 1;
```

_Answer:_ New York, NY with 94 institutions

### 2. What are the average earnings for each control?

```buildoutcfg
SELECT control AS 'Control', AVG(mean_earn) AS 'Average Earnings'
FROM institutions i
LEFT JOIN controls c ON c.control_id = i.control_id
GROUP BY i.control_id;
```

| Control            | Average Earnings |
|--------------------|------------------|
| Public             |       40593.2840 |
| Private nonprofit  |       49404.9698 |
| Private for-profit |       31195.1763 |

### 3. What is the average cost and average family income for each level?

```buildoutcfg
SELECT 
    level AS 'Level', 
    AVG(mean_cost) as 'Average Cost', 
    AVG(family_inc) AS 'Average Family Income'
FROM institutions i
LEFT JOIN levels l ON l.level_id = i.level_id
GROUP BY i.level_id;
```

| Level            | Average Cost | Average Family Income |
|------------------|--------------|-----------------------|
| 4-year           |   14759.5241 |          49160.962502 |
| 2-year           |   11569.9270 |          27359.161760 |
| Less-than-2-year |   13247.2743 |          23700.872962 |

### 4a. Which region has the highest average share of first generation students attending its institutions? 

```buildoutcfg
SELECT 
    region AS 'Region', 
    AVG(first_gen) as 'Average Share of First Gen Students'
FROM states s
LEFT JOIN institutions i ON i.state_id = s.state_id
GROUP BY s.region ORDER BY AVG(first_gen) DESC LIMIT 1;
```

_Answer:_ Southwest, with an average share of 50.7%

### 4b. Which has the lowest? 

```buildoutcfg
SELECT 
    region AS 'Region', 
    AVG(first_gen) as 'Average Share of First Gen Students'
FROM states s
LEFT JOIN institutions i ON i.state_id = s.state_id
GROUP BY s.region ORDER BY AVG(first_gen) ASC LIMIT 1;
```

_Answer:_ Plains, with an average share of 40.2%

### 5. Which institution has the largest share of first generation students? 

```buildoutcfg
SELECT 
    i.name AS 'Institution', 
    i.first_gen AS 'Share of First Gen Students',
    i.city AS 'City',
    s.abbr_state AS 'State',
    s.region AS 'Region',
    c.control AS 'Control',
    l.level AS 'Level',
    i.mean_earn AS 'Mean Earnings',
    i.family_inc AS 'Mean Family Income',
    i.mean_cost AS 'Mean Net Cost'
FROM institutions i
LEFT JOIN states s ON s.state_id = i.state_id
LEFT JOIN controls c ON c.control_id = i.control_id
LEFT JOIN levels l ON l.level_id = i.level_id
ORDER BY i.first_gen DESC LIMIT 1;
```

| Institution                         | Share of First Gen Students | City      | State | Region    | Control            | Level            | Mean Earnings | Mean Family Income | Mean Net Cost |
|-------------------------------------|-----------------------------|-----------|-------|-----------|--------------------|------------------|---------------|--------------------|---------------|
| Cosmopolitan Beauty and Tech School |                        0.93 | Annandale | VA    | Southeast | Private for-profit | Less-than-2-year |          NULL |           18081.19 |          3052 |

### 6a. Which institutional control has the highest mean family income, and what is that income?

```buildoutcfg
SELECT 
    c.control AS 'Control', 
    AVG(family_inc) AS 'Average Family Income'
FROM controls c
LEFT JOIN institutions i ON i.control_id = c.control_id
GROUP BY c.control_id ORDER BY AVG(family_inc) DESC LIMIT 1;
```

_Answer:_ Private nonprofit, with an average family income of $55,281.27

### 6b. How much higher is it than the next closest?

```buildoutcfg
SELECT 
    h.highest - l.lowest
FROM (
    SELECT AVG(i.family_inc) as 'highest'
    FROM institutions i
    GROUP BY i.control_id 
    ORDER BY AVG(family_inc) DESC LIMIT 1
) h
, (
    SELECT AVG(i.family_inc) as 'lowest'
    FROM institutions i
    GROUP BY i.control_id 
    ORDER BY AVG(family_inc) ASC LIMIT 1
) l;
```

_Answer:_ $30,495.58 higher than the next closest

### 7. Which region has the largest share of private for-profit institutions (compared to other types of controls)?

```buildoutcfg
SELECT 
    s.region AS 'Region', 
    COUNT(CASE WHEN i.control_id = 3 THEN 1 END) / 
        COUNT(1) AS 'Share of Private For-Profit'
FROM institutions i
LEFT JOIN states s ON s.state_id = i.state_id
GROUP BY s.region 
ORDER BY COUNT(CASE WHEN i.control_id = 3 THEN 1 END) / 
        COUNT(1) DESC LIMIT 1;
```

_Answer:_ Rocky Mountains with 57.95% of its institutions being private for-profit.

### 8. Please give me the name, city, and state of the top 5 institutions by mean earnings.

```buildoutcfg
SELECT 
    i.name AS 'Institution',
    i.city AS 'City',
    s.long_state AS 'State',
    i.mean_earn AS 'Mean Earnings'
FROM institutions i
LEFT JOIN states s ON s.state_id = i.state_id
WHERE i.first_gen > 0.5 AND mean_cost < 10000
ORDER BY i.mean_earn DESC LIMIT 5;
```

| Institution                                             | City         | State         | Mean Earnings |
|---------------------------------------------------------|--------------|---------------|---------------|
| Los Angeles County College of Nursing and Allied Health | Los Angeles  | California    |         84800 |
| American Public University System                       | Charles Town | West Virginia |         67000 |
| Citizens School of Nursing                              | Tarentum     | Pennsylvania  |         59600 |
| Los Angeles Center                                      | Los Angeles  | California    |         55000 |
| Florida Center                                          | Hollywood    | Florida       |         55000 |

### 9. Please give me the name and level of the 5 institutions with the highest mean cost.

```buildoutcfg
SELECT 
    i.name AS 'Institution',
    l.level AS 'Level',
    i.mean_cost AS 'Mean Cost'
FROM institutions i
LEFT JOIN levels l ON l.level_id = i.level_id
ORDER BY i.mean_cost DESC LIMIT 5;
```

| Institution                                            | Level            | Mean Cost |
|--------------------------------------------------------|------------------|-----------|
| L3 Commercial Training Solutions Airline Academy       | Less-than-2-year |     89406 |
| Aviator College of Aeronautical Science and Technology | 2-year           |     77100 |
| Hallmark Institute of Photography                      | Less-than-2-year |     74673 |
| The International Culinary Center                      | Less-than-2-year |     58271 |
| First Coast Barber Academy                             | Less-than-2-year |     47994 |

### 10a. Which region has the highest mean earnings?

```buildoutcfg
SELECT 
    s.region AS 'Region',
    AVG(i.mean_earn) AS 'Mean Earnings'
FROM states s 
LEFT JOIN institutions i ON i.state_id = s.state_id
GROUP BY s.region ORDER BY AVG(i.mean_earn) DESC LIMIT 1;
```

_Answer:_ New England with mean earnings of $45,672.73

### 10b. Which state?

```buildoutcfg
SELECT 
    s.long_state AS 'State',
    AVG(i.mean_earn) AS 'Mean Earnings'
FROM states s 
LEFT JOIN institutions i ON i.state_id = s.state_id
GROUP BY s.long_state ORDER BY AVG(i.mean_earn) DESC LIMIT 1;
```

_Answer:_ District of Columbia with mean earnings of $55,941.18