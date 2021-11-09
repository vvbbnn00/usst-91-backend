# usst-91-backend
USST就业日历轻应用后端

## 关于环境安装

### 需要在本地配置的数据库服务器
- mysql(>=5.6)

#### Mysql数据库配置
```sql
# Host: localhost  (Version: 5.5.47)
# Date: 2021-11-07 13:17:25

/*!40101 SET NAMES utf8 */;

#
# Structure for table "meet_list"
#

DROP TABLE IF EXISTS `meet_list`;
CREATE TABLE `meet_list` (
  `Id` bigint(20) NOT NULL AUTO_INCREMENT,
  `MeetID` varchar(255) NOT NULL DEFAULT '',
  `MeetName` varchar(255) NOT NULL DEFAULT '',
  `MeetStart` varchar(255) NOT NULL DEFAULT '',
  `MeetEnd` varchar(255) NOT NULL DEFAULT '',
  `MeetAddress` varchar(255) NOT NULL DEFAULT '',
  `AppStart` varchar(255) NOT NULL DEFAULT '',
  `AppEnd` varchar(255) NOT NULL DEFAULT '',
  `update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `MeetID` (`MeetID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=gbk COMMENT='招聘会缓存数据';

DROP TABLE IF EXISTS `recruitment_list`;
CREATE TABLE `recruitment_list` (
  `Id` bigint(20) NOT NULL AUTO_INCREMENT,
  `AppID` int(11) NOT NULL DEFAULT '0',
  `SequenceNumber` varchar(255) NOT NULL DEFAULT '',
  `EntName` varchar(255) NOT NULL DEFAULT '',
  `Address` varchar(255) NOT NULL DEFAULT '',
  `HostVenue` varchar(255) NOT NULL DEFAULT '',
  `ScheduledDate` varchar(255) NOT NULL DEFAULT '',
  `ScheduledDateS` varchar(255) NOT NULL DEFAULT '',
  `ScheduledDateE` varchar(255) NOT NULL DEFAULT '',
  `update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '校对日期',
  PRIMARY KEY (`Id`),
  UNIQUE KEY `AppID` (`AppID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=gbk COMMENT='宣讲会缓存数据';

DROP TABLE IF EXISTS `subscription_list`;
CREATE TABLE `subscription_list` (
  `Id` bigint(20) NOT NULL AUTO_INCREMENT,
  `welink_id` varchar(255) NOT NULL DEFAULT '' COMMENT '订阅用户的welinkID',
  `sub_type` int(11) NOT NULL DEFAULT '0' COMMENT '订阅类型 0-宣讲会 1-招聘会',
  `sub_id` varchar(255) NOT NULL DEFAULT '' COMMENT '订阅条目ID',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '当前状态 0-已订阅 1-订阅已取消',
  `calendar_id` varchar(255) NOT NULL DEFAULT '' COMMENT 'welink日历id',
  PRIMARY KEY (`Id`),
  KEY `1` (`welink_id`,`sub_type`),
  KEY `2` (`sub_type`,`sub_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=gbk COMMENT='用户订阅记录';

```

- redis

### 远程数据库
- mssql 2014
关于远程数据库连接的问题，请参照[微软官方文档](https://docs.microsoft.com/zh-cn/sql/connect/python/pyodbc/python-sql-driver-pyodbc?view=sql-server-ver15)

