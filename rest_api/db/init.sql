CREATE TABLE IF NOT EXISTS `Cars` (
	`car_id` integer primary key NOT NULL UNIQUE,
	`registration_number` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `Parking_spot` (
	`spot_id` integer primary key NOT NULL UNIQUE,
	`car_id` INTEGER,
	`spot_number` INTEGER NOT NULL,
FOREIGN KEY(`car_id`) REFERENCES `Cars`(`car_id`)
);
CREATE TABLE IF NOT EXISTS `activity` (
	`activity_id` integer primary key NOT NULL UNIQUE,
	`car_id` INTEGER NOT NULL,
	`spot_id` INTEGER NOT NULL,
	`enterance_timestamp` TEXT NOT NULL,
	`leave_timestamp` TEXT NOT NULL,
FOREIGN KEY(`car_id`) REFERENCES `Cars`(`car_id`),
FOREIGN KEY(`spot_id`) REFERENCES `Parking_spot`(`spot_id`)
);