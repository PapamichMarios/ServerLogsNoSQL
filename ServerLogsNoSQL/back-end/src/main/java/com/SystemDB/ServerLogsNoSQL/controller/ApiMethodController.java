package com.SystemDB.ServerLogsNoSQL.controller;

import com.SystemDB.ServerLogsNoSQL.service.ApiMethodService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.aggregation.Aggregation;
import org.springframework.data.mongodb.core.aggregation.GroupOperation;
import org.springframework.data.mongodb.core.aggregation.MatchOperation;
import org.springframework.data.mongodb.core.aggregation.ProjectionOperation;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Date;

import static org.springframework.data.mongodb.core.aggregation.Aggregation.*;

@RestController
@RequestMapping("/api/methods")
public class ApiMethodController {

    @Autowired
    private ApiMethodService apiMethodService;

    @GetMapping(value = "/1")
    public ResponseEntity<?> getMethod1(@RequestParam("from") @DateTimeFormat(pattern="yyyy-MM-dd") Date from,
                                        @RequestParam("to")   @DateTimeFormat(pattern="yyyy-MM-dd") Date to,
                                        @RequestParam("type") String type) {

        return this.apiMethodService.getMethod1(from, to, type);
    }
}
