package startingJFrame;

import java.awt.Dimension;

import javax.swing.JPanel;

public class CalendarJFrameMain {
	public static void main(String[] args) {
		StartingJFrame startFrame = new StartingJFrame();
		CalendarJPanel cp = new CalendarJPanel(startFrame);
		startFrame.setMainJPanel(cp);
		startFrame.setSize(new Dimension(550, 400));
		startFrame.validate();
	}
}
