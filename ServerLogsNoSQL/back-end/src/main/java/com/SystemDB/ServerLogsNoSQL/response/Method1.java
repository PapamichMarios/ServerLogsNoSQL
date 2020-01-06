package com.SystemDB.ServerLogsNoSQL.response;

public class Method1 {

    private String id;
    private int requests;

    public Method1() {
    }

    public Method1(String id, int requests) {
        this.id = id;
        this.requests = requests;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public int getRequests() {
        return requests;
    }

    public void setRequests(int requests) {
        this.requests = requests;
    }
}
