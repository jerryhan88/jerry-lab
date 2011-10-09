package startingJFrame;

public class TextAreaJPanelMain {
	public static void main(String[] args) {
		TextAreaJPanel bp = new TextAreaJPanel();
		
		StartingJFrame frame = new StartingJFrame();
		frame.setMainJPanel(bp);
		frame.setSize(500,400);
		frame.validate();
	}
}
