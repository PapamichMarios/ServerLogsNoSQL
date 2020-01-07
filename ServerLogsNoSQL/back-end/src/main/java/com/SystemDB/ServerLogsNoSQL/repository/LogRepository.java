package com.SystemDB.ServerLogsNoSQL.repository;

import com.SystemDB.ServerLogsNoSQL.model.Log;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.Date;
import java.util.List;

@Repository
public interface LogRepository extends MongoRepository<Log, String> {

    List<Log> findByLogTimestampBetween(Date from, Date to);
}