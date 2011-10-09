package startingJFrame;


public class GridTabPanesMain {
	public static void main(String[] args) {
		GridTabPanes bp = new GridTabPanes();
		StartingJFrame frame = new StartingJFrame();
		frame.setMainJPanel(bp);
		frame.setSize(600,400);
		frame.validate();
	}
}
