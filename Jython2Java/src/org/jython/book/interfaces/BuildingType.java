package org.jython.book.interfaces;

public interface BuildingType {

    public String getBuildingName();
    public String getBuildingAddress();
    public int getBuildingId();
    public void setBuildingName(String name);
    public void setBuildingAddress(String address);
    public void setBuildingId(int id);
    public String getDoc();

}