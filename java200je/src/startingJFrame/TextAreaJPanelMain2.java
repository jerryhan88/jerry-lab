package startingJFrame;

public class TextAreaJPanelMain2 {
	public static void main(String[] args) {
		TextAreaJPanel2 bp = new TextAreaJPanel2();
		
		StartingJFrame frame = new StartingJFrame();
		frame.setMainJPanel(bp);
		frame.setSize(500,400);
		frame.validate();
	}
}
