-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： db
-- 產生時間： 2024 年 08 月 15 日 16:52
-- 伺服器版本： 11.4.3-MariaDB-ubu2404
-- PHP 版本： 8.2.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `counter_db`
--

-- --------------------------------------------------------

--
-- 資料表結構 `match_info`
--

CREATE TABLE `match_info` (
  `level` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `red1` char(8) NOT NULL,
  `red2` char(8) NOT NULL,
  `blue1` char(8) NOT NULL,
  `blue2` char(8) NOT NULL,
  `state` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- 傾印資料表的資料 `match_info`
--

INSERT INTO `match_info` (`level`, `id`, `red1`, `red2`, `blue1`, `blue2`, `state`) VALUES
(0, 1, '6998-1', '6998-3', '8020-2', '6998-2', 6),
(0, 3, '6998-1', '8020', '6998-1', '4554', 3),
(0, 7, '5454', '7788', '2323', '4444', 0),
(1, 2, '6998-2', '8020-1', '9126', '6998-2', 0),
(1, 6, '77889', '8223', '9126', '1111', 0),
(1, 8, '98-2', '8020-1', '9126', '6998-2', 0),
(2, 1, '6998-1', '6998-3', '8020-2', '6998-2', 0),
(2, 2, '6998-2', '8020-1', '9126', '6998-2', 0),
(2, 3, '6998-1', '8020', '6998-1', '4554', 0),
(2, 6, '77889', '8223', '9126', '1111', 0),
(2, 7, '5454', '7788', '2323', '4444', 0),
(2, 8, '98-2', '8020-1', '9126', '6998-2', 0);

-- --------------------------------------------------------

--
-- 資料表結構 `match_result`
--

CREATE TABLE `match_result` (
  `match-level` int(11) NOT NULL,
  `match-id` int(11) NOT NULL,
  `red-team1` char(8) NOT NULL,
  `blue-team1` char(8) NOT NULL,
  `red-team2` char(8) NOT NULL,
  `blue-team2` char(8) NOT NULL,
  `red-total-score-with-penalty` int(11) NOT NULL,
  `blue-total-score-with-penalty` int(11) NOT NULL,
  `red-melody` tinyint(1) NOT NULL,
  `blue-melody` tinyint(1) NOT NULL,
  `red-melody-demand` int(11) NOT NULL,
  `blue-melody-demand` int(11) NOT NULL,
  `red-ensemble` tinyint(1) NOT NULL,
  `blue-ensemble` tinyint(1) NOT NULL,
  `red-ensemble-demand` int(11) NOT NULL,
  `blue-ensemble-demand` int(11) NOT NULL,
  `winner` char(4) NOT NULL,
  `red-auto-leave1` int(11) NOT NULL,
  `blue-auto-leave1` int(11) NOT NULL,
  `red-auto-leave2` int(11) NOT NULL,
  `blue-auto-leave2` int(11) NOT NULL,
  `red-auto-leavePoints` int(11) NOT NULL,
  `blue-auto-leavePoints` int(11) NOT NULL,
  `red-auto-speaker` int(11) NOT NULL,
  `blue-auto-speaker` int(11) NOT NULL,
  `red-auto-echo` int(11) NOT NULL,
  `blue-auto-echo` int(11) NOT NULL,
  `red-auto-foul` int(11) NOT NULL,
  `blue-auto-foul` int(11) NOT NULL,
  `red-auto-techFoul` int(11) NOT NULL,
  `blue-auto-techFoul` int(11) NOT NULL,
  `red-auto-total-point` int(11) NOT NULL,
  `blue-auto-total-point` int(11) NOT NULL,
  `red-telop-speaker` int(11) NOT NULL,
  `blue-telop-speaker` int(11) NOT NULL,
  `red-telop-echo` int(11) NOT NULL,
  `blue-telop-echo` int(11) NOT NULL,
  `red-telop-fortissimo` int(11) NOT NULL,
  `blue-telop-fortissimo` int(11) NOT NULL,
  `red-telop-foul` int(11) NOT NULL,
  `blue-telop-foul` int(11) NOT NULL,
  `red-telop-techFoul` int(11) NOT NULL,
  `blue-telop-techFoul` int(11) NOT NULL,
  `red-telop-park1` int(11) NOT NULL,
  `blue-telop-park1` int(11) NOT NULL,
  `red-telop-park2` int(11) NOT NULL,
  `blue-telop-park2` int(11) NOT NULL,
  `red-telop-stagePoints` int(11) NOT NULL,
  `blue-telop-stagePoints` int(11) NOT NULL,
  `red-telop-total-point` int(11) NOT NULL,
  `blue-telop-total-point` int(11) NOT NULL,
  `red-total-score` int(11) NOT NULL,
  `blue-total-score` int(11) NOT NULL,
  `red-total-penalty` int(11) NOT NULL,
  `blue-total-penalty` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- 傾印資料表的資料 `match_result`
--

INSERT INTO `match_result` (`match-level`, `match-id`, `red-team1`, `blue-team1`, `red-team2`, `blue-team2`, `red-total-score-with-penalty`, `blue-total-score-with-penalty`, `red-melody`, `blue-melody`, `red-melody-demand`, `blue-melody-demand`, `red-ensemble`, `blue-ensemble`, `red-ensemble-demand`, `blue-ensemble-demand`, `winner`, `red-auto-leave1`, `blue-auto-leave1`, `red-auto-leave2`, `blue-auto-leave2`, `red-auto-leavePoints`, `blue-auto-leavePoints`, `red-auto-speaker`, `blue-auto-speaker`, `red-auto-echo`, `blue-auto-echo`, `red-auto-foul`, `blue-auto-foul`, `red-auto-techFoul`, `blue-auto-techFoul`, `red-auto-total-point`, `blue-auto-total-point`, `red-telop-speaker`, `blue-telop-speaker`, `red-telop-echo`, `blue-telop-echo`, `red-telop-fortissimo`, `blue-telop-fortissimo`, `red-telop-foul`, `blue-telop-foul`, `red-telop-techFoul`, `blue-telop-techFoul`, `red-telop-park1`, `blue-telop-park1`, `red-telop-park2`, `blue-telop-park2`, `red-telop-stagePoints`, `blue-telop-stagePoints`, `red-telop-total-point`, `blue-telop-total-point`, `red-total-score`, `blue-total-score`, `red-total-penalty`, `blue-total-penalty`) VALUES
(0, 3, '6998-1', '6998-1', '8020', '4554', 8, 0, 0, 0, 0, 0, 0, 0, 8, 0, 'red', 2, 0, 1, 0, 8, 0, 0, 0, 0, 0, 2, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0);

-- --------------------------------------------------------

--
-- 資料表結構 `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` char(20) NOT NULL,
  `password` char(20) NOT NULL,
  `role` int(11) NOT NULL,
  `alliance` char(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- 傾印資料表的資料 `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`, `alliance`) VALUES
(1, 'r1', '1', 1, 'red'),
(2, 'r2', '1', 1, 'red'),
(3, 'b1', '1', 1, 'blue'),
(4, 'b2', '1', 1, 'blue'),
(5, 'admin', 'admin', 0, '');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `match_info`
--
ALTER TABLE `match_info`
  ADD PRIMARY KEY (`level`,`id`);

--
-- 資料表索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
