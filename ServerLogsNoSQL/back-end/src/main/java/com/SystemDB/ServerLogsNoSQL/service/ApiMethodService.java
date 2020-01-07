package com.SystemDB.ServerLogsNoSQL.service;

import com.SystemDB.ServerLogsNoSQL.repository.LogRepository;
import com.SystemDB.ServerLogsNoSQL.response.Method2;
import com.SystemDB.ServerLogsNoSQL.response.Method4;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.aggregation.*;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;

import static org.springframework.data.mongodb.core.aggregation.Aggregation.*;

@Service
public class ApiMethodService {

    @Autowired
    private MongoTemplate mongoTemplate;

    @Autowired
    private LogRepository logRepository;

    public ResponseEntity<?> getMethod2(Date from, Date to, String type) {

        MatchOperation matchOperation = Aggregation.match(new Criteria("type").is(type).and("log_timestamp").gte(from).lte(to));
        ProjectionOperation projectionOperation = Aggregation.project()
                .andExpression("log_timestamp").dateAsFormattedString("%Y-%m-%d").as("date");

        GroupOperation groupOperation = Aggregation.group(fields().and("date")).count().as("requests");

        Aggregation aggregation = newAggregation(matchOperation, projectionOperation, groupOperation);
        AggregationResults<Method2> result = mongoTemplate.aggregate(aggregation, "log", Method2.class);
        List<Method2> resultList = result.getMappedResults();

        return ResponseEntity.ok(resultList);
    }

    public ResponseEntity<?> getMethod4(Date from, Date to) {

        MatchOperation matchOperation = Aggregation.match(new Criteria("log_timestamp").gte(from).lte(to));
        GroupOperation groupOperation = Aggregation.group(fields().and("http_method")).count().as("total");
        SortOperation sortOperation = Aggregation.sort(Sort.Direction.ASC, "total");
        LimitOperation limitOperation = Aggregation.limit(2);

        Aggregation aggregation = newAggregation(matchOperation, groupOperation, sortOperation, limitOperation);
        AggregationResults<Method4> result = mongoTemplate.aggregate(aggregation, "log", Method4.class);
        List<Method4> resultList = result.getMappedResults();

        return ResponseEntity.ok(resultList);
    }

}
