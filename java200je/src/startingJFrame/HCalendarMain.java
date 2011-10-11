package startingJFrame;

import java.awt.Dimension;

import javax.swing.JPanel;

public class HCalendarMain {
	public static void main(String[] args) {
		StartingJFrame startFrame = new StartingJFrame();
		JPanel cp = new JPanel();
		HCalendar hcal = new HCalendar(cp);
		startFrame.setMainJPanel(cp);
		startFrame.setSize(new Dimension(550,400));
		startFrame.validate();
	}
}
