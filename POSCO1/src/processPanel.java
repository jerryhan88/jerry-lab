import java.awt.BorderLayout;

import java.awt.Container;

import javax.swing.JPanel;

public class processPanel extends JPanel {
	private static final long serialVersionUID = 1L;
	processDrawing graph;

	public processPanel(int ppx, int ppy, int psx, int psy) {
		this.setLayout(new BorderLayout());
		this.setBounds(ppx, ppy, psx, psy);
		graph = new processDrawing();
		this.add("Center", graph);
	}
}
