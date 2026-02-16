-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-02-2026 a las 13:54:27
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `harryquiz`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preguntas`
--

CREATE TABLE `preguntas` (
  `id` int(11) NOT NULL,
  `texto_pregunta` text NOT NULL,
  `imagen` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `preguntas`
--

INSERT INTO `preguntas` (`id`, `texto_pregunta`, `imagen`) VALUES
(14, '¿Qué objeto cogerías para usar?', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `respuestas`
--

CREATE TABLE `respuestas` (
  `id` int(11) NOT NULL,
  `pregunta_id` int(11) NOT NULL,
  `texto_respuesta` varchar(255) NOT NULL,
  `casa` varchar(20) NOT NULL,
  `imagen` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `respuestas`
--

INSERT INTO `respuestas` (`id`, `pregunta_id`, `texto_respuesta`, `casa`, `imagen`) VALUES
(53, 14, 'Mapa 23232333', 'Gryffindor', 'uploads/c3750a36285c4b28b79dbf908a60845f_0b97f00a7d1a4051b82a049ed686336c_68631b44f416e9f1f4003846_1702250050_WB0019-5.jpg'),
(54, 14, 'Diadema de Ravenclaw2', 'Ravenclaw', 'uploads/d661e8939cf4486195636cb489426cd4_7b35391f189f42aea96a427aaf7371ee_9333de8fa8584561948bd817db8c2a61_diadema-de-rowena-ravenclaw-harry-potter-Zl4TtS3ybQ.jpg'),
(55, 14, 'Anillo Gaunt2', 'Slytherin', 'uploads/ac8befc475b44e42af8fda9ad78a8dc3_2e927260cca14712bad3395d6687f522_images.jpg'),
(56, 14, 'Capa de invisibilidad2', 'Hufflepuff', 'uploads/49f6d672128b48979fef2c1e6ec8395d_UZKOKQRYDJCX3NGF5QI33KD5GU.avif');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `rol` varchar(20) NOT NULL DEFAULT 'usuario',
  `casa` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `password`, `rol`, `casa`) VALUES
(9, 'Eren', NULL, 'usuario', 'Gryffindor'),
(10, 'Eren', NULL, 'usuario', 'Gryffindor'),
(11, 'Eren', NULL, 'usuario', 'Gryffindor'),
(12, 'Eren', NULL, 'usuario', 'Gryffindor'),
(13, 'Eren', NULL, 'usuario', 'Gryffindor'),
(14, 'Eren', NULL, 'usuario', 'Gryffindor'),
(15, 'Eren', NULL, 'usuario', 'Ravenclaw'),
(16, 'Eren', NULL, 'usuario', 'Ravenclaw'),
(17, 'Eren', NULL, 'usuario', 'Slytherin'),
(18, 'Eren', NULL, 'usuario', 'Hufflepuff'),
(19, 'Eren', NULL, 'usuario', 'Slytherin'),
(20, 'Eren', NULL, 'usuario', 'Slytherin'),
(21, 'Eren', NULL, 'usuario', 'Slytherin'),
(22, 'Eren', NULL, 'usuario', 'Slytherin'),
(23, 'Eren', NULL, 'usuario', 'Hufflepuff'),
(24, 'Eren', NULL, 'usuario', 'Slytherin'),
(25, 'Eren', NULL, 'usuario', 'Gryffindor'),
(26, 'Eren', NULL, 'usuario', 'Gryffindor'),
(27, 'Harry', NULL, 'usuario', 'Gryffindor'),
(28, 'admin', '$5$rounds=535000$nOSHwwD/ZIdzNs/n$dPPmf/2/LfxUTvNxWsAkkBEx1D.ojpW1b1q9zdGrAX9', 'admin', NULL),
(29, 'Oscar', NULL, 'usuario', 'Gryffindor'),
(30, 'Eren11', NULL, 'usuario', 'Gryffindor'),
(31, 'Eren11', NULL, 'usuario', 'Gryffindor'),
(32, 'Eren11', NULL, 'usuario', 'Gryffindor'),
(33, 'Eren11', NULL, 'usuario', 'Gryffindor'),
(34, 'Eren11', NULL, 'usuario', 'Gryffindor'),
(35, 'ereno', NULL, 'usuario', 'Gryffindor'),
(36, 'ereno', NULL, 'usuario', 'Gryffindor'),
(37, 'ereno', NULL, 'usuario', 'Gryffindor'),
(38, 'ereno', NULL, 'usuario', 'Gryffindor'),
(39, 'ereno', NULL, 'usuario', 'Gryffindor'),
(40, 'ereno', NULL, 'usuario', 'Gryffindor'),
(41, 'ereno', NULL, 'usuario', 'Gryffindor'),
(42, 'ereno', NULL, 'usuario', 'Gryffindor'),
(43, 'ereno', NULL, 'usuario', 'Gryffindor'),
(44, 'ereno', NULL, 'usuario', 'Gryffindor'),
(45, 'ereno', NULL, 'usuario', 'Gryffindor'),
(46, 'ereno', NULL, 'usuario', 'Gryffindor'),
(47, 'ereno', NULL, 'usuario', 'Gryffindor'),
(48, 'ereno', NULL, 'usuario', 'Gryffindor'),
(49, 'ereno', NULL, 'usuario', 'Gryffindor'),
(50, 'ereb', NULL, 'usuario', 'Gryffindor'),
(51, 'ereb', NULL, 'usuario', 'Gryffindor'),
(52, 'ereb', NULL, 'usuario', 'Gryffindor'),
(53, 'ereb', NULL, 'usuario', 'Gryffindor'),
(54, 'holes', NULL, 'usuario', 'Gryffindor'),
(55, 'rebeca', NULL, 'usuario', 'Slytherin'),
(56, 'ana', NULL, 'usuario', 'Ravenclaw'),
(57, 'Osquer', NULL, 'usuario', 'Gryffindor'),
(58, 'Eren', NULL, 'usuario', 'Hufflepuff'),
(59, 'Harry', NULL, 'usuario', 'Ravenclaw');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `preguntas`
--
ALTER TABLE `preguntas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `respuestas`
--
ALTER TABLE `respuestas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pregunta_id` (`pregunta_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `preguntas`
--
ALTER TABLE `preguntas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `respuestas`
--
ALTER TABLE `respuestas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `respuestas`
--
ALTER TABLE `respuestas`
  ADD CONSTRAINT `respuestas_ibfk_1` FOREIGN KEY (`pregunta_id`) REFERENCES `preguntas` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
