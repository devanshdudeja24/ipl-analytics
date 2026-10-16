-- 1. Wins by team
SELECT winner, COUNT(*) AS wins
FROM matches
GROUP BY winner
ORDER BY wins DESC;

-- 2. Toss impact by decision
SELECT toss_decision,
       COUNT(*) AS matches,
       ROUND(100.0 * SUM(toss_winner = winner) / COUNT(*), 1) AS toss_winner_win_pct
FROM matches
GROUP BY toss_decision;

-- 3. Top 10 batters
SELECT batter, SUM(batsman_runs) AS runs
FROM deliveries
GROUP BY batter
ORDER BY runs DESC
LIMIT 10;

-- 4. Chasing team win % at each venue
SELECT m.venue,
       COUNT(*) AS matches,
       ROUND(100.0 * SUM(m.winner = d.batting_team) / COUNT(*), 1) AS chase_win_pct
FROM matches m
JOIN (SELECT DISTINCT match_id, batting_team
      FROM deliveries WHERE inning = 2) d
  ON m.id = d.match_id
GROUP BY m.venue
ORDER BY chase_win_pct DESC;

-- 5. Average first-innings score per season
SELECT m.season, ROUND(AVG(s.total), 1) AS avg_first_innings_score
FROM matches m
JOIN (SELECT match_id, SUM(total_runs) AS total
      FROM deliveries WHERE inning = 1
      GROUP BY match_id) s
  ON m.id = s.match_id
GROUP BY m.season
ORDER BY m.season;