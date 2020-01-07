package com.SystemDB.ServerLogsNoSQL.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Document(collection="log")
public class Log {

    @Id private String id;

    private String resource;

    @Field("source_ip")
    private String sourceIp;

    @Field("http_method")
    private String httpMethod;

    private String type;

    @Field("agent_string")
    private String agentString;

    private int size;

    @Field("http_response")
    private int httpResponse;

    @Field("log_timestamp")
    private Date logTimestamp;

    private List<String> blocks = new ArrayList<>();

    private List<String> destinations = new ArrayList<>();

    public Log() {

    }

    public Log(String id, String resource, String source_ip, String http_method, String type, String agent_string, int size, int http_response, Date log_timestamp, List<String> blocks, List<String> destinations) {
        this.id = id;
        this.resource = resource;
        this.sourceIp = source_ip;
        this.httpMethod = http_method;
        this.type = type;
        this.agentString = agent_string;
        this.size = size;
        this.httpResponse = http_response;
        this.logTimestamp = log_timestamp;
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
        return sourceIp;
    }

    public void setSource_ip(String source_ip) {
        this.sourceIp = source_ip;
    }

    public String getHttp_method() {
        return httpMethod;
    }

    public void setHttp_method(String http_method) {
        this.httpMethod = http_method;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getAgent_string() {
        return agentString;
    }

    public void setAgent_string(String agent_string) {
        this.agentString = agent_string;
    }

    public int getSize() {
        return size;
    }

    public void setSize(int size) {
        this.size = size;
    }

    public int getHttp_response() {
        return httpResponse;
    }

    public void setHttp_response(int http_response) {
        this.httpResponse = http_response;
    }

    public Date getLog_timestamp() {
        return logTimestamp;
    }

    public void setLog_timestamp(Date log_timestamp) {
        this.logTimestamp = log_timestamp;
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
