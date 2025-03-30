CREATE TABLE IF NOT EXISTS `job_titles` (
	`id_job_title` integer primary key NOT NULL UNIQUE,
	`name` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `employees` (
	`id` integer primary key NOT NULL UNIQUE,
	`surname` TEXT NOT NULL,
	`name` TEXT NOT NULL,
	`id_job` INTEGER NOT NULL,
FOREIGN KEY(`id_job`) REFERENCES `job_titles`(`id_job_title`)
);
CREATE TABLE IF NOT EXISTS `orders` (
	`id_order` integer primary key NOT NULL UNIQUE,
	`id_customer` INTEGER NOT NULL,
	`id_employee` INTEGER NOT NULL,
	`sum` INTEGER NOT NULL,
	`order_date` REAL NOT NULL,
	`status` TEXT NOT NULL,
FOREIGN KEY(`id_customer`) REFERENCES `customers`(`id`),
FOREIGN KEY(`id_employee`) REFERENCES `employees`(`id`)
);
CREATE TABLE IF NOT EXISTS `customers` (
	`id` integer primary key NOT NULL UNIQUE,
	`company` TEXT NOT NULL,
	`phone_number` TEXT NOT NULL
);