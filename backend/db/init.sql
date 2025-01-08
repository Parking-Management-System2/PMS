DROP TABLE IF EXISTS `activities`;

CREATE TABLE IF NOT EXISTS `activities` (
    `activity_id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `registration_number` TEXT NOT NULL,
    `spot_id` INTEGER,
    `type` TEXT NOT NULL CHECK(type IN ('entrance', 'exit', 'rejected_entrance', 'rejected_exit', 'parked_ok', 'parked_wrong')),
    `timestamp` TEXT NOT NULL
);

-- Insert sample data into the activities table
INSERT INTO `activities` (`registration_number`, `spot_id`, `type`, `timestamp`) VALUES
('ABC123', 1, 'entrance', '2024-12-01 08:00:00'),
('ABC123', 1, 'exit', '2024-12-01 10:00:00'),
('DEF456', 2, 'entrance', '2024-12-01 09:00:00'),
('DEF456', 2, 'exit', '2024-12-01 11:30:00'),
('GHI789', 3, 'entrance', '2024-12-01 10:00:00'),
('GHI789', 3, 'exit', '2024-12-01 12:00:00'),
('JKL012', 5, 'entrance', '2024-12-01 07:30:00'),
('JKL012', 5, 'exit', '2024-12-01 09:45:00'),
('MNO345', 6, 'entrance', '2024-12-01 08:15:00'),
('MNO345', 6, 'exit', '2024-12-01 10:15:00'),
('PQR678', 8, 'entrance', '2024-12-01 06:00:00'),
('PQR678', 8, 'exit', '2024-12-01 08:30:00'),
('STU901', 10, 'entrance', '2024-12-01 09:45:00'),
('STU901', 10, 'exit', '2024-12-01 11:00:00'),
('VWX234', NULL, 'entrance', '2024-12-01 10:30:00'),
('VWX234', NULL, 'exit', '2024-12-01 12:30:00'),
('YZA567', NULL, 'entrance', '2024-12-01 07:00:00'),
('YZA567', NULL, 'exit', '2024-12-01 08:00:00'),
('BCD890', NULL, 'entrance', '2024-12-01 08:30:00'),
('BCD890', NULL, 'exit', '2024-12-01 09:30:00'),
('EFG234', 4, 'entrance', '2024-12-01 07:45:00'),
('EFG234', 4, 'exit', '2024-12-01 09:15:00'),
('HIJ567', 7, 'entrance', '2024-12-01 08:20:00'),
('HIJ567', 7, 'exit', '2024-12-01 10:40:00'),
('LMN890', NULL, 'rejected_entrance', '2024-12-01 13:00:00'),
('OPQ123', NULL, 'rejected_entrance', '2024-12-01 14:00:00'),
('RST456', NULL, 'rejected_exit', '2024-12-01 15:00:00');
