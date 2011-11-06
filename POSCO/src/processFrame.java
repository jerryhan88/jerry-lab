import java.awt.Container;

import javax.swing.JFrame;


public class processFrame extends JFrame {
	private static final long serialVersionUID = 1L;
	
	processDrawing graph = new processDrawing();

	public processFrame() {
		setTitle("Container Terminal Simulation");
		Container ct = getContentPane();
		ct.add("Center", graph);
	}
	
	public static void main(String[] args) {
		processFrame pF = new processFrame();
		pF.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		pF.setBounds(100, 50, 800, 300);
		pF.setResizable(false);
		pF.setVisible(true);
	}
	
}
