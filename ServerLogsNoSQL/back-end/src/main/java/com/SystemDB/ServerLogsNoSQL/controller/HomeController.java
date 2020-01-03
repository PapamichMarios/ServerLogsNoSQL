package com.SystemDB.ServerLogsNoSQL.controller;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;

@RestController
public class HomeController {

    @GetMapping(value="/")
    public String index() {
        return "index";
    }

    @GetMapping(value = {"/welcome"})
    public List<String> welcome() {
        List<String> categories = new ArrayList<>();
        categories.add("lol");
        categories.add("lol1");

        return categories;
//        return ResponseEntity.ok().build();
    }
}