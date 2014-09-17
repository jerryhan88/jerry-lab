package org.jython.book;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.jython.book.interfaces.CostCalculatorType;
import org.jybhon.book.factory.JythonObjectFactory;

public class Main_calc {

    public static void main(String[] args) {

        // Create factory and coerce Jython calculator object
        JythonObjectFactory factory = JythonObjectFactory.getInstance();
        CostCalculatorType costCalc = (CostCalculatorType)
            factory.createObject(CostCalculatorType.class, "CostCalculator");
        System.out.println(costCalc.calculateCost(25.96, .07));

    }
}