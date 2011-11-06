import java.awt.*;
import javax.swing.*;
// Main에서는 그냥 Graph를 window상에 띄우는 일만 함
public class ShortestPathMain extends JFrame {
	private static final long serialVersionUID = 9081019894012314471L;

	Graph graph = new Graph();

	public ShortestPathMain() {
		setTitle("Container Terminal Simulation");
		Container ct = getContentPane();
		ct.add("Center", graph);
	}

	public static void main(String[] args) {
		ShortestPathMain sp = new ShortestPathMain();
		sp.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		sp.setSize(990, 650);
		sp.setLocation(25, 25);
		sp.setVisible(true);
	}

}
