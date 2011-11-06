import java.awt.Frame;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.JPanel;
import javax.swing.JWindow;

public class itemFrame extends JWindow {
	private static final long serialVersionUID = 1L;
	JPanel whole;

	public itemFrame(Frame f) {
		setBounds(60, 60, 100, 100);
		addWindowListener(new WindowAdapter() {

			public void windowClosing(WindowEvent e) {
				System.exit(0); // An Exit Listener
			}
		});
		
		setVisible(true);
	}

}
