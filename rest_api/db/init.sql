DROP TABLE IF EXISTS`cars`;
DROP TABLE IF EXISTS`parking_spots`;
DROP TABLE IF EXISTS`activities`;

CREATE TABLE IF NOT EXISTS `cars` (
	`car_id` integer primary key NOT NULL UNIQUE,
	`registration_number` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `parking_spots` (
	`spot_id` integer primary key NOT NULL UNIQUE,
	`car_id` INTEGER,
	`spot_number` INTEGER NOT NULL,
FOREIGN KEY(`car_id`) REFERENCES `cars`(`car_id`)
);

CREATE TABLE IF NOT EXISTS `activities` (
	`activity_id` integer primary key NOT NULL UNIQUE,
	`car_id` INTEGER NOT NULL,
	`spot_id` INTEGER,
	`entrance_timestamp` TEXT NOT NULL,
	`leave_timestamp` TEXT NOT NULL,
FOREIGN KEY(`car_id`) REFERENCES `cars`(`car_id`),
FOREIGN KEY(`spot_id`) REFERENCES `parking_spots`(`spot_id`)
);

-- Insert sample data into Cars table
INSERT INTO `cars` (`car_id`, `registration_number`) VALUES
(1, 'ABC123'),
(2, 'DEF456'),
(3, 'GHI789'),
(4, 'JKL012'),
(5, 'MNO345'),
(6, 'PQR678'),
(7, 'STU901'),
(8, 'VWX234'),
(9, 'YZA567'),
(10, 'BCD890');

-- Insert sample data into Parking_spot table
INSERT INTO `parking_spots` (`spot_id`, `car_id`, `spot_number`) VALUES
(1, 1, 101),
(2, 2, 102),
(3, 3, 103),
(4, NULL, 104),
(5, 4, 105),
(6, 5, 106),
(7, NULL, 107),
(8, 6, 108),
(9, NULL, 109),
(10, 7, 110);

-- Insert sample data into activity table
INSERT INTO `activities` (`activity_id`, `car_id`, `spot_id`, `entrance_timestamp`, `leave_timestamp`) VALUES
(1, 1, 1, '2024-12-01 08:00:00', '2024-12-01 10:00:00'),
(2, 2, 2, '2024-12-01 09:00:00', '2024-12-01 11:30:00'),
(3, 3, 3, '2024-12-01 10:00:00', '2024-12-01 12:00:00'),
(4, 4, 5, '2024-12-01 07:30:00', '2024-12-01 09:45:00'),
(5, 5, 6, '2024-12-01 08:15:00', '2024-12-01 10:15:00'),
(6, 6, 8, '2024-12-01 06:00:00', '2024-12-01 08:30:00'),
(7, 7, 10, '2024-12-01 09:45:00', '2024-12-01 11:00:00'),
(8, 8, NULL, '2024-12-01 10:30:00', '2024-12-01 12:30:00'),
(9, 9, NULL, '2024-12-01 07:00:00', '2024-12-01 08:00:00'),
(10, 10, NULL, '2024-12-01 08:30:00', '2024-12-01 09:30:00');