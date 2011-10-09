package startingJFrame;


import java.awt.AWTEvent;
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.Toolkit;
import java.awt.event.WindowEvent;

import javax.swing.JFrame;
import javax.swing.JPanel;

public class StartingJFrame extends JFrame {
	private static final long serialVersionUID = 1L;
	JPanel mainp;

	public StartingJFrame() {
		System.out.println(this.getClass().getName() + "    start!!");
		inits();
	}

	private void inits() {
		// TODO Auto-generated method stub
		mainp = (JPanel) this.getContentPane();
		mainp.setLayout(new BorderLayout());
		this.setSize(new Dimension(400, 300));
		initFrame();
		this.setTitle(this.getClass().getName());
	}

	public void addLiseners() {
	}

	private void initFrame() {
		// TODO Auto-generated method stub
		Dimension monitorSize = Toolkit.getDefaultToolkit().getScreenSize();
		Dimension frameSize = this.getSize();

		if (frameSize.height > monitorSize.height) {
			frameSize.height = monitorSize.height;
		}

		if (frameSize.width > monitorSize.width) {
			frameSize.width = monitorSize.width;
		}
		int locationX = (monitorSize.width - frameSize.width)/2;
		int locationY = (monitorSize.height - frameSize.height)/2;
		this.setLocation(locationX, locationY);
		this.setVisible(true);
		enableEvents(AWTEvent.WINDOW_EVENT_MASK);
	}
	
	public void processWindowEvent(WindowEvent e) {
		super.processWindowEvent(e);
		if(e.getID() == WindowEvent.WINDOW_CLOSING) {
			System.out.println(this.getClass().getName() + "   End!!");
			System.exit(1);
		}
	}
	
	public void setMainJPanel(javax.swing.JComponent c) {
		mainp.add(c);
	}
}
