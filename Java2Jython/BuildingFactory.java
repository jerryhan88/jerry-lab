import org.jython.book.interfaces.BuildingType;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;

public class BuildingFactory {

    private PyObject buildingClass;


    public BuildingFactory() {
        PythonInterpreter interpreter = new PythonInterpreter();
        interpreter.exec("from Building import Building");
        buildingClass = interpreter.get("Building");
    }

    public BuildingType create (String name, String location, String id) {

        PyObject buildingObject = buildingClass.__call__(new PyString(name),
                                                         new PyString(location),
                                                         new PyString(id));
        return (BuildingType)buildingObject.__tojava__(BuildingType.class);
    }

}