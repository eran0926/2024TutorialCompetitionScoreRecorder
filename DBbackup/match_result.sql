-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： db
-- 產生時間： 2024 年 08 月 15 日 13:58
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
-- 資料表結構 `match_result`
--

CREATE TABLE `match_result` (
  `match-level` int(11) NOT NULL,
  `match-id` int(11) NOT NULL,
  `red-team1` char(8) NOT NULL,
  `blue-team1` char(8) NOT NULL,
  `red-team2` char(8) NOT NULL,
  `blue-team2` char(8) NOT NULL,
  `red-total-point` int(11) NOT NULL,
  `blue-total-point` int(11) NOT NULL,
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
  `red-total-penalty` int(11) NOT NULL,
  `blue-total-penalty` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
