package com.SystemDB.ServerLogsNoSQL.service;

import com.SystemDB.ServerLogsNoSQL.model.Log;
import com.SystemDB.ServerLogsNoSQL.response.Method1;
import com.mongodb.DBCollection;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.aggregation.*;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;

import static org.springframework.data.mongodb.core.aggregation.Aggregation.fields;
import static org.springframework.data.mongodb.core.aggregation.Aggregation.newAggregation;

@Service
public class ApiMethodService {

    @Autowired
    private MongoTemplate mongoTemplate;

    public ResponseEntity<?> getMethod2(Date from, Date to, String type) {

        MatchOperation matchOperation = Aggregation.match(new Criteria("type").is(type).and("log_timestamp").gte(from).lte(to));
        ProjectionOperation projectionOperation = Aggregation.project()
                .andExpression("log_timestamp").dateAsFormattedString("%Y-%m-%d").as("date");

        GroupOperation groupOperation = Aggregation.group(fields().and("date")).count().as("requests");

        Aggregation aggregation = newAggregation(matchOperation, projectionOperation, groupOperation);
        AggregationResults<Method1> result = mongoTemplate.aggregate(aggregation, "log", Method1.class);
        List<Method1> resultList = result.getMappedResults();

        return ResponseEntity.ok(resultList);
    }

}
