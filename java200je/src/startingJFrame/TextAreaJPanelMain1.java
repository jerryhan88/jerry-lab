package startingJFrame;

public class TextAreaJPanelMain1 {
	public static void main(String[] args) {
		TextAreaJPanel1 bp = new TextAreaJPanel1();
		
		StartingJFrame frame = new StartingJFrame();
		frame.setMainJPanel(bp);
		frame.setSize(500,400);
		frame.validate();
	}
}
