package com.SystemDB.ServerLogsNoSQL.response;

public class Method2 {

    private String id;
    private int requests;

    public Method2() {
    }

    public Method2(String id, int requests) {
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
