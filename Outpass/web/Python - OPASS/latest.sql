/*
SQLyog Ultimate v11.11 (64 bit)
MySQL - 5.5.5-10.4.27-MariaDB : Database - opass
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`opass` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;

USE `opass`;

/*Table structure for table `batches` */

DROP TABLE IF EXISTS `batches`;

CREATE TABLE `batches` (
  `batch_id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) DEFAULT NULL,
  `start_year` varchar(100) DEFAULT NULL,
  `end_year` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`batch_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `batches` */

insert  into `batches`(`batch_id`,`course_id`,`start_year`,`end_year`) values (1,1,'2019-06-06','2023-06-06'),(2,1,'2020-06-06','2024-09-06'),(3,2,'2020-08-08','2022-08-08');

/*Table structure for table `courses` */

DROP TABLE IF EXISTS `courses`;

CREATE TABLE `courses` (
  `course_id` int(11) NOT NULL AUTO_INCREMENT,
  `dept_id` int(11) DEFAULT NULL,
  `course_name` varchar(100) DEFAULT NULL,
  `duration` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `courses` */

insert  into `courses`(`course_id`,`dept_id`,`course_name`,`duration`) values (1,1,'B TECH ','4'),(2,6,'MCA','2'),(3,6,'INMCA','5');

/*Table structure for table `department` */

DROP TABLE IF EXISTS `department`;

CREATE TABLE `department` (
  `dept_id` int(15) NOT NULL AUTO_INCREMENT,
  `department` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`dept_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `department` */

insert  into `department`(`dept_id`,`department`) values (1,'Computer Science Engineering'),(2,'Electronics and communication '),(3,'Electrical and Electroncis'),(4,'Civil Engineering'),(5,'Mechanical Engineering'),(6,'Computer Science');

/*Table structure for table `guest` */

DROP TABLE IF EXISTS `guest`;

CREATE TABLE `guest` (
  `guest_id` int(11) NOT NULL AUTO_INCREMENT,
  `warden_id` int(11) DEFAULT NULL,
  `room_id` varchar(100) DEFAULT NULL,
  `guest` varchar(100) DEFAULT NULL,
  `noofdays` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`guest_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `guest` */

insert  into `guest`(`guest_id`,`warden_id`,`room_id`,`guest`,`noofdays`,`date`,`status`) values (2,1,'1','hei','3','2023-03-12','pending');

/*Table structure for table `hod` */

DROP TABLE IF EXISTS `hod`;

CREATE TABLE `hod` (
  `hod_id` int(15) NOT NULL AUTO_INCREMENT,
  `login_id` int(15) DEFAULT NULL,
  `dept_id` int(15) DEFAULT NULL,
  `fname` varchar(50) DEFAULT NULL,
  `lname` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`hod_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `hod` */

insert  into `hod`(`hod_id`,`login_id`,`dept_id`,`fname`,`lname`,`place`,`phone`,`email`) values (1,65,6,'Kavitha','C R','Ernakulam','6787675676','kavitha@gmail.com');

/*Table structure for table `hostels` */

DROP TABLE IF EXISTS `hostels`;

CREATE TABLE `hostels` (
  `hostel_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `landmark` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`hostel_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `hostels` */

insert  into `hostels`(`hostel_id`,`name`,`place`,`landmark`,`phone`,`email`) values (1,'mary queens','karikkamuri','ymca','7998675643','queens@gmail.com'),(3,'fdgvhj','vbnm','fghjk','5676767787','anjijose91@gmail.com');

/*Table structure for table `late_coming` */

DROP TABLE IF EXISTS `late_coming`;

CREATE TABLE `late_coming` (
  `late_coming_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) DEFAULT NULL,
  `date_time` varchar(100) DEFAULT NULL,
  `late_by` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`late_coming_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `late_coming` */

insert  into `late_coming`(`late_coming_id`,`student_id`,`date_time`,`late_by`) values (1,1,'2022-06-30 10:32:16','5min');

/*Table structure for table `leave_requests` */

DROP TABLE IF EXISTS `leave_requests`;

CREATE TABLE `leave_requests` (
  `leave_id` int(11) NOT NULL AUTO_INCREMENT,
  `requested_id` int(11) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `reason` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `duration` varchar(100) DEFAULT NULL,
  `date_time` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `qr` varchar(500) DEFAULT NULL,
  `leave_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`leave_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `leave_requests` */

insert  into `leave_requests`(`leave_id`,`requested_id`,`type`,`reason`,`date`,`duration`,`date_time`,`status`,`qr`,`leave_type`) values (1,67,'student','fever','2022-06-30','5','2022-06-30 10:01:55','accepted','static/qrcode/33f1e28c-0aeb-40df-82e4-7c11fb9e4ca2.png',''),(2,67,'student','fever','2022-06-30','5','2022-06-30 10:01:55','pending','pending',''),(3,66,'teacher','fever','2022-06-30','5','2022-06-30 10:12:39','principal approved teacher leave','pending','pending'),(4,67,'student','mrg','2022-06-30','2','2022-06-30 10:23:51','teacher approved student leave','static/qrcode/af19ecdb-b5c5-4804-9464-a3e8d249eff0.png','');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=73 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values (1,'admin','admin','admin'),(54,'rsehmi','reshmi123','student'),(3,'jacob','jacob123','guard'),(4,'koshi','koshi@gmail.com','guard'),(5,'guard','guard','guard'),(6,'hema','hema123','warden'),(11,'a','a','student'),(9,'mary','mary123','teacher'),(14,'bvgdvyu','fyhi','principal'),(15,'asdr','g hj','principal'),(16,'asdr','vb','principal'),(17,'asdr','vb','principal'),(18,'asdr','vb','principal'),(19,'123se','123er','principal'),(20,'123se','123er','principal'),(27,'anj','123','guard'),(22,'12345','2345','principal'),(23,'john','wert','principal'),(51,'anji123','anji','teacher'),(25,'pk1234','pk@123','guard'),(26,'gbnghg','ghny','guard'),(28,'dtfygh','ty','guard'),(31,'shameer123','123skr','hod'),(32,'abcd','123abcd','hod'),(33,'dxfghj123','123','hod'),(34,'bhn123','123ert','hod'),(35,'srtct123','gvhvhy','hod'),(36,'vhvh@gmail.com','sdertyu','hod'),(37,'anji','fff','hod'),(53,'thrishna123','thrish','student'),(39,'fg123','asd','teacher'),(40,'fg123','asd','teacher'),(41,'anji123','anji','teacher'),(42,'anji123','anji','teacher'),(43,'anji123','anji','teacher'),(44,'gbnhk123','gbnk','teacher'),(45,'gbnhk123','gbnk','teacher'),(46,'fcgh','dfgh','teacher'),(47,'vvvv','mmm','teacher'),(48,'ffffff','vvvvvv','teacher'),(49,'sajini123','saji123','principal'),(52,'swd','345','hod'),(55,'cuppy','cuppy123','student'),(56,'thrisg','123thris','student'),(57,'anji123344','dzfgyui','student'),(58,'df','fv','student'),(59,'aswathi123','aswathi','teacher'),(60,'rose123','rose','student'),(61,'aswin123','aswin','student'),(62,'aswathi','ASSR','principal'),(63,'reashma123','reasg','teacher'),(64,'sagini123','sagini123','principal'),(65,'kavitha123','kavitha123','hod'),(66,'tintu123','tintu123','teacher'),(67,'anji123','anji123','student'),(68,'hbh','h h','student'),(69,'admin','dsa','teacher'),(70,'admin','dsa','teacher'),(71,'tc','tc','teacher'),(72,'user','user','student');

/*Table structure for table `messages` */

DROP TABLE IF EXISTS `messages`;

CREATE TABLE `messages` (
  `message_id` int(11) NOT NULL AUTO_INCREMENT,
  `guard_id` int(11) DEFAULT NULL,
  `student_id` int(11) DEFAULT NULL,
  `reciever_id` int(11) DEFAULT NULL,
  `reciever_type` varchar(100) DEFAULT NULL,
  `message` varchar(100) DEFAULT NULL,
  `date_time` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`message_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `messages` */

insert  into `messages`(`message_id`,`guard_id`,`student_id`,`reciever_id`,`reciever_type`,`message`,`date_time`) values (1,1,1,1,'warden','szxh','2021-05-15 22:39:11'),(2,1,3,1,'warden','sdfgvhj','2021-05-15 22:43:33');

/*Table structure for table `out_passes` */

DROP TABLE IF EXISTS `out_passes`;

CREATE TABLE `out_passes` (
  `pass_id` int(11) NOT NULL AUTO_INCREMENT,
  `requested_id` int(11) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `request_date` varchar(100) DEFAULT NULL,
  `request_time` varchar(100) DEFAULT NULL,
  `reason` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `qr` varchar(500) DEFAULT NULL,
  `return_time` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`pass_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `out_passes` */

insert  into `out_passes`(`pass_id`,`requested_id`,`type`,`request_date`,`request_time`,`reason`,`status`,`qr`,`return_time`) values (1,66,'teacher','2022-06-29','12:18:30','fever','principal approved teacher outpass',NULL,'11:19'),(2,66,'teacher','2022-06-29','14:18:50','fever','principal approved teacher outpass','static/qrcode/da871691-ba6e-4a6a-9843-7f44e95c217b.png','15:24'),(3,66,'teacher','2022-06-30','3:15','mrg','pending','pending','pending'),(4,66,'teacher','2022-06-30','3:15','mrg','pending','pending','pending'),(5,66,'teacher','2022-06-30','3:15','mrg','pending','pending','pending'),(6,66,'teacher','2022-06-30','3:15','mrg','pending','pending','pending'),(7,66,'teacher','2022-06-30','4:0','pain','pending','pending','pending'),(8,66,'teacher','2022-06-30','3:0','pain','pending','pending','pending'),(9,67,'student','2022-06-30','15:0','home','accepted','static/qrcode/a49cc5a4-2272-473b-9bda-f9688ff7599f.png',''),(10,72,'student','2023-02-17','2:15','chumma','pending','pending','pending');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `request_id` int(11) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `payment` */

insert  into `payment`(`payment_id`,`request_id`,`amount`,`date`) values (1,4,'20000','2023-02-03'),(2,3,'100','2023-02-03');

/*Table structure for table `principal` */

DROP TABLE IF EXISTS `principal`;

CREATE TABLE `principal` (
  `principal_id` int(15) NOT NULL AUTO_INCREMENT,
  `login_id` int(15) DEFAULT NULL,
  `fname` varchar(50) DEFAULT NULL,
  `lname` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`principal_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `principal` */

insert  into `principal`(`principal_id`,`login_id`,`fname`,`lname`,`place`,`phone`,`email`) values (1,64,'Dr sagini','Thomas Mathai','Ernakulam','8767675645','sagini@gmail.com');

/*Table structure for table `request` */

DROP TABLE IF EXISTS `request`;

CREATE TABLE `request` (
  `request_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) DEFAULT NULL,
  `requested_for` varchar(100) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `formonth` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `request` */

insert  into `request`(`request_id`,`student_id`,`requested_for`,`amount`,`date`,`formonth`,`status`) values (1,1,'mess','500','23/08/2001','10','pending'),(2,1,'room','5000','23/08/2001','10','pending'),(3,3,'mess','100','2023-02-26','12','Payment Completed'),(4,3,'room','20000','2023-03-02','24','Payment Completed');

/*Table structure for table `rooms` */

DROP TABLE IF EXISTS `rooms`;

CREATE TABLE `rooms` (
  `room_id` int(11) NOT NULL AUTO_INCREMENT,
  `room_no` varchar(100) DEFAULT NULL,
  `hostel_id` int(11) DEFAULT NULL,
  `capacity` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`room_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `rooms` */

insert  into `rooms`(`room_id`,`room_no`,`hostel_id`,`capacity`) values (1,'1A',1,'4'),(2,'1B',1,'5'),(3,'1C',1,'8');

/*Table structure for table `security_guards` */

DROP TABLE IF EXISTS `security_guards`;

CREATE TABLE `security_guards` (
  `guard_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `house_name` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`guard_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `security_guards` */

insert  into `security_guards`(`guard_id`,`login_id`,`first_name`,`last_name`,`house_name`,`place`,`phone`,`email`) values (1,3,'jacob','p','ery','kottayam','7998675643','jacob@gmail.com'),(2,4,'koshi','k','kayathil','kollam','9876546756','koshi@gmail.com'),(4,25,'pk','h','ghj','vbnj','5678789878','pk@gmail.com'),(5,26,'wertfgg','xzfg','gb','gnh','5678765676','ert@gmail.com');

/*Table structure for table `student_rooms` */

DROP TABLE IF EXISTS `student_rooms`;

CREATE TABLE `student_rooms` (
  `student_room_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `assigned_date` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`student_room_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `student_rooms` */

insert  into `student_rooms`(`student_room_id`,`student_id`,`room_id`,`assigned_date`,`status`) values (1,1,2,'2021-05-14','assigned'),(2,3,3,'2021-05-16','assigned'),(3,1,2,'2022-06-23','assigned'),(4,1,1,'2022-06-24','assigned'),(5,1,2,'2023-02-02','assigned');

/*Table structure for table `students` */

DROP TABLE IF EXISTS `students`;

CREATE TABLE `students` (
  `student_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `batch_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `house_name` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `parent_email` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `hostel` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`student_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `students` */

insert  into `students`(`student_id`,`login_id`,`batch_id`,`course_id`,`first_name`,`last_name`,`house_name`,`place`,`parent_email`,`phone`,`email`,`hostel`) values (1,67,3,2,'anji','jose','UKKURU','thrissur','anjijose91@gmail.com','9847571534','anjijose91@gmail','Yes'),(2,68,1,1,'hj','b ','hhj','bjj','anjijose91@gmail.com','8767857675','anjijose91@gmail.com','Yes'),(3,72,2,2,'anandhu','saas','nearthammanamjunction','alpy','sankusanku001@gmail.com','6238526459','sankusanku001@gmail.com','Yes');

/*Table structure for table `teachers` */

DROP TABLE IF EXISTS `teachers`;

CREATE TABLE `teachers` (
  `teacher_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `batch_id` int(11) DEFAULT NULL,
  `hod_id` int(11) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `house_name` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`teacher_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `teachers` */

insert  into `teachers`(`teacher_id`,`login_id`,`batch_id`,`hod_id`,`first_name`,`last_name`,`house_name`,`place`,`phone`,`email`) values (1,66,NULL,1,'Tintu','P B','erkl','manjali','8767676765','anjijose91@gmail.com'),(2,70,1,NULL,'san','kar','ssssssssssssssssss','kochi','6238526459','safasfssfd@gmail.com'),(3,71,3,NULL,'anandhu','saas','nearthammanamjunction','kochi','6238526459','sankusanku001@gmail.com');

/*Table structure for table `wardens` */

DROP TABLE IF EXISTS `wardens`;

CREATE TABLE `wardens` (
  `warden_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `hostel_id` int(11) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `house_name` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`warden_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `wardens` */

insert  into `wardens`(`warden_id`,`login_id`,`hostel_id`,`first_name`,`last_name`,`house_name`,`place`,`phone`,`email`) values (1,6,1,'hema','s','nest','kannur','9857645432','hema@gmail.com');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
