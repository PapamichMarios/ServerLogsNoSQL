package com.SystemDB.ServerLogsNoSQL.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Document(collection="log")
public class Log {

    @Id private String id;

    private String resource;

    private String source_ip;

    private String http_method;

    private String type;

    private String agent_string;

    private int size;

    private int http_response;

    private Date log_timestamp;

    private List<String> blocks = new ArrayList<>();

    private List<String> destinations = new ArrayList<>();

    public Log() {

    }

    public Log(String id, String resource, String source_ip, String http_method, String type, String agent_string, int size, int http_response, Date log_timestamp, List<String> blocks, List<String> destinations) {
        this.id = id;
        this.resource = resource;
        this.source_ip = source_ip;
        this.http_method = http_method;
        this.type = type;
        this.agent_string = agent_string;
        this.size = size;
        this.http_response = http_response;
        this.log_timestamp = log_timestamp;
        this.blocks = blocks;
        this.destinations = destinations;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getResource() {
        return resource;
    }

    public void setResource(String resource) {
        this.resource = resource;
    }

    public String getSource_ip() {
        return source_ip;
    }

    public void setSource_ip(String source_ip) {
        this.source_ip = source_ip;
    }

    public String getHttp_method() {
        return http_method;
    }

    public void setHttp_method(String http_method) {
        this.http_method = http_method;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getAgent_string() {
        return agent_string;
    }

    public void setAgent_string(String agent_string) {
        this.agent_string = agent_string;
    }

    public int getSize() {
        return size;
    }

    public void setSize(int size) {
        this.size = size;
    }

    public int getHttp_response() {
        return http_response;
    }

    public void setHttp_response(int http_response) {
        this.http_response = http_response;
    }

    public Date getLog_timestamp() {
        return log_timestamp;
    }

    public void setLog_timestamp(Date log_timestamp) {
        this.log_timestamp = log_timestamp;
    }

    public List<String> getBlocks() {
        return blocks;
    }

    public void setBlocks(List<String> blocks) {
        this.blocks = blocks;
    }

    public List<String> getDestinations() {
        return destinations;
    }

    public void setDestinations(List<String> destinations) {
        this.destinations = destinations;
    }
}
