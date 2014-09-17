package org.jython.book;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.jython.book.interfaces.BuildingType;
import org.jybhon.book.factory.JythonObjectFactory;

public class Main {

    public static void main(String[] args) {

    // Obtain an instance of the object factory
    JythonObjectFactory factory = JythonObjectFactory.getInstance();

    // Call the createObject() method on the object factory by
    // passing the Java interface and the name of the Jython module
    // in String format. The returning object is casted to the the same
    // type as the Java interface and stored into a variable.
    BuildingType building = (BuildingType) factory.createObject(
        BuildingType.class, "Building");
    // Populate the object with values using the setter methods
    building.setBuildingName("BUIDING-A");
    building.setBuildingAddress("100 MAIN ST.");
    building.setBuildingId(1);
    System.out.println(building.getBuildingId() + " " + building.getBuildingName() + " " +
        building.getBuildingAddress());
    System.out.println(building.getDoc());

    }

}