package com.SystemDB.ServerLogsNoSQL.response;

public class Method4 {
    private String id;
    private int total;

    public Method4() {
    }

    public Method4(String id, int total) {
        this.id = id;
        this.total = total;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public int getTotal() {
        return total;
    }

    public void setTotal(int total) {
        this.total = total;
    }
}
