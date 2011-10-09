package startingJFrame;

public class BorderFlowMain {
	public static void main(String[] args) {
		BorderFlowJPanel bp = new BorderFlowJPanel();
		StartingJFrame frame = new StartingJFrame();
		frame.setMainJPanel(bp);
		frame.setSize(500,300);
		frame.validate();
		
		BorderFlowJPanel bp1 = new BorderFlowJPanel();
		StartingJFrame frame1 = new StartingJFrame();
		frame1.setMainJPanel(bp1);
		frame1.setSize(300,300);
		frame1.validate();
	}
}
