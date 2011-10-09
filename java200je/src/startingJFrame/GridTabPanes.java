package startingJFrame;

import java.awt.BorderLayout;

import javax.swing.JPanel;
import javax.swing.JTabbedPane;


public class GridTabPanes extends JPanel {
	private static final long serialVersionUID = 1L;
	JTabbedPane jTabbedPane1 = new JTabbedPane();
	ButtonJPanel5 jPane5 = new ButtonJPanel5();
	
	public GridTabPanes() {
		inits();
	}
	
	void inits() {
		this.setLayout(new BorderLayout());
		this.add(jTabbedPane1, BorderLayout.CENTER);
		jTabbedPane1.add(jPane5, "Button Insets");
	}

}
