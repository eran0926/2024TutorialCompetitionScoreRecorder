-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： db
-- 產生時間： 2024 年 08 月 14 日 14:21
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
(0, 2, '6998-2', '8020-1', '9126', '6998-2', 0),
(1, 2, '98-2', '8020-1', '9126', '6998-2', 0);

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
(4, 'b2', '1', 1, 'blue');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
